"""Render a 3-D turntable-spin GIF of the bimodal trough.

Uses OpenSCAD's headless renderer to draw the parametric model from
``cad/bimodal_trough.scad`` at a sequence of azimuth angles, then stitches
the frames together with Pillow into ``cad/bimodal-trough-spin.gif``.

Run from the repository root::

    sudo apt-get install -y openscad      # one-time, ~80 MB
    python -m scripts.render_trough_spin

Output:
    cad/bimodal-trough-spin.gif   # 360° turntable, default 60 frames @ 20 fps
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


def _openscad_command() -> list[str]:
    """Return the command prefix for invoking OpenSCAD.

    OpenSCAD's ``-o file.png`` mode still spins up a GL context, so on
    headless CI runners (no ``$DISPLAY``) it segfaults on launch. If we
    detect a headless environment and ``xvfb-run`` is available, transparently
    wrap the call.
    """
    cmd = ["openscad"]
    if not os.environ.get("DISPLAY") and shutil.which("xvfb-run"):
        cmd = ["xvfb-run", "-a", "--server-args=-screen 0 1024x768x24"] + cmd
    return cmd


REPO_ROOT = Path(__file__).resolve().parent.parent
SCAD_SOURCE = REPO_ROOT / "cad" / "bimodal_trough.scad"
DEFAULT_OUTPUT = REPO_ROOT / "cad" / "bimodal-trough-spin.gif"


def render_frame(
    azimuth_deg: float,
    output_path: Path,
    *,
    width: int,
    height: int,
    elevation_deg: float,
    distance: float,
) -> None:
    """Render a single OpenSCAD PNG frame at the requested camera azimuth.

    The OpenSCAD camera vector is
    ``tx,ty,tz, rot_x,rot_y,rot_z, distance``. We hold the translation,
    elevation (``rot_x``) and distance fixed, and sweep ``rot_z`` to
    produce a turntable spin around the model's vertical axis.
    """
    camera = f"0,0,8,{elevation_deg},0,{azimuth_deg},{distance}"
    cmd = _openscad_command() + [
        "-o",
        str(output_path),
        f"--imgsize={width},{height}",
        f"--camera={camera}",
        "--colorscheme=Tomorrow",
        "--projection=perspective",
        str(SCAD_SOURCE),
    ]
    result = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not output_path.exists():
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError(
            f"openscad failed for azimuth={azimuth_deg:.1f}°"
            f" (exit={result.returncode})"
        )


def build_gif(
    output_path: Path = DEFAULT_OUTPUT,
    *,
    frames: int = 60,
    fps: int = 20,
    width: int = 700,
    height: int = 520,
    elevation_deg: float = 60.0,
    distance: float = 200.0,
) -> Path:
    """Render ``frames`` OpenSCAD PNGs and stitch them into a looped GIF."""
    if shutil.which("openscad") is None:
        raise RuntimeError(
            "openscad not found on PATH. Install it first: "
            "sudo apt-get install -y openscad"
        )
    if not os.environ.get("DISPLAY") and shutil.which("xvfb-run") is None:
        raise RuntimeError(
            "Headless environment detected but xvfb-run is not installed. "
            "Install it with: sudo apt-get install -y xvfb"
        )
    if not SCAD_SOURCE.exists():
        raise FileNotFoundError(f"OpenSCAD source not found: {SCAD_SOURCE}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    images: list[Image.Image] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for i in range(frames):
            azimuth = 360.0 * i / frames
            frame_path = tmp_dir / f"frame_{i:03d}.png"
            render_frame(
                azimuth,
                frame_path,
                width=width,
                height=height,
                elevation_deg=elevation_deg,
                distance=distance,
            )
            # Quantise to a 256-colour palette so the GIF stays small while
            # keeping smooth shading. ``MEDIANCUT`` picks a palette that
            # minimises perceived error on this kind of low-saturation render;
            # ``Image.Dither.FLOYDSTEINBERG`` smooths the gradients.
            img = Image.open(frame_path).convert("RGB")
            images.append(
                img.quantize(
                    colors=256,
                    method=Image.Quantize.MEDIANCUT,
                    dither=Image.Dither.FLOYDSTEINBERG,
                )
            )
            print(f"  frame {i + 1:3d}/{frames}  azimuth={azimuth:6.1f}°")

    duration_ms = max(1, round(1000.0 / fps))
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration_ms,
        loop=0,
        optimize=False,
        disposal=2,
    )
    print(f"Wrote {output_path} ({output_path.stat().st_size // 1024} KiB)")
    return output_path


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output GIF path (default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--frames", type=int, default=60, help="number of frames (default: 60)"
    )
    parser.add_argument(
        "--fps", type=int, default=20, help="playback frames per second (default: 20)"
    )
    parser.add_argument(
        "--width", type=int, default=700, help="frame width in px (default: 700)"
    )
    parser.add_argument(
        "--height", type=int, default=520, help="frame height in px (default: 520)"
    )
    parser.add_argument(
        "--elevation",
        type=float,
        default=60.0,
        dest="elevation_deg",
        help="camera tilt (rot_x) in degrees (default: 60)",
    )
    parser.add_argument(
        "--distance",
        type=float,
        default=200.0,
        help="camera distance from the model (default: 200)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    build_gif(
        output_path=args.output,
        frames=args.frames,
        fps=args.fps,
        width=args.width,
        height=args.height,
        elevation_deg=args.elevation_deg,
        distance=args.distance,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
