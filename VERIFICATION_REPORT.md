# COMP3710 Demo 1 Verification Report

Verification date: 17 August 2026 (Australia/Brisbane)

This report first records the AI-assisted verification of the original Julia
constant `-0.8 + 0.156i`. A later student-run experiment is recorded at the end.

## Environment

- Python 3.12
- PyTorch 2.13.0
- NumPy 2.5.2
- Matplotlib 3.11.1
- Device selected by the program: CPU

Dependencies were installed from `requirements.txt` into an isolated local
virtual environment. The environment itself is excluded from the repository.

## Commands checked

```text
python demo1_fractals.py --quick
python demo1_fractals.py
```

Both commands exited successfully. The full run reported:

```text
PyTorch version: 2.13.0
Computation device: cpu
Measured box-counting dimension: 1.892789
Theoretical dimension log(8)/log(3): 1.892789
```

## Output checks

All five expected files were generated and opened for visual inspection:

| File | Full-run pixel size | Check |
| --- | ---: | --- |
| `part1_gabor.png` | 2700 × 828 | Gaussian, oriented cosine, and modulated Gabor panels are visible |
| `part2_mandelbrot_zoom.png` | 2000 × 1400 | Seahorse Valley boundary detail is visible |
| `part2_julia.png` | 2000 × 1400 | Julia-set structure for `c = -0.8 + 0.156i` is visible |
| `part3_sierpinski_carpet.png` | 2600 × 1200 | Binary carpet and removal-depth visualisation are visible |
| `part3_box_counting.png` | 1400 × 1000 | Measured points and fitted dimension `1.8928` are visible |

## Remaining student-owned checks

- Personally complete and be able to demonstrate the Git short course requirement.
- Confirm the Sierpinski carpet choice with teaching staff if prior approval is required.
- Try and explain at least one changed Julia constant and Mandelbrot zoom.
- Practise answering the questions in `DEMO_NOTES_CN.md` without reading a script.
- Make the GitHub repository public if teaching staff require an open-source repository.
- Add any later AI prompts and personal experiments to `AI_USAGE_LOG.md`.

## Subsequent student-run experiment

The student personally ran quick mode, opened the generated images, changed the
Julia constant and plot title to `-0.4 + 0.6i`, and ran quick mode again. The
updated Julia image was generated successfully. It changed from a relatively
continuous spiral-like structure into disconnected, centrally symmetric
island-like clusters. The original image is retained as
`outputs/part2_julia_original.png` for direct comparison.
