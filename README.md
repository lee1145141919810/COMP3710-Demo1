# COMP3710 Demo 1 — Fractals & Chaos

This project follows the **Demo 1 Sheet v2.31 (3 August 2026)** and produces all five coding demonstrations needed for Parts 1–3.

## What the script demonstrates

1. **Part 1 (2 marks)**
   - A 2-D oriented cosine function.
   - A Gaussian multiplied by the cosine to create a Gabor filter.

2. **Part 2 (3 marks)**
   - A high-resolution zoom into Mandelbrot “Seahorse Valley”.
   - A Julia set using the constant `c = -0.8 + 0.156i`.

3. **Part 3 coding component (6 marks)**
   - A Sierpinski carpet implemented with vectorised PyTorch tensor operations.
   - A second colour visualisation showing the iteration at which pixels are removed.
   - Numerical box-counting analysis compared with the theoretical dimension `log(8)/log(3)`.

The remaining **4 marks** in Part 3 come from personally completing the UQ/edX **Introduction to Version Control with Git** short course.

## Run it

Use a UQ lab computer, Anaconda, or Google Colab with Python, PyTorch, NumPy and Matplotlib installed.

For a fast first test:

```powershell
python demo1_fractals.py --quick
```

For the full-resolution demonstration:

```powershell
python demo1_fractals.py
```

The program automatically uses a CUDA GPU when available and otherwise uses the CPU. It saves the following images in the `outputs` folder:

- `part1_gabor.png`
- `part2_mandelbrot_zoom.png`
- `part2_julia.png`
- `part3_sierpinski_carpet.png`
- `part3_box_counting.png`

## Before the marked practical

- Run the quick version first and open every generated image.
- Run the full version on a GPU-equipped lab computer.
- Confirm the Sierpinski carpet choice with the demonstrator if they require prior approval. It is deliberately different from the Mandelbrot and Julia sets.
- Complete the Git short course yourself.
- Create your own GitHub repository, commit this project in several meaningful stages, and push it.
- Update `AI_USAGE_LOG.md` with any new AI prompts or changes you make.
- Practise the explanations in `DEMO_NOTES_CN.md`; do not present code you cannot explain.

## Suggested meaningful Git commits

1. `Add Gaussian, sinusoid and Gabor demonstration`
2. `Add Mandelbrot zoom and Julia set`
3. `Add vectorised Sierpinski carpet`
4. `Add box-counting dimension analysis and documentation`

Do not make all changes in one final commit; the repository history is part of showing reasonable effort.
