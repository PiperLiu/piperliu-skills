# Dependency setup and version handling

## Inspect, then decide

The runtime uses Python 3.9+ standard library, resvg's command-line SVG renderer, and FFmpeg with PNG input, `palettegen`, `paletteuse`, and GIF output. gifsicle `-O3` is optional. No Python virtual environment is necessary for these scripts; a venv isolates Python packages, not native FFmpeg/resvg executables.

Run `animation_tools.py` with the chosen interpreter. It uses PATH only for unspecified tools and tests the selected executable paths. An explicit broken path must not silently fall back to another installation. It writes only temporary probe files unless a report destination is requested.

| Finding | Action |
| --- | --- |
| Existing tools pass capability checks | Reuse them, including older versions. |
| Version string is unusual but actual probe passes | Record the raw version and hash; no upgrade needed for this workflow. |
| Required tool missing or incompatible | Explain the concrete missing capability and offer a specific isolated install or a user-provided executable. |
| Optional gifsicle absent or broken | Continue without it and report the omission. |
| Toolchain differs from a previous render | Show the changed paths/versions/hashes. Reuse the old binaries if available, or obtain authorization for any installation. Accepting a new baseline does not authorize replacing software. |
| User declines installation | Finish editable scene/assets and SVG keyframes where possible; clearly state that a GIF was not rendered. Do not substitute an unrelated backend silently. |

Example consent request: “The selected FFmpeg cannot run palettegen. May I place version X for your OS/architecture in `<project>/.tools/ffmpeg/X/` and invoke it by absolute path? Your existing FFmpeg and PATH will remain untouched.” Replace X with a verified available release and show its source and installation footprint. If the user requests standard-path installation, explain that scope and check for collisions before writing there. Do not repeat consent already granted for the same action.

## Installation choices after authorization

Prefer an existing compatible installation. Otherwise, prefer unpacking a verified release into a versioned project/user tool directory and passing its full path. Verify OS, architecture, dynamic-library requirements, archive content, and publisher checksums/signatures where provided. Record the source URL, archive digest, executable digest, version, and destination in a local setup record. A locally calculated digest alone records identity; it does not authenticate a download.

| Platform | Isolated approach | Broader approach only if requested/approved |
| --- | --- | --- |
| macOS | Matching resvg release binary; compatible FFmpeg build from a source linked by FFmpeg; keep versioned directories. | A package manager already in use, or a user executable directory already on PATH. |
| Linux | Compatible release/archive for CPU and libc; explicitly invoke the unpacked binary. | The distribution package manager, after reviewing dependency changes and privilege requirements. |
| Windows | Matching native executable/archive in a versioned directory; use quoted full `.exe` paths. | An approved installer/package manager; review PATH, file associations, and existing-install effects. |

Release assets differ across versions and architectures. Verify the current upstream listing; do not invent download URLs or force a source build that brings in Rust/other toolchains without authorization. If Python itself is missing, choose an official supported runtime with the user and leave the operating system's Python in place. The code's 3.9 compatibility floor is not a recommendation to install an unsupported Python release.

Do not run blanket commands such as `brew upgrade`, `apt upgrade`, `winget upgrade --all`, or `pip install --upgrade` for this skill. Even a targeted package-manager install can update shared dependencies; review its plan and obtain authorization for that scope. Scripts intentionally contain no installer or updater.

Official starting points:

- [Python downloads](https://www.python.org/downloads/)
- [resvg releases](https://github.com/linebender/resvg/releases) and [supported static SVG subset](https://github.com/linebender/resvg)
- [FFmpeg downloads and platform build links](https://ffmpeg.org/download.html); FFmpeg itself distributes source and links to external compiled builds.
- [FFmpeg palette filters](https://ffmpeg.org/ffmpeg-filters.html#palettegen-1)
- [gifsicle](https://www.lcdf.org/gifsicle/)
- [Python venv scope](https://docs.python.org/3/library/venv.html)

## Reproduction and drift

Retain the render JSON with the editable scene and source assets. `--require-toolchain previous.gif.json` requires the selected tools to match the recorded identities before importing the scene. It checks identity, not a floating “latest” requirement. The same binary can still behave differently if fonts, linked libraries, OS, or inputs change; preserve those separately when strict reproduction matters. Absolute paths and host information in reports are local provenance: review/redact before sharing publicly, and do not commit machine-specific reports or downloaded executables into the skill repository.

To adopt a different tool version, install it alongside the old version only with authorization, select it explicitly, render to a new output, inspect the differences, and keep its new report. Do not rewrite an earlier report to make a mismatch disappear.
