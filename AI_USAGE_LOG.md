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

- [x] I ran `python demo1_fractals.py --quick` myself.
- [ ] I ran the full-resolution version and inspected all five images.
- [ ] I can explain every formula and the tensor shapes.
- [x] I tried at least one different Julia constant and recorded the result below.
- [ ] I tried at least one different Mandelbrot zoom and recorded the bounds below.
- [ ] I confirmed the Part 3 fractal choice with teaching staff if required.
- [ ] I added all later AI prompts and changes to this log.

### My own experiments

- Julia constant tested: changed from `-0.8 + 0.156i` to `-0.4 + 0.6i`.
- What changed: the relatively continuous, curled and spiral-like structure
  became several disconnected island-like clusters. The branches did not
  become finer; they became more compact and fragmented. The new image has no
  single central body: two major clusters lie on opposite sides of the origin,
  with smaller repeated clusters. Both versions retain approximately 180-degree
  rotational symmetry about the origin.
- Mandelbrot bounds tested:
- What changed:
- Other code changes I made: updated both the Julia constant and the plot title,
  ran quick mode personally, opened the generated images, and compared the new
  Julia image with the saved original.

## Session 2 — 7 August 2026

### Prompt 6 (student, original wording)

> 帮我

### Context and AI assistance

The student asked for help creating the GitHub repository for the COMP3710 Demo 1 project after personally completing the Git short course. The AI prepared and, after explicit confirmation, created the empty private repository `lee1145141919810/COMP3710-Demo1`. It also added a `.gitignore` so Python cache and local virtual-environment files are not committed.

The repository was intentionally created without a GitHub-generated README, licence, or `.gitignore` because the local project already contains its own README and documentation. The student still needs to initialise the local repository, review the files, create meaningful commits, push them, and be able to explain all submitted code.

### Later status clarification

The final sentence above described the repository immediately after creation.
It is no longer current: by 17 August 2026, the repository contained three
meaningful commits, including the fractal implementation, demonstration notes,
and AI-assistance documentation. The repository was still private at the time
of verification, so it must be made public before the marked practical if the
task requires an open-source repository visible to teaching staff.

## Session 3 — 17 August 2026

### Prompt 7 (student, original wording)

> 我已经提交了 接下来带着我做完其他的

### Context and AI assistance

The AI opened the current COMP3710 Demo 1 sheet and marking rubric in Learn.UQ,
inspected the student's existing private GitHub repository, downloaded a ZIP
copy, installed the declared dependencies in an isolated local environment,
and ran both the quick and full-resolution commands. The AI also inspected all
five generated images and compared the implementation and documentation with
the rubric.

### Independent verification result

- Environment: macOS ARM64, Python 3.12, PyTorch 2.13.0, CPU.
- `python demo1_fractals.py --quick`: completed successfully.
- `python demo1_fractals.py`: completed successfully.
- Five expected PNG files were generated and visually inspected.
- Measured box-counting dimension: `1.892789`.
- Theoretical dimension `log(8)/log(3)`: `1.892789`.
- No teaching-system submission, repository visibility change, commit, or push
  was performed during this verification.

### Documentation changes suggested by the AI

- Add a reproducible verification report.
- Clarify that the three repository commits already exist.
- Note that the repository is currently private and must be made public if the
  open-source requirement applies.
- Keep student-only checklist items unchecked until the student personally
  completes and can explain them.

## Session 4 — 17 August 2026

### Student-run Julia experiment

### Related student prompts (original wording)

> 我该怎么做

> 我忘记原先的图长啥样了

The AI responded with exact terminal commands for running quick mode, opening
the generated files, preserving the original Julia image, and changing the
Julia constant and matching plot title. The student executed the commands and
made the parameter change personally.

The student personally ran:

```text
MPLBACKEND=Agg MPLCONFIGDIR=.mplconfig .venv/bin/python demo1_fractals.py --quick
open outputs/*.png
```

The run completed successfully using PyTorch 2.13.0 on the CPU and again
reported a measured and theoretical box-counting dimension of `1.892789`.

The student then changed the Julia constant and matching plot title from
`-0.8 + 0.156i` to `-0.4 + 0.6i`, reran quick mode, and compared the images.

### Student observation (original wording)

> 整体并不连接,分支并没有更细,对称性和中心形状,我看看,都是关于中心对称,中心形状,我不知道怎么描述。

### Refined description after image comparison

The new Julia set is disconnected and consists of multiple island-like
clusters. Its structures are more compact and fragmented rather than finer.
There is no single central body; instead, two large clusters appear on opposite
sides of the origin, accompanied by smaller repeated clusters. Both versions
show approximately 180-degree rotational symmetry about the origin.

The AI compared the two rendered images and checked the orbit of `z_0 = 0` for
`c = -0.4 + 0.6i`. The orbit escaped after 26 iterations, consistent with this
parameter lying outside the Mandelbrot set and therefore producing a
disconnected Julia set. The 180-degree rotational symmetry follows because
`z` and `-z` have the same square in the iteration `z_(n+1) = z_n^2 + c`.

## Session 5 — 17 August 2026

### Pre-publication validation performed by the AI

Before preparing the GitHub update, the AI compiled the updated script and ran
the full-resolution command with `c = -0.4 + 0.6i`. The command completed on
the CPU, regenerated all five current output images, and again reported a
measured and theoretical box-counting dimension of `1.892789`. The original
Julia image remains preserved as `outputs/part2_julia_original.png`. This was
an AI-operated publication check and is not presented as a student-run test.

## Session 6 - 21 August 2026

### Student prompt (original wording)

> 帮我准备comp3710的面试 有已经参加过面试的人给了如下提示：代码里面可以有注释 建议你用Jupyter notebook，别用.py pytorch和numpy区别，tensor作用 task2的代码里面那个ns有什么作用 如何放大局部 julia set和Mandelbrot的区别 可能会考你sine wave的频率修改，就是f_x，f_y啥的 gabor filter原理和作用 我目前的成果在我的github里

The student later offered the exact course requirements and uploaded:

- `COMP3710_Lab_1_2026.pdf` (Lab Demonstration 1, Version 2.31)
- `COMP3710_Demo_rubric_v2_final.pdf` (Demonstrations Marking Scheme, Version 2.0)

### Context inspected by the AI

The AI inspected the current public GitHub repository `lee1145141919810/COMP3710-Demo1`, including:

- `demo1_fractals.py`
- `README.md`
- `DEMO_NOTES_CN.md`
- `AI_USAGE_LOG.md`
- `VERIFICATION_REPORT.md`
- declared dependencies and generated output file list

The AI then extracted and visually reviewed all 9 pages of the Lab Sheet and all 3 pages of the Demonstrations Marking Scheme.

### AI assistance and reasoning summary

The AI prepared three local interview-support artifacts:

1. an annotated Jupyter notebook organised for parameter changes and oral explanation;
2. a Chinese interview guide with concise and expanded answers;
3. a requirement-by-requirement rubric audit.

The preparation focused on the topics reported by previous students and mapped them to the student's actual variable names and functions. Important findings included:

- The Lab Sheet variable `ns` is a per-pixel counter. Each iteration adds the Boolean `not_diverged` mask, so a larger value means the orbit stayed within the threshold for more iterations. The student's implementation calls the equivalent variable `counts`.
- The Lab Sheet uses `ns = torch.zeros_like(z)`, so `ns` inherits a complex dtype although its imaginary component remains zero. The student's integer `counts` more clearly represents its purpose.
- The Lab Sheet's `z`, `zs`, `zs_`, `not_diverged`, and `ns` correspond to the student's `constant_c`, current `z`, `candidate`, `active` condition, and `counts` respectively.
- The student's `torch.linspace` grid is equivalent to controlling NumPy `mgrid` spacing through `dx=(x_max-x_min)/(width-1)`. For the full Mandelbrot output, `dx` is approximately `7.15e-5`, compared with the sheet's `0.005` step, while the horizontal field of view is about 30 times narrower than the standard `[-2,1]` range.
- The direct `f_x/f_y` sine representation and the repository's `frequency/angle` representation are equivalent through `f_x=f*cos(angle)` and `f_y=f*sin(angle)`.
- The AI identified the distinction between a frequency vector's direction and the visible stripe direction: the stripes are perpendicular to `(f_x,f_y)`.
- The AI highlighted that Mandelbrot should be described precisely as bounded versus escaping, rather than assuming every bounded orbit converges to one limit.
- The AI checked the Lab Sheet's example `c=0.5+0.5i` and found that the canonical orbit from `z_0=0` escapes on iteration 5, with magnitude approximately 3.55.
- The rubric places 40% of marks on questions, understanding and ownership, while functional code accounts for 20%. The interview materials were therefore revised to emphasise explanation and live modification.

### AI-operated verification

The AI created a temporary isolated Python environment and executed all 11 code cells in the revised interview notebook on the CPU. The run completed without code errors and reported:

```text
PyTorch: 2.13.0+cpu
Lab Sheet ns dtype: torch.complex64
Lab Sheet ns maximum imaginary magnitude: 0.0
Repository full Mandelbrot dx: approximately 7.148e-5
Estimated Sierpinski box-counting dimension: 1.892789
Theoretical log(8)/log(3): 1.892789
```

This was an AI-operated verification. It must not be represented as a student-run test.

### Risks identified for student follow-up

- Confirm the Sierpinski carpet choice with the teaching staff and retain evidence of approval.
- Be ready to show completion of the Git Introduction short course.
- Personally run the interview notebook from start to finish on the intended demo machine.
- Personally change and record at least one Mandelbrot zoom/bounds or spacing experiment; the existing log field is incomplete.
- Retain a shareable conversation link or complete prompt history because the rubric states that original AI evidence may be requested.
- Review and, if appropriate, add these new AI interactions to the repository before the demonstration.

### Student-owned work still required

The student should personally practise the three-minute presentation, answer the mock questions without reading, perform the live parameter modifications and verify all outputs.

After the student explicitly authorised necessary repository edits, the AI created the branch `codex/interview-prep-20260821` and committed the reviewed notebook and documentation changes to that branch. The default branch was not changed, and no pull request, merge, teaching-staff message or course submission was performed. The student still needs to review the branch and personally verify that every statement matches their actions before authorising any merge.

## Session 7 - 21 August 2026

### Student prompts (original wording)

> 创建 draft PR

> 现在一步一步带我完成所有步骤并且周密准备

### Draft pull request action

After the student's explicit request, the AI created draft pull request
[#2](https://github.com/lee1145141919810/COMP3710-Demo1/pull/2) from
`codex/interview-prep-20260821` into `main`. At creation, the pull request
was open, draft, mergeable and unmerged. The default branch was not changed.
The pull request was intentionally left as a draft because student-owned
verification, approval and evidence tasks were still incomplete.

### Prompt-history supporting PDF

The AI compiled the complete repository `AI_USAGE_LOG.md` snapshot at commit
`fb1958a341b0c8d5eae37c2a99489d15175778e3` into a local ten-page PDF named
`COMP3710_prompt_history.pdf`. The PDF includes the source commit, a content
hash, an evidence-status warning and a chronology note. The AI checked its text
layer and visually inspected all rendered pages.

The PDF was not uploaded to GitHub and is supporting evidence only. It does not
replace an original shareable conversation link if teaching staff request one,
and AI-operated verification must not be represented as student-run work.

### Student-run verification status

The AI gave the student a Colab link pinned to the reviewed notebook commit and
asked the student to restart the runtime, run all 11 code cells, check every
figure and report the PyTorch version, device, `ns` dtype, Mandelbrot spacing
and box-counting values. No student-run result had been received when this
session was recorded, so the corresponding checklist items remain incomplete.

No merge, ready-for-review transition, teaching-staff message, course
submission or claim of student completion was performed in this session.

## Session 8 - 21 August 2026

### Related student instruction (previously recorded)

> 现在一步一步带我完成所有步骤并且周密准备

### Live Mandelbrot zoom rehearsal improvement

While checking whether the interview notebook supported the requested live
parameter changes, the AI found that the existing zoom rehearsal cell computed
and printed new bounds but did not actually resample, rerun the escape-time
iteration or display the resulting Mandelbrot image.

The AI updated that existing code cell without adding another code cell. It now:

- exposes `practice_span_x` and `practice_iterations` as rehearsal parameters;
- computes bounds around the same complex-plane centre;
- uses `(height-1)/(width-1)` so the horizontal and vertical sample spacing
  are equal;
- prints the new bounds, `dx`, `dy` and zoom factor;
- creates a new coordinate tensor grid, reruns `escape_counts`, and plots the
  recomputed Mandelbrot view.

Changing `practice_span_x` from `0.05` to `0.025` therefore performs a
real additional two-times zoom at the same centre rather than resizing an
existing image.

### AI-operated validation

The AI executed all 11 code cells in the revised notebook in an isolated CPU
environment. The run completed without code errors, produced five PNG display
outputs and reported for the default practice zoom:

```text
practice x limits: (-0.795, -0.745)
practice y limits: (0.05096658711217184, 0.08903341288782818)
dx=1.193e-04, dy=1.193e-04
Zoom relative to the repository view: 2.0x
```

The AI also visually inspected the new plot and confirmed that it displays
recomputed boundary detail rather than a blank or constant image. This remains
AI-operated validation. The student has not yet supplied a personal Run All
result or a personally recorded `0.05 -> 0.025` zoom experiment, so those
checklist items remain incomplete.

No pull-request merge, ready-for-review transition, teaching-staff message,
course submission or claim of student completion was performed.
