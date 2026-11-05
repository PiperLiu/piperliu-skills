#!/usr/bin/env python3
"""Render a trusted Python SVG scene to a compact, looping GIF (Python 3.9+).

Only standard-library modules are imported; resvg and FFmpeg are external tools.
The scene supplies svg_frame(t), where 0 <= t < 1 is normalized loop progress.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from animation_tools import compare_toolchains, probe_tools


class RenderError(Exception):
    """A user-actionable scene, tool, or output failure."""


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command, timeout=120):
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RenderError(f"Could not run {command[0]}: {exc}") from exc
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace")[-3000:].strip()
        raise RenderError(f"{Path(command[0]).name} exited {result.returncode}: {detail}")


def make_presets(width, fps, colors, target=False):
    """At most five distinct candidates; fallback never increases a parameter."""
    presets = [(width, fps, colors)]
    if target:
        for width_factor, fps_factor, color_limit in (
                (.88, .9, 32), (.76, .8, 24), (.65, .7, 16), (.55, .6, 12)):
            item = (min(width, max(100, round(width * width_factor))),
                    min(fps, max(3, round(fps * fps_factor))),
                    min(colors, color_limit))
            if item not in presets:
                presets.append(item)
    return presets


def load_scene(path):
    """Import local trusted code without creating bytecode caches."""
    spec = importlib.util.spec_from_file_location("svg_to_gif_scene", path)
    if spec is None or spec.loader is None:
        raise RenderError(f"Cannot load Python scene: {path}")
    module = importlib.util.module_from_spec(spec)
    # Dataclasses and other runtime annotations resolve their defining module here.
    sys.modules[spec.name] = module
    old_flag = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise RenderError(f"Scene import failed: {exc}") from exc
    finally:
        sys.dont_write_bytecode = old_flag
        sys.path.pop(0)
    if not callable(getattr(module, "svg_frame", None)):
        raise RenderError("Scene must export a callable svg_frame(t) returning SVG text.")
    return module.svg_frame


def svg_text(frame_function, t):
    try:
        text = frame_function(t)
        if not isinstance(text, str):
            raise ValueError("svg_frame(t) must return str")
        root = ET.fromstring(text)
        if root.tag not in ("svg", "{http://www.w3.org/2000/svg}svg"):
            raise ValueError("root element must be svg")
        return text
    except Exception as exc:
        raise RenderError(f"Invalid SVG at t={t:.6f}: {exc}") from exc


def gif_info(path):
    """Read actual GIF dimensions, image count and centisecond frame delays."""
    data = Path(path).read_bytes()
    if len(data) < 14 or data[:6] not in (b"GIF87a", b"GIF89a"):
        raise RenderError(f"Encoder did not produce a valid GIF: {path}")
    width, height, flags = struct.unpack_from("<HHB", data, 6)
    position = 13 + (3 * (2 ** ((flags & 7) + 1)) if flags & 128 else 0)
    delays = []
    delay = 0
    loop_count = None

    def subblocks(offset):
        blocks = []
        while True:
            if offset >= len(data):
                raise RenderError("Truncated GIF sub-block.")
            length = data[offset]
            offset += 1
            if not length:
                return offset, blocks
            if offset + length > len(data):
                raise RenderError("Truncated GIF payload.")
            blocks.append(data[offset:offset + length])
            offset += length

    try:
        while position < len(data):
            marker = data[position]
            position += 1
            if marker == 0x3B:
                if not delays or width == 0 or height == 0:
                    raise RenderError("GIF contains no usable frames.")
                return {"width": width, "height": height, "frame_count": len(delays),
                        "duration_seconds": sum(delays) / 100,
                        "frame_delays_centiseconds": delays, "loop_count": loop_count}
            if marker == 0x21:
                label = data[position]
                position += 1
                position, blocks = subblocks(position)
                if label == 0xF9:
                    if len(blocks) != 1 or len(blocks[0]) != 4:
                        raise RenderError("Invalid GIF graphics control extension.")
                    delay = struct.unpack_from("<H", blocks[0], 1)[0]
                elif label == 0xFF and len(blocks) > 1:
                    if blocks[0] in (b"NETSCAPE2.0", b"ANIMEXTS1.0"):
                        if len(blocks[1]) >= 3 and blocks[1][0] == 1:
                            loop_count = struct.unpack_from("<H", blocks[1], 1)[0]
            elif marker == 0x2C:
                flags = data[position + 8]
                position += 9
                if flags & 128:
                    position += 3 * (2 ** ((flags & 7) + 1))
                position += 1  # LZW minimum code size.
                position, _ = subblocks(position)
                delays.append(delay)
                delay = 0
            else:
                raise RenderError(f"Unexpected GIF block: {marker:#x}")
    except (IndexError, struct.error) as exc:
        raise RenderError("Truncated GIF structure.") from exc
    raise RenderError("GIF trailer is missing.")


def encode_frames(frames, output, fps, colors, ffmpeg):
    palette = (f"[0:v]split[a][b];[a]palettegen=max_colors={colors}:stats_mode=full[p];"
               "[b][p]paletteuse=dither=none:diff_mode=rectangle")
    run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
         "-framerate", str(fps), "-i", str(frames / "frame_%04d.png"),
         "-filter_complex_threads", "1", "-filter_complex", palette,
         "-loop", "0", str(output)])


def check_output(path, overwrite):
    if path.is_symlink():
        raise RenderError(f"Refusing to replace a symbolic link: {path}")
    if path.exists() and (not overwrite or not path.is_file()):
        raise RenderError(f"Output exists: {path}. Choose a new path or use --overwrite for files.")


def publish(source, destination, overwrite):
    """Exclusive creation by default; stage then atomically replace on opt-in."""
    check_output(destination, overwrite)
    if not overwrite:
        created = False
        try:
            with destination.open("xb") as stream, source.open("rb") as incoming:
                created = True
                shutil.copyfileobj(incoming, stream)
        except Exception:
            if created:
                destination.unlink(missing_ok=True)
            raise
        return
    descriptor, temporary = tempfile.mkstemp(prefix=".animation-", dir=destination.parent)
    temporary = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream, source.open("rb") as incoming:
            shutil.copyfileobj(incoming, stream)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", required=True, help="Trusted Python scene exporting svg_frame(t)")
    parser.add_argument("--output", required=True, help="Destination .gif; adds .gif.json manifest")
    parser.add_argument("--width", type=int, default=560, help="Output width, 100..2000 pixels")
    parser.add_argument("--fps", type=int, default=10, help="3..50 fps; GIF delays have 1/100 s precision")
    parser.add_argument("--seconds", type=float, default=6, help="Loop length, 1..60 seconds")
    parser.add_argument("--colors", type=int, default=48, help="Palette budget, 4..256")
    parser.add_argument("--target-kib", type=float, help="Best-effort size budget in KiB (1024 bytes)")
    parser.add_argument("--strict-target", action="store_true", help="Exit 2 if budget unmet; keep smallest GIF")
    parser.add_argument("--keep-keyframes", action="store_true", help="Save four editable SVG keyframes")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing output, manifest and named keyframes")
    parser.add_argument("--ffmpeg", help="Exact FFmpeg executable path")
    parser.add_argument("--resvg", help="Exact resvg executable path")
    parser.add_argument("--gifsicle", help="Exact optional gifsicle executable path")
    parser.add_argument("--no-gifsicle", action="store_true", help="Disable optional optimization")
    parser.add_argument("--require-toolchain", help="Previous probe JSON or GIF manifest; stop on drift")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if sys.version_info < (3, 9):
        parser.error("Python 3.9 or newer is required; choose an existing compatible interpreter.")
    if not (100 <= args.width <= 2000 and 3 <= args.fps <= 50
            and math.isfinite(args.seconds) and 1 <= args.seconds <= 60
            and 4 <= args.colors <= 256):
        parser.error("width 100..2000; fps 3..50; seconds 1..60; colors 4..256")
    if args.target_kib is not None and (not math.isfinite(args.target_kib) or args.target_kib <= 0):
        parser.error("--target-kib must be a finite positive number")
    if args.strict_target and args.target_kib is None:
        parser.error("--strict-target requires --target-kib")
    if args.no_gifsicle and args.gifsicle:
        parser.error("--gifsicle and --no-gifsicle cannot be combined")

    scene = Path(args.scene).expanduser().resolve()
    output = Path(args.output).expanduser().absolute()
    if not scene.is_file() or scene.suffix.lower() != ".py":
        raise RenderError(f"Scene must be an existing .py file: {scene}")
    if output.suffix.lower() != ".gif":
        raise RenderError("--output must end in .gif")
    manifest_path = Path(str(output) + ".json")
    keyframe_dir = Path(str(output) + ".keyframes")
    destinations = [output, manifest_path]
    if args.keep_keyframes:
        if keyframe_dir.is_symlink() or (keyframe_dir.exists() and not keyframe_dir.is_dir()):
            raise RenderError(f"Keyframe destination must be a real directory: {keyframe_dir}")
        destinations += [keyframe_dir / f"keyframe_{number}.svg" for number in range(1, 5)]
    for destination in destinations:
        check_output(destination, args.overwrite)

    toolchain = probe_tools(ffmpeg=args.ffmpeg, resvg=args.resvg,
                            gifsicle=args.gifsicle, no_gifsicle=args.no_gifsicle)
    for warning in toolchain["warnings"]:
        print(f"Warning: {warning}", file=sys.stderr)
    if not toolchain["ok"]:
        raise RenderError("Dependency check failed:\n" + "\n".join(toolchain["errors"]))
    if args.require_toolchain:
        previous = json.loads(Path(args.require_toolchain).expanduser().read_text(encoding="utf-8"))
        if not isinstance(previous, dict):
            raise RenderError("Toolchain report must be a JSON object.")
        previous = previous.get("toolchain", previous)
        differences = compare_toolchains(toolchain, previous)
        if differences:
            raise RenderError("Toolchain changed; no scene was loaded:\n" + "\n".join(differences))

    frame_function = load_scene(scene)
    ffmpeg = toolchain["tools"]["ffmpeg"]["path"]
    resvg = toolchain["tools"]["resvg"]["path"]
    optimizer = toolchain["tools"].get("gifsicle", {})
    gifsicle = optimizer.get("path") if optimizer.get("compatible") else None
    target_bytes = args.target_kib * 1024 if args.target_kib is not None else None
    attempts, warnings = [], []
    best = None
    with tempfile.TemporaryDirectory(prefix="svg-to-gif-") as temporary:
        temporary = Path(temporary)
        best_path = temporary / "best.gif"
        for number, (width, fps, colors) in enumerate(
                make_presets(args.width, args.fps, args.colors, target_bytes is not None), 1):
            frames = temporary / "frames"
            if frames.exists():
                shutil.rmtree(frames)
            frames.mkdir()
            count = max(1, round(args.seconds * fps))
            source_svg = temporary / "frame.svg"
            for index in range(count):
                source_svg.write_text(svg_text(frame_function, index / count), encoding="utf-8")
                run([resvg, "-w", str(width), str(source_svg),
                     str(frames / f"frame_{index:04d}.png")], timeout=60)
            candidate = temporary / "candidate.gif"
            candidate.unlink(missing_ok=True)
            encode_frames(frames, candidate, fps, colors, ffmpeg)
            original_info = gif_info(candidate)
            if original_info["width"] != width:
                raise RenderError(f"Encoded GIF width {original_info['width']} differs from requested {width}.")
            optimized = False
            if gifsicle:
                optimized_path = temporary / "optimized.gif"
                optimized_path.unlink(missing_ok=True)
                try:
                    run([gifsicle, "-O3", str(candidate), "-o", str(optimized_path)])
                    optimized_info = gif_info(optimized_path)
                    # Optimization may combine duplicate frames but must preserve timing and canvas.
                    equal = all(original_info[key] == optimized_info[key] for key in
                                ("width", "height", "duration_seconds", "loop_count"))
                    if equal and optimized_path.stat().st_size < candidate.stat().st_size:
                        candidate = optimized_path
                        optimized = True
                except (RenderError, OSError) as exc:
                    warning = f"Optional gifsicle optimization skipped: {exc}"
                    warnings.append(warning)
                    print(f"Warning: {warning}", file=sys.stderr)
            info = gif_info(candidate)
            if info["duration_seconds"] <= 0 or info["loop_count"] != 0:
                raise RenderError("Encoded GIF must have positive duration and infinite looping.")
            size = candidate.stat().st_size
            attempt = {"attempt": number, "width": width, "fps": fps, "colors": colors,
                       "generated_frame_count": count, "size_bytes": size,
                       "optimized": optimized, "gif": info}
            attempts.append(attempt)
            if best is None or size < best["size_bytes"]:
                shutil.copyfile(candidate, best_path)
                best = attempt
            print(f"Attempt {number}: {width}px, {fps} fps, {colors} colors -> {size / 1024:.2f} KiB")
            if target_bytes is None or size <= target_bytes:
                break

        target_met = None if target_bytes is None else best["size_bytes"] <= target_bytes
        manifest = {"schema_version": 1,
                    "scene": {"path": str(scene), "sha256": sha256(scene)},
                    "renderer_sha256": sha256(Path(__file__)),
                    "toolchain": toolchain,
                    "requested": {"width": args.width, "fps": args.fps, "seconds": args.seconds,
                                  "colors": args.colors, "target_kib": args.target_kib,
                                  "strict_target": args.strict_target},
                    "selected": best, "attempts": attempts, "target_met": target_met,
                    "output": {"path": str(output), "sha256": sha256(best_path),
                               "size_bytes": best["size_bytes"]},
                    "warnings": warnings}
        staged_manifest = temporary / "manifest.json"
        staged_manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        files = [(best_path, output), (staged_manifest, manifest_path)]
        if args.keep_keyframes:
            for number, t in enumerate((0, .25, .5, .75), 1):
                staged = temporary / f"keyframe_{number}.svg"
                staged.write_text(svg_text(frame_function, t), encoding="utf-8")
                files.append((staged, keyframe_dir / staged.name))
        # Validate every destination again before publishing any artifact.
        for _, destination in files:
            check_output(destination, args.overwrite)
        output.parent.mkdir(parents=True, exist_ok=True)
        if args.keep_keyframes:
            keyframe_dir.mkdir(exist_ok=True)
        for staged, destination in files:
            publish(staged, destination, args.overwrite)

    print(f"Wrote: {output} ({best['size_bytes'] / 1024:.2f} KiB); manifest: {manifest_path}")
    if target_met is False:
        print("Size target unmet; retained the smallest candidate. Reduce detail, dimensions, "
              "frame rate or duration and rerun.", file=sys.stderr)
        return 2 if args.strict_target else 0
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RenderError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
