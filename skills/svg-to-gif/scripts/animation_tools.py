#!/usr/bin/env python3
"""Read-only tool discovery and functional preflight for svg-to-gif.

Python 3.9+; standard library only. Never installs or changes dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib


TOOL_NAMES = ("resvg", "ffmpeg", "gifsicle")
PROBE_TIMEOUT = 30


def _run(command):
    """Execute one selected binary without a shell and retain diagnostic output."""
    try:
        result = subprocess.run(
            [str(part) for part in command], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=PROBE_TIMEOUT, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(str(exc)) from exc
    stdout = result.stdout.decode("utf-8", errors="replace")
    stderr = result.stderr.decode("utf-8", errors="replace")
    if result.returncode:
        detail = (stderr or stdout).strip()[-3000:]
        raise RuntimeError(f"exit {result.returncode}: {detail}")
    return (stdout or stderr).strip()


def _fingerprint(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _resolve(name, override):
    if override is not None:
        # An explicit path never falls back to some other PATH installation.
        requested = os.path.expanduser(str(override))
        if Path(requested).is_absolute() or Path(requested).parent != Path("."):
            candidate = Path(requested).resolve()
        elif Path(requested).is_file():
            candidate = Path(requested).resolve()
        else:
            found = shutil.which(requested)
            candidate = Path(found).resolve() if found else None
    else:
        found = shutil.which(name)
        candidate = Path(found).resolve() if found else None
    if candidate is None or not candidate.is_file():
        return None
    if os.name != "nt" and not os.access(candidate, os.X_OK):
        return None
    return candidate


def resolve_tools(ffmpeg=None, resvg=None, gifsicle=None, no_gifsicle=False):
    """Find selected executables, report identities; compatibility is still unknown.

    The returned report can be saved as a toolchain record. A version-command
    failure is a warning, not proof that the requested rendering is unsupported.
    """
    report = {
        "schema_version": 1,
        "stage": "discovery",
        "python": {"path": str(Path(sys.executable).resolve()),
                   "version": platform.python_version()},
        "platform": {"system": platform.system(), "release": platform.release(),
                     "machine": platform.machine()},
        "tools": {},
        "capabilities": {"svg_to_png": False, "gif_palette": False,
                         "gif_optimize": False},
        "errors": [], "warnings": [], "ok": False,
    }
    if sys.version_info < (3, 9):
        report["errors"].append("Python 3.9+ is required; select an existing compatible interpreter before rendering.")
    overrides = {"ffmpeg": ffmpeg, "resvg": resvg, "gifsicle": gifsicle}
    for name in TOOL_NAMES:
        entry = {"path": None, "version": None, "version_output": None,
                 "sha256": None, "available": False, "compatible": None,
                 "disabled": name == "gifsicle" and no_gifsicle, "error": None}
        report["tools"][name] = entry
        if entry["disabled"]:
            continue
        path = _resolve(name, overrides[name])
        if path is None:
            entry["error"] = (
                f"{name} executable not found or not executable. "
                f"Select an existing binary with --{name} PATH; "
                "ask before installing anything."
            )
            report["warnings" if name == "gifsicle" else "errors"].append(entry["error"])
            continue
        entry["path"] = str(path)
        entry["available"] = True
        try:
            entry["sha256"] = _fingerprint(path)
        except OSError as exc:
            entry["error"] = f"Cannot fingerprint {name} at {path}: {exc}"
            report["warnings" if name == "gifsicle" else "errors"].append(entry["error"])
        try:
            version_output = _run([path, "-version" if name == "ffmpeg" else "--version"])
            entry["version_output"] = version_output[:8000]
            entry["version"] = version_output.splitlines()[0] if version_output else None
        except RuntimeError as exc:
            report["warnings"].append(f"Cannot read {name} version: {exc}; capability probe decides compatibility.")
    return report


def _png(width, height, phase):
    """Build a tiny RGB fixture without depending on the SVG renderer."""
    def chunk(kind, payload):
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff))
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            row.extend((245, 170, 40) if (x + phase * 8) % width < 8 else (20, 30, 45))
        rows.append(bytes(row))
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows))) + chunk(b"IEND", b""))


def _check_png(path):
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError("renderer did not produce a PNG")
    if struct.unpack(">II", header[16:24]) != (32, 24):
        raise RuntimeError("renderer did not honor the requested width/aspect ratio")


def _check_gif(path):
    data = path.read_bytes()
    if len(data) < 14 or data[:6] not in (b"GIF87a", b"GIF89a") or data[-1:] != b";":
        raise RuntimeError("encoder did not produce a complete GIF")
    if struct.unpack("<HH", data[6:10]) != (32, 24):
        raise RuntimeError("encoder produced incorrect GIF dimensions")


def probe_tools(ffmpeg=None, resvg=None, gifsicle=None, no_gifsicle=False):
    """Return a JSON-serializable report from actual temporary render/encode tests.

    report['ok'] requires SVG rasterization and the GIF palette pipeline to work.
    Optional gifsicle failure only disables optimization. No minimum version is
    guessed: older and unfamiliar builds are accepted when these probes pass.
    """
    report = resolve_tools(ffmpeg, resvg, gifsicle, no_gifsicle)
    report["stage"] = "preflight"
    entries = report["tools"]
    with tempfile.TemporaryDirectory(prefix="svg_to_gif_probe_") as temporary:
        directory = Path(temporary)
        svg_path = directory / "probe.svg"
        svg_path.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="48" viewBox="0 0 64 48">'
            '<rect width="64" height="48" fill="#142030"/>'
            '<circle cx="32" cy="24" r="12" fill="#efaa28"/></svg>', encoding="utf-8",
        )
        if entries["resvg"]["available"]:
            try:
                _run([entries["resvg"]["path"], "-w", "32", svg_path, directory / "probe.png"])
                _check_png(directory / "probe.png")
                report["capabilities"]["svg_to_png"] = True
                entries["resvg"]["compatible"] = True
            except (RuntimeError, OSError) as exc:
                entries["resvg"]["compatible"] = False
                entries["resvg"]["error"] = f"resvg SVG-to-PNG probe failed: {exc}"
                report["errors"].append(entries["resvg"]["error"])
        for frame in range(2):
            (directory / f"frame_{frame:04d}.png").write_bytes(_png(32, 24, frame))
        gif_path = directory / "probe.gif"
        if entries["ffmpeg"]["available"]:
            try:
                palette = ("[0:v]split[a][b];[a]palettegen=max_colors=16:stats_mode=full[p];"
                           "[b][p]paletteuse=dither=none:diff_mode=rectangle")
                _run([entries["ffmpeg"]["path"], "-hide_banner", "-loglevel", "error",
                      "-nostdin", "-y", "-filter_complex_threads", "1", "-framerate", "10",
                      "-i", directory / "frame_%04d.png", "-filter_complex", palette,
                      "-loop", "0", gif_path])
                _check_gif(gif_path)
                _run([entries["ffmpeg"]["path"], "-hide_banner", "-loglevel", "error",
                      "-nostdin", "-i", gif_path, "-f", "null", "-"])
                report["capabilities"]["gif_palette"] = True
                entries["ffmpeg"]["compatible"] = True
            except (RuntimeError, OSError) as exc:
                entries["ffmpeg"]["compatible"] = False
                entries["ffmpeg"]["error"] = f"FFmpeg palettegen/paletteuse GIF probe failed: {exc}"
                report["errors"].append(entries["ffmpeg"]["error"])
        if entries["gifsicle"]["available"]:
            if report["capabilities"]["gif_palette"]:
                try:
                    optimized = directory / "optimized.gif"
                    _run([entries["gifsicle"]["path"], "-O3", gif_path, "-o", optimized])
                    _check_gif(optimized)
                    report["capabilities"]["gif_optimize"] = True
                    entries["gifsicle"]["compatible"] = True
                except (RuntimeError, OSError) as exc:
                    entries["gifsicle"]["compatible"] = False
                    entries["gifsicle"]["error"] = f"Optional gifsicle optimization probe failed: {exc}"
                    report["warnings"].append(entries["gifsicle"]["error"])
            else:
                report["warnings"].append("gifsicle capability not tested because FFmpeg GIF probe did not pass.")
    report["ok"] = not report["errors"] and all(
        report["capabilities"][key] for key in ("svg_to_png", "gif_palette")
    )
    if not report["ok"]:
        report["next_step"] = (
            "Keep existing installations unchanged. Select another already-installed binary with "
            "--resvg/--ffmpeg PATH, or ask the user to approve an isolated, versioned installation "
            "with its exact source and destination. Do not automatically upgrade or uninstall."
        )
    return report


def compare_toolchains(current, previous):
    """Describe executable/version drift; accept only complete identity reports.

    Render manifests must be unwrapped by the caller. A successful comparison
    does not lock dynamic libraries, fonts, operating-system behavior or assets.
    """
    differences = []
    if not isinstance(previous, dict) or previous.get("schema_version") != 1:
        return ["Previous toolchain report has an unsupported or missing schema_version."]
    if not isinstance(previous.get("tools"), dict):
        return ["Previous toolchain report is missing executable identities."]
    for section, keys in (("python", ("path", "version")),):
        before = previous.get(section)
        after = current.get(section)
        if not isinstance(before, dict) or not isinstance(after, dict):
            differences.append(f"Missing {section} identity.")
            continue
        for key in keys:
            if key not in before or key not in after or before[key] != after[key]:
                differences.append(f"{section}.{key} changed: {before.get(key)!r} -> {after.get(key)!r}")
    for name in TOOL_NAMES:
        before = previous["tools"].get(name)
        after = current.get("tools", {}).get(name)
        if not isinstance(before, dict) or not isinstance(after, dict):
            differences.append(f"Missing {name} identity.")
            continue
        for key in ("path", "version", "sha256", "disabled"):
            if key not in before or key not in after or before[key] != after[key]:
                differences.append(f"{name}.{key} changed: {before.get(key)!r} -> {after.get(key)!r}")
    return differences


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in TOOL_NAMES:
        parser.add_argument(f"--{name}", metavar="PATH", help=f"Use this {name} executable")
    parser.add_argument("--no-gifsicle", action="store_true", help="Skip optional GIF optimization")
    parser.add_argument("--output", type=Path, help="Also save JSON; refuses to overwrite an existing file")
    parser.add_argument("--compare", type=Path, help="Compare with a prior preflight JSON; exit 2 on identity drift")
    args = parser.parse_args(argv)
    if args.no_gifsicle and args.gifsicle:
        parser.error("--gifsicle and --no-gifsicle cannot be used together")
    if args.output and args.output.exists():
        parser.error(f"Report already exists: {args.output}")
    previous = None
    if args.compare:
        try:
            previous = json.loads(args.compare.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            parser.error(f"Cannot read comparison report: {exc}")
    report = probe_tools(args.ffmpeg, args.resvg, args.gifsicle, args.no_gifsicle)
    if args.compare:
        report["drift"] = compare_toolchains(report, previous)
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        try:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(content)
        except OSError as exc:
            parser.error(f"Cannot write report: {exc}")
    print(content, end="")
    if not report["ok"]:
        return 1
    return 2 if report.get("drift") else 0


if __name__ == "__main__":
    sys.exit(main())
