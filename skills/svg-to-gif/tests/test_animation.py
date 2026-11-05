"""Behavioral regressions; run with Python's standard-library unittest runner."""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
import copy
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import animation_tools as tools
import render_animation as renderer


class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.paths = {}
        for name in tools.TOOL_NAMES:
            path = self.directory / name
            path.write_text("fixture binary identity " + name, encoding="utf-8")
            path.chmod(0o700)
            self.paths[name] = str(path)
        self.calls = []

    def fake_run(self, command):
        command = [str(item) for item in command]
        self.calls.append(command)
        name = Path(command[0]).name
        if command[1] in ("--version", "-version"):
            return name + " version 0.0.1-custom"
        if name == "resvg":
            Path(command[-1]).write_bytes(tools._png(32, 24, 0))
        elif command[-1] != "-":
            # Control-flow fixture: real media decoding belongs to smoke tests.
            Path(command[-1]).write_bytes(b"GIF89a" + struct.pack("<HH", 32, 24) + b"\0\0\0;")
        return ""

    def test_old_version_is_accepted_when_required_operations_work(self):
        with mock.patch.object(tools, "_run", side_effect=self.fake_run):
            report = tools.probe_tools(**self.paths)
        self.assertTrue(report["ok"], report["errors"])
        self.assertTrue(all(report["capabilities"].values()))
        self.assertIn("0.0.1-custom", report["tools"]["ffmpeg"]["version"])
        self.assertEqual(len(report["tools"]["ffmpeg"]["sha256"]), 64)
        self.assertTrue(any("-filter_complex" in command for command in self.calls))

    def test_explicit_missing_binary_does_not_fall_back_to_path(self):
        missing = str(self.directory / "missing" / "ffmpeg")
        with mock.patch.object(tools.shutil, "which", return_value=self.paths["ffmpeg"]) as which:
            with mock.patch.object(tools, "_run", side_effect=self.fake_run):
                report = tools.probe_tools(ffmpeg=missing, resvg=self.paths["resvg"], no_gifsicle=True)
        which.assert_not_called()
        self.assertFalse(report["ok"])
        self.assertFalse(report["tools"]["ffmpeg"]["available"])
        self.assertTrue(report["capabilities"]["svg_to_png"])
        self.assertFalse(any(Path(command[0]).name == "ffmpeg" for command in self.calls))

    def test_incompatible_required_binary_is_not_replaced(self):
        def failed_palette(command):
            if "-filter_complex" in command:
                raise RuntimeError("Unknown filter palettegen")
            return self.fake_run(command)
        with mock.patch.object(tools, "_run", side_effect=failed_palette):
            report = tools.probe_tools(**self.paths)
        self.assertFalse(report["ok"])
        self.assertFalse(report["tools"]["ffmpeg"]["compatible"])
        self.assertIn("Unknown filter palettegen", " ".join(report["errors"]))
        self.assertEqual(report["tools"]["ffmpeg"]["path"], str(Path(self.paths["ffmpeg"]).resolve()))
        self.assertEqual(Path(self.paths["ffmpeg"]).read_text(), "fixture binary identity ffmpeg")

    def test_optional_optimizer_failure_does_not_block_rendering(self):
        def failed_optimizer(command):
            if "-O3" in command:
                raise RuntimeError("Unsupported optimization")
            return self.fake_run(command)
        with mock.patch.object(tools, "_run", side_effect=failed_optimizer):
            report = tools.probe_tools(**self.paths)
        self.assertTrue(report["ok"], report["errors"])
        self.assertFalse(report["capabilities"]["gif_optimize"])
        self.assertFalse(report["tools"]["gifsicle"]["compatible"])
        self.assertIn("Unsupported optimization", " ".join(report["warnings"]))

    def test_version_query_failure_does_not_override_functional_probe(self):
        def failed_version(command):
            if command[1] in ("--version", "-version"):
                raise RuntimeError("unsupported version flag")
            return self.fake_run(command)
        with mock.patch.object(tools, "_run", side_effect=failed_version):
            report = tools.probe_tools(**self.paths)
        self.assertTrue(report["ok"], report["errors"])
        self.assertIsNone(report["tools"]["ffmpeg"]["version"])
        self.assertTrue(report["warnings"])

    def test_same_version_changed_binary_is_detected(self):
        with mock.patch.object(tools, "_run", side_effect=self.fake_run):
            before = tools.resolve_tools(**self.paths)
            Path(self.paths["ffmpeg"]).write_text("different build, same version", encoding="utf-8")
            after = tools.resolve_tools(**self.paths)
        drift = tools.compare_toolchains(after, before)
        self.assertEqual(len(drift), 1)
        self.assertIn("ffmpeg.sha256 changed", drift[0])
        self.assertFalse(tools.compare_toolchains(before, copy.deepcopy(before)))


def gif_fixture(width=100, height=80, size=None, delays=(10, 10)):
    """A real two-color GIF with 1px subframes, infinite looping and known delays."""
    data = bytearray(b"GIF89a" + struct.pack("<HH", width, height) + b"\x80\0\0")
    data.extend(b"\0\0\0\xff\xff\xff")
    data.extend(b"!\xff\x0bNETSCAPE2.0\x03\x01\0\0\0")
    for delay in delays:
        data.extend(b"!\xf9\x04\0" + struct.pack("<H", delay) + b"\0\0")
        data.extend(b",\0\0\0\0\x01\0\x01\0\0\x02\x02\x44\x01\0")
    if size is not None:
        # Fill by bounded comment sub-blocks; desired sizes below leave space.
        remaining = size - len(data) - 4
        data.extend(b"!\xfe")
        while remaining > 0:
            length = min(255, remaining - 1)
            if length <= 0:
                raise ValueError("fixture size leaves a one-byte remainder")
            data.extend(bytes([length]) + b"x" * length)
            remaining -= length + 1
        data.append(0)
    data.append(0x3B)
    return bytes(data)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.scene = self.directory / "scene.py"
        self.scene.write_text('def svg_frame(t):\n    return \'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="80"/>\'\n')
        self.output = self.directory / "result.gif"
        self.toolchain = {
            "schema_version": 1, "ok": True, "errors": [], "warnings": [],
            "python": {"path": "/fixture/python", "version": "3.9.6"},
            "tools": {
                name: {"path": "/fixture/" + name, "version": "fixture", "sha256": "abc",
                       "disabled": name == "gifsicle", "compatible": name != "gifsicle"}
                for name in tools.TOOL_NAMES
            },
        }
        self.width = 200
        self.sizes = iter([1600, 1300, 1700, 1500, 1800])
        self.encode_count = 0
        self.encode_error = None

    def fake_run(self, command, **kwargs):
        if "-w" in command:
            self.width = int(command[command.index("-w") + 1])
        return None

    def fake_encode(self, frames, output, fps, colors, ffmpeg):
        self.encode_count += 1
        if self.encode_error:
            raise self.encode_error
        output.write_bytes(gif_fixture(width=self.width, size=next(self.sizes)))

    def run_renderer(self, *arguments):
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(renderer, "probe_tools", return_value=self.toolchain))
            stack.enter_context(mock.patch.object(renderer, "run", side_effect=self.fake_run))
            stack.enter_context(mock.patch.object(renderer, "encode_frames", side_effect=self.fake_encode))
            stack.enter_context(redirect_stdout(io.StringIO()))
            stack.enter_context(redirect_stderr(io.StringIO()))
            return renderer.main(["--scene", str(self.scene), "--output", str(self.output),
                                  "--width", "200", "--fps", "3", "--seconds", "1", *arguments])

    def test_fallbacks_never_increase_dimensions_rate_or_palette(self):
        for initial in ((100, 3, 4), (120, 4, 8), (560, 10, 48), (2000, 50, 256)):
            candidates = renderer.make_presets(*initial, target=True)
            self.assertEqual(candidates[0], initial)
            self.assertEqual(len(candidates), len(set(candidates)))
            self.assertLessEqual(len(candidates), 5)
            for before, after in zip(candidates, candidates[1:]):
                self.assertTrue(all(b <= a for a, b in zip(before, after)))

    def test_strict_unmet_budget_keeps_smallest_not_last_candidate(self):
        status = self.run_renderer("--target-kib", "0.5", "--strict-target")
        report = json.loads(Path(str(self.output) + ".json").read_text())
        self.assertEqual(status, 2)
        self.assertFalse(report["target_met"])
        self.assertEqual(report["selected"]["attempt"], 2)
        self.assertEqual(report["selected"]["size_bytes"], 1300)
        self.assertEqual(self.output.stat().st_size, 1300)
        self.assertEqual(report["output"]["sha256"], renderer.sha256(self.output))
        self.assertEqual(self.encode_count, 5)

    def test_reaching_budget_stops_search_and_saves_actual_result(self):
        status = self.run_renderer("--target-kib", "1.4", "--strict-target")
        report = json.loads(Path(str(self.output) + ".json").read_text())
        self.assertEqual(status, 0)
        self.assertTrue(report["target_met"])
        self.assertEqual(self.encode_count, 2)
        self.assertEqual(report["selected"]["gif"], renderer.gif_info(self.output))

    def test_existing_output_or_sidecar_blocks_before_probing(self):
        for destination in (self.output, Path(str(self.output) + ".json")):
            with self.subTest(destination=destination):
                destination.write_text("keep me")
                with mock.patch.object(renderer, "probe_tools") as probe:
                    with self.assertRaises(renderer.RenderError):
                        renderer.main(["--scene", str(self.scene), "--output", str(self.output)])
                probe.assert_not_called()
                self.assertEqual(destination.read_text(), "keep me")
                destination.unlink()

    def test_explicit_overwrite_replaces_output_and_sidecar(self):
        self.output.write_text("old gif")
        Path(str(self.output) + ".json").write_text("old manifest")
        self.assertEqual(self.run_renderer("--overwrite"), 0)
        self.assertEqual(self.output.stat().st_size, 1600)
        self.assertEqual(json.loads(Path(str(self.output) + ".json").read_text())["output"]["size_bytes"], 1600)

    def test_failed_preflight_writes_nothing_and_never_imports_scene(self):
        self.output = self.directory / "not-created" / "result.gif"
        self.toolchain.update(ok=False, errors=["required tool unavailable"])
        with mock.patch.object(renderer, "load_scene") as load:
            with self.assertRaisesRegex(renderer.RenderError, "required tool unavailable"):
                self.run_renderer()
        load.assert_not_called()
        self.assertFalse(self.output.parent.exists())

    def test_toolchain_drift_blocks_before_scene_import(self):
        previous = copy.deepcopy(self.toolchain)
        previous["tools"]["ffmpeg"]["sha256"] = "previous build"
        baseline = self.directory / "prior.json"
        baseline.write_text(json.dumps({"toolchain": previous}))
        with mock.patch.object(renderer, "load_scene") as load:
            with self.assertRaisesRegex(renderer.RenderError, "ffmpeg.sha256 changed"):
                self.run_renderer("--require-toolchain", str(baseline))
        load.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_failed_encoding_keeps_existing_artifacts_unchanged(self):
        self.output.write_text("old gif")
        sidecar = Path(str(self.output) + ".json")
        sidecar.write_text("old manifest")
        self.encode_error = renderer.RenderError("encoding failed")
        with self.assertRaisesRegex(renderer.RenderError, "encoding failed"):
            self.run_renderer("--overwrite")
        self.assertEqual(self.output.read_text(), "old gif")
        self.assertEqual(sidecar.read_text(), "old manifest")

    def test_overwrite_never_follows_output_symlink(self):
        target = self.directory / "important.gif"
        target.write_text("preserve target")
        try:
            self.output.symlink_to(target)
        except OSError:
            self.skipTest("symlink creation unavailable on this host")
        with self.assertRaisesRegex(renderer.RenderError, "symbolic link"):
            self.run_renderer("--overwrite")
        self.assertEqual(target.read_text(), "preserve target")
        self.assertTrue(self.output.is_symlink())

    def test_encoded_width_must_match_requested_width(self):
        def incorrect_encode(frames, output, fps, colors, ffmpeg):
            output.write_bytes(gif_fixture(width=1))
        self.fake_encode = incorrect_encode
        with self.assertRaises(renderer.RenderError):
            self.run_renderer()
        self.assertFalse(self.output.exists())

    def test_gif_parser_reads_timing_and_rejects_truncation(self):
        self.output.write_bytes(gif_fixture(delays=(7, 13)))
        info = renderer.gif_info(self.output)
        self.assertEqual(info["frame_delays_centiseconds"], [7, 13])
        self.assertEqual(info["duration_seconds"], 0.2)
        self.assertEqual(info["loop_count"], 0)
        self.assertEqual(info["frame_count"], 2)
        self.output.write_bytes(self.output.read_bytes()[:-1])
        with self.assertRaises(renderer.RenderError):
            renderer.gif_info(self.output)


if __name__ == "__main__":
    unittest.main()
