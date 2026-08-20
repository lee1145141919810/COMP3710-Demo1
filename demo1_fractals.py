"""COMP3710 Demo 1: Fractals & Chaos.

This script covers the three assessed coding demonstrations:
  1. A 2-D Gaussian, an oriented sinusoid, and their Gabor modulation.
  2. A high-resolution Mandelbrot zoom and a Julia set.
  3. A vectorised PyTorch Sierpinski carpet plus box-counting analysis.

The code intentionally keeps the mathematics visible so it can be explained
during the practical demonstration.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch


OUTPUT_DIR = Path(__file__).with_name("outputs")


def choose_device() -> torch.device:
    """Use a GPU when one is available, otherwise fall back to the CPU."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def coordinate_grid(
    x_limits: tuple[float, float],
    y_limits: tuple[float, float],
    width: int,
    height: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return x/y coordinate tensors with one coordinate pair per pixel."""
    xs = torch.linspace(x_limits[0], x_limits[1], width, device=device)
    ys = torch.linspace(y_limits[0], y_limits[1], height, device=device)
    y, x = torch.meshgrid(ys, xs, indexing="ij")
    return x, y


def save_three_panel_figure(
    arrays: list[np.ndarray],
    titles: list[str],
    output_path: Path,
    colour_maps: list[str],
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), constrained_layout=True)
    for axis, array, title, colour_map in zip(
        axes, arrays, titles, colour_maps, strict=True
    ):
        image = axis.imshow(array, cmap=colour_map, origin="lower")
        axis.set_title(title)
        axis.set_axis_off()
        fig.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


@torch.no_grad()
def part1_gabor(device: torch.device, quick: bool = False) -> None:
    """Create the Gaussian, sinusoidal grating, and Gabor filter."""
    resolution = 450 if quick else 800
    x, y = coordinate_grid((-4.0, 4.0), (-4.0, 4.0), resolution, resolution, device)

    sigma = 1.25
    gaussian = torch.exp(-(x.square() + y.square()) / (2.0 * sigma**2))

    angle = math.radians(30.0)
    frequency = 0.75  # cycles per coordinate unit

    # Equivalent frequency-vector form: cos(2*pi*(f_x*x + f_y*y)).
    # The vector magnitude controls stripe density; its direction is normal
    # to the visible stripes.
    f_x = frequency * math.cos(angle)
    f_y = frequency * math.sin(angle)
    sinusoid = torch.cos(2.0 * math.pi * (f_x * x + f_y * y))

    # Modulation: multiplying a Gaussian envelope by a sinusoidal carrier.
    gabor = gaussian * sinusoid

    save_three_panel_figure(
        [
            gaussian.cpu().numpy(),
            sinusoid.cpu().numpy(),
            gabor.cpu().numpy(),
        ],
        ["2-D Gaussian", "2-D oriented cosine", "Gaussian × cosine (Gabor)"],
        OUTPUT_DIR / "part1_gabor.png",
        ["viridis", "coolwarm", "coolwarm"],
    )


@torch.no_grad()
def escape_counts(
    initial_z: torch.Tensor,
    constant_c: torch.Tensor,
    max_iterations: int,
) -> torch.Tensor:
    """Count bounded iterations of z <- z^2 + c for every pixel in parallel."""
    z = initial_z.clone()
    counts = torch.zeros(z.shape, dtype=torch.int32, device=z.device)
    active = torch.ones(z.shape, dtype=torch.bool, device=z.device)

    for _ in range(max_iterations):
        # Freeze escaped states so they do not keep growing towards infinity.
        # candidate is still evaluated for the whole tensor before torch.where.
        candidate = z.square() + constant_c
        z = torch.where(active, candidate, z)
        active = active & (z.abs() <= 2.0)
        counts += active

        if not bool(active.any()):
            break

    return counts


def save_escape_time_figure(
    counts: torch.Tensor,
    max_iterations: int,
    extent: tuple[float, float, float, float],
    title: str,
    output_path: Path,
) -> None:
    values = counts.cpu().numpy().astype(np.float32)
    values[values >= max_iterations] = np.nan
    colour_map = plt.colormaps["turbo"].copy()
    colour_map.set_bad("black")

    fig, axis = plt.subplots(figsize=(10, 7), constrained_layout=True)
    image = axis.imshow(
        values,
        cmap=colour_map,
        origin="lower",
        extent=extent,
        interpolation="bilinear",
    )
    axis.set_title(title)
    axis.set_xlabel("Real axis")
    axis.set_ylabel("Imaginary axis")
    fig.colorbar(image, ax=axis, label="Iterations before escape")
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


@torch.no_grad()
def part2_mandelbrot_and_julia(device: torch.device, quick: bool = False) -> None:
    """Render one Mandelbrot zoom and one Julia set."""
    if quick:
        mandelbrot_width, mandelbrot_height, mandelbrot_iterations = 650, 450, 180
        julia_width, julia_height, julia_iterations = 600, 450, 180
    else:
        mandelbrot_width, mandelbrot_height, mandelbrot_iterations = 1400, 1000, 420
        julia_width, julia_height, julia_iterations = 1200, 900, 320

    # Seahorse Valley: a detailed region that visibly demonstrates zooming.
    mandelbrot_x = (-0.82, -0.72)
    mandelbrot_y = (0.02, 0.12)
    x, y = coordinate_grid(
        mandelbrot_x,
        mandelbrot_y,
        mandelbrot_width,
        mandelbrot_height,
        device,
    )
    c = torch.complex(x, y)
    mandelbrot = escape_counts(torch.zeros_like(c), c, mandelbrot_iterations)
    save_escape_time_figure(
        mandelbrot,
        mandelbrot_iterations,
        (*mandelbrot_x, *mandelbrot_y),
        "Mandelbrot set — high-resolution Seahorse Valley zoom",
        OUTPUT_DIR / "part2_mandelbrot_zoom.png",
    )

    # For a Julia set, each pixel is z_0 and the same c is used everywhere.
    julia_x = (-1.7, 1.7)
    julia_y = (-1.25, 1.25)
    x, y = coordinate_grid(julia_x, julia_y, julia_width, julia_height, device)
    initial_z = torch.complex(x, y)
    julia_constant = torch.tensor(-0.4 + 0.6j, dtype=torch.complex64, device=device)
    julia = escape_counts(initial_z, julia_constant, julia_iterations)
    save_escape_time_figure(
        julia,
        julia_iterations,
        (*julia_x, *julia_y),
        "Julia set for c = -0.4 + 0.6i",
        OUTPUT_DIR / "part2_julia.png",
    )


@torch.no_grad()
def sierpinski_carpet(
    level: int, device: torch.device
) -> tuple[torch.Tensor, torch.Tensor]:
    """Build a Sierpinski carpet with vectorised tensor operations.

    Each base-3 digit position is checked simultaneously for every image pixel.
    A pixel is removed when both its x and y digit are 1 at any level.
    """
    size = 3**level
    coordinates = torch.arange(size, device=device, dtype=torch.int64)
    y, x = torch.meshgrid(coordinates, coordinates, indexing="ij")

    active = torch.ones((size, size), dtype=torch.bool, device=device)
    removal_depth = torch.zeros((size, size), dtype=torch.int16, device=device)
    working_x = x.clone()
    working_y = y.clone()

    for step in range(1, level + 1):
        removed_now = active & (working_x.remainder(3) == 1) & (
            working_y.remainder(3) == 1
        )
        removal_depth[removed_now] = step
        active &= ~removed_now
        working_x.div_(3, rounding_mode="floor")
        working_y.div_(3, rounding_mode="floor")

    removal_depth[active] = level + 1
    return active, removal_depth


@torch.no_grad()
def box_counting_dimension(mask: torch.Tensor, level: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Estimate fractal dimension by counting occupied boxes at several scales."""
    size = mask.shape[0]
    box_sizes = np.array([3**power for power in range(level)], dtype=np.int64)
    counts: list[int] = []

    for box_size in box_sizes:
        boxes_per_side = size // int(box_size)
        blocks = mask.reshape(
            boxes_per_side,
            int(box_size),
            boxes_per_side,
            int(box_size),
        )
        occupied = blocks.any(dim=3).any(dim=1)
        counts.append(int(occupied.sum().item()))

    counts_array = np.array(counts, dtype=np.float64)
    inverse_scales = size / box_sizes.astype(np.float64)
    estimated_dimension = float(
        np.polyfit(np.log(inverse_scales), np.log(counts_array), deg=1)[0]
    )
    return inverse_scales, counts_array, estimated_dimension


@torch.no_grad()
def part3_sierpinski(device: torch.device, level: int) -> None:
    """Render and analyse a vectorised PyTorch Sierpinski carpet."""
    carpet, removal_depth = sierpinski_carpet(level, device)
    inverse_scales, counts, estimated_dimension = box_counting_dimension(carpet, level)
    theoretical_dimension = math.log(8.0) / math.log(3.0)

    carpet_cpu = carpet.cpu().numpy()
    depth_cpu = removal_depth.cpu().numpy()

    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)
    axes[0].imshow(carpet_cpu, cmap="gray", origin="lower", interpolation="nearest")
    axes[0].set_title(f"Sierpinski carpet, level {level}")
    axes[0].set_axis_off()

    depth_image = axes[1].imshow(
        depth_cpu,
        cmap="magma",
        origin="lower",
        interpolation="nearest",
    )
    axes[1].set_title("Removal depth visualisation")
    axes[1].set_axis_off()
    fig.colorbar(depth_image, ax=axes[1], label="Iteration removed (survivors last)")
    fig.savefig(OUTPUT_DIR / "part3_sierpinski_carpet.png", dpi=200)
    plt.close(fig)

    log_scale = np.log(inverse_scales)
    log_count = np.log(counts)
    fitted = np.polyval(np.polyfit(log_scale, log_count, deg=1), log_scale)

    fig, axis = plt.subplots(figsize=(7, 5), constrained_layout=True)
    axis.scatter(log_scale, log_count, label="Measured box counts")
    axis.plot(log_scale, fitted, label=f"Fit: dimension = {estimated_dimension:.4f}")
    axis.set_xlabel("log(1 / box scale)")
    axis.set_ylabel("log(occupied boxes)")
    axis.set_title("Box-counting dimension of the Sierpinski carpet")
    axis.legend()
    axis.grid(alpha=0.25)
    fig.savefig(OUTPUT_DIR / "part3_box_counting.png", dpi=200)
    plt.close(fig)

    print(f"Measured box-counting dimension: {estimated_dimension:.6f}")
    print(f"Theoretical dimension log(8)/log(3): {theoretical_dimension:.6f}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="COMP3710 Demo 1 fractal demonstrations")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Use smaller images for a fast first run on a CPU.",
    )
    parser.add_argument(
        "--level",
        type=int,
        default=7,
        help="Sierpinski carpet level (default: 7; quick mode caps this at 6).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    level = min(args.level, 6) if args.quick else args.level
    if not 2 <= level <= 7:
        raise ValueError("Choose a Sierpinski level between 2 and 7.")

    OUTPUT_DIR.mkdir(exist_ok=True)
    device = choose_device()
    print(f"PyTorch version: {torch.__version__}")
    print(f"Computation device: {device}")

    part1_gabor(device, quick=args.quick)
    part2_mandelbrot_and_julia(device, quick=args.quick)
    part3_sierpinski(device, level)
    print(f"Finished. Images saved in: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
