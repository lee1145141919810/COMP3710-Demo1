# COMP3710 Demo 1 — Fractals & Chaos

This repository follows **COMP3710 Lab Demonstration 1: Fractals, Version 2.31** and contains the code and documentation for all three assessed parts.

## Assessed components

1. **Part 1 (2 marks)**
   - A 2-D oriented cosine function.
   - A Gaussian multiplied by the cosine to create a Gabor filter.

2. **Part 2 (3 marks)**
   - A high-resolution zoom into Mandelbrot “Seahorse Valley”.
   - A Julia set using the student-tested constant `c = -0.4 + 0.6i`.

3. **Part 3 (10 marks)**
   - Completion of the UQ/edX **Introduction to Version Control with Git** short course (4 marks).
   - A Sierpinski carpet implemented with vectorised PyTorch tensor operations.
   - A removal-depth visualisation.
   - Box-counting analysis compared with the theoretical dimension `log(8)/log(3)`.
   - A public GitHub repository that can be shown and verified during the demonstration.

The Sierpinski carpet is mathematically different from the Mandelbrot and Julia escape-time algorithms, but its use must still be confirmed with the teaching staff as required by the lab sheet.

## Ways to run the project

### Interactive notebook

Open `COMP3710_Demo1.ipynb` in Jupyter or Google Colab and run the cells from top to bottom. The notebook keeps the main formulas, the official `ns` variable comparison, spacing calculation and live parameter exercises visible for the practical demonstration.

The notebook was prepared with AI assistance. The student must review it, run it personally and document any later changes before presenting it.

### Python script

Use a UQ lab computer, Anaconda or Google Colab with Python, PyTorch, NumPy and Matplotlib installed.

Fast CPU-friendly test:

```powershell
python demo1_fractals.py --quick
```

Full-resolution output:

```powershell
python demo1_fractals.py
```

The program selects CUDA when available and otherwise uses the CPU. It writes:

- `outputs/part1_gabor.png`
- `outputs/part2_mandelbrot_zoom.png`
- `outputs/part2_julia.png`
- `outputs/part3_sierpinski_carpet.png`
- `outputs/part3_box_counting.png`

## Key implementation choices

- The Gabor carrier can be written as `cos(2*pi*(f_x*x + f_y*y))`, where `f_x=f*cos(angle)` and `f_y=f*sin(angle)`.
- The lab sheet's Mandelbrot `ns` variable corresponds conceptually to this project's integer `counts`: both accumulate how many iterations each pixel remains unescaped.
- The Mandelbrot implementation uses canonical `z_0=0`; the Julia implementation varies `z_0` per pixel and holds `c` fixed.
- Increasing `width/height` decreases the effective `linspace` spacing. Narrowing the coordinate bounds performs the actual complex-plane zoom.
- The Sierpinski implementation loops over fractal levels but processes every pixel at each level with tensor remainder and Boolean-mask operations.

More detailed explanations and likely questions are in `DEMO_NOTES_CN.md`.

## Verification

On 17 August 2026, both the quick and full commands completed successfully in a clean CPU environment using PyTorch 2.13.0. They generated all five expected images and measured a box-counting dimension of `1.892789`, matching `log(8)/log(3)`. See `VERIFICATION_REPORT.md`.

The student later ran quick mode personally, changed the Julia constant from `-0.8 + 0.156i` to `-0.4 + 0.6i`, and compared the original and updated images. The original remains at `outputs/part2_julia_original.png`.

## Before the marked practical

- [ ] Obtain and retain teaching-staff approval for the Sierpinski carpet.
- [ ] Be ready to show completion of the Git Introduction short course.
- [ ] Personally run the notebook or script from start to finish on the intended machine.
- [ ] Personally change and record at least one Mandelbrot zoom or spacing experiment.
- [ ] Open all five generated images and explain what each one demonstrates.
- [ ] Keep GitHub logged in and be ready to show the repository and commit history.
- [ ] Keep the repository public for demonstrator access.
- [ ] Review `AI_USAGE_LOG.md`, add every later AI interaction and retain original prompt evidence or a shareable conversation history.
- [ ] Practise a three-minute summary and live changes to Gabor frequency, Mandelbrot bounds, Julia `c` and Sierpinski level.
- [ ] Confirm with the teaching staff whether an explicit open-source licence is required; no licence should be selected without understanding its terms.

Do not present code or documentation that you have not personally reviewed and cannot explain.
