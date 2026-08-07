# AI Usage Log

The Demo 1 sheet permits AI assistance, but requires prompts, outputs/reasoning and later modifications to be documented. Keep this file accurate and add every further AI interaction used for the project.

## Session 1 — 7 August 2026

### Prompt 1 (student, original wording)

> COMP3710 Fractals & Chaos Demo 的要求做这个

### Context provided to the AI

The COMP3710 Demo 1 Sheet v2.31 was opened in Learn.UQ. The assessed requirements were:

- generate a 2-D sine/cosine and multiply it by a Gaussian;
- render a higher-resolution Mandelbrot zoom and modify the algorithm into a Julia set;
- implement a substantially different fractal with PyTorch/TF/JAX, publish it in the student's GitHub repository, and explain its parallel implementation;
- document all AI prompts and add substantial analysis if AI is used.

### AI output and reasoning summary

The AI proposed one readable Python script containing all three parts. It selected a Sierpinski carpet for Part 3 because its construction is substantially different from the complex-plane escape-time algorithm used by Mandelbrot/Julia sets. The image is computed with vectorised PyTorch tensor masks so all pixel coordinates can be processed in parallel on a GPU.

The AI added box-counting dimension analysis so the project goes beyond producing a single AI-generated picture. The measured slope is compared with the known theoretical dimension `log(8)/log(3) ≈ 1.8928`. It also added a removal-depth colour visualisation.

### Important implementation choices/modifications

- Replaced Python pixel-by-pixel loops with PyTorch coordinate tensors.
- Added CPU fallback while preferring a CUDA GPU.
- Used an active mask in Mandelbrot/Julia iteration to stop updating escaped points and reduce overflow/unnecessary work.
- Used a zoomed Mandelbrot region instead of only regenerating the full standard view.
- Made the key parameters explicit: image size, bounds, maximum iterations, Julia constant, Gabor orientation/frequency and Sierpinski level.
- Added `--quick` for testing on a CPU and full resolution for the marked demonstration.

### Runtime verification completed in Google Colab

- Environment: Google Colab, PyTorch `2.11.0+cpu`.
- The quick test and the full-resolution command both completed without errors.
- All five output images were generated and visually inspected: Gaussian/cosine/Gabor, Julia set, Mandelbrot zoom, Sierpinski carpet/removal-depth view, and box-counting graph.
- Measured box-counting dimension: `1.892789`.
- Theoretical dimension `log(8)/log(3)`: `1.892789`.
- The Colab notebook was saved as `COMP3710_Demo1.ipynb` in the student's Google Drive. It was not submitted to Learn.UQ or uploaded to GitHub.

## Course-suggested prompt sequence reproduced in this project

### Prompt 2

> Generate a Python script to plot a 2D Gaussian function using NumPy and Matplotlib.

Result: a coordinate grid is created and the Gaussian `exp(-(x²+y²)/(2σ²))` is evaluated over the whole grid before plotting.

### Prompt 3

> Convert this script to PyTorch and use tensors instead of NumPy for the computation. Use a GPU when available.

Result: the grid and formulas use PyTorch tensors on `cuda` or `cpu`; the result is moved back with `.cpu().numpy()` only for Matplotlib.

### Prompt 4

> Change the function into an oriented 2D sine or cosine, then multiply it by the Gaussian and explain the result.

Result: the script creates an oriented cosine carrier and multiplies it by the Gaussian envelope. The output is a Gabor filter.

### Prompt 5

> Modify the PyTorch Mandelbrot implementation to produce a Julia set and explain the mathematical difference.

Result: Mandelbrot fixes `z₀ = 0` and varies `c` per pixel; Julia varies `z₀` per pixel and fixes one complex `c` for the whole image.

## Student verification record — complete before demonstration

- [ ] I ran `python demo1_fractals.py --quick` myself.
- [ ] I ran the full-resolution version and inspected all five images.
- [ ] I can explain every formula and the tensor shapes.
- [ ] I tried at least one different Julia constant and recorded the result below.
- [ ] I tried at least one different Mandelbrot zoom and recorded the bounds below.
- [ ] I confirmed the Part 3 fractal choice with teaching staff if required.
- [ ] I added all later AI prompts and changes to this log.

### My own experiments

- Julia constant tested:
- What changed:
- Mandelbrot bounds tested:
- What changed:
- Other code changes I made:

## Session 2 — 7 August 2026

### Prompt 6 (student, original wording)

> 帮我

### Context and AI assistance

The student asked for help creating the GitHub repository for the COMP3710 Demo 1 project after personally completing the Git short course. The AI prepared and, after explicit confirmation, created the empty private repository `lee1145141919810/COMP3710-Demo1`. It also added a `.gitignore` so Python cache and local virtual-environment files are not committed.

The repository was intentionally created without a GitHub-generated README, licence, or `.gitignore` because the local project already contains its own README and documentation. The student still needs to initialise the local repository, review the files, create meaningful commits, push them, and be able to explain all submitted code.
