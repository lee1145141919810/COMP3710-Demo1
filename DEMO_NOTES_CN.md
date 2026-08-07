# COMP3710 Demo 1 现场讲解提纲

这份提纲帮助理解代码。演示时不要逐字背诵，要用自己的话讲，并准备现场修改参数。

## Part 1：Gaussian、二维余弦和 Gabor filter

开场可以这样解释：

> 我先创建一张坐标网格，每个像素同时对应一个 `(x, y)`。高斯函数在中心最大，离中心越远越接近零。二维余弦的相位由旋转后的坐标决定，所以形成有方向的条纹。两者相乘后，条纹只在中心附近明显，这就是 Gabor filter。

必须会回答：

- `sigma` 控制高斯包络的宽度。
- `frequency` 控制条纹的密度。
- `angle` 控制条纹的方向。
- `gaussian * sinusoid` 是调制；高斯是 envelope，余弦是 carrier。
- `.cpu().numpy()` 是因为 Matplotlib 通常读取 CPU 上的 NumPy 数组，而计算可能在 GPU tensor 上。

现场可改：把 `angle` 从 30° 改成 60°，或者改变 `frequency`，重新运行后指出条纹方向/密度变化。

## Part 2：Mandelbrot 和 Julia

共同迭代公式：

`z_(n+1) = z_n² + c`

核心区别：

- Mandelbrot：每个像素是不同的 `c`，所有像素从 `z₀ = 0` 开始。
- Julia：每个像素是不同的 `z₀`，整张图共用同一个固定 `c`。
- 当 `|z| > 2` 时判定已经逃逸；颜色表示逃逸前经历的迭代次数。
- Mandelbrot 放大图使用更窄的坐标范围和更多像素，所以 mgrid/linspace 的间隔更小、细节更多，但计算更慢。

必须会指出代码里的两处变化：

1. Mandelbrot 调用 `escape_counts(torch.zeros_like(c), c, ...)`。
2. Julia 调用 `escape_counts(initial_z, julia_constant, ...)`。

现场可改：把 Julia 常量从 `-0.8 + 0.156j` 改成 `-0.4 + 0.6j`，比较形状。

## Part 3：Sierpinski carpet

形成规则：

1. 把正方形分成 `3 × 3`。
2. 删除中心小正方形。
3. 对剩下的八个正方形重复这个过程。

为什么使用 PyTorch 是合理的：

> 我没有用 Python 双重循环逐个检查像素，而是把所有 x/y 坐标放进 tensor。每一层都用取余和布尔 mask 同时检查所有像素。这个工作可以在 GPU 上并行执行；分辨率为 `3^7 × 3^7` 时差别尤其明显。

维数分析：

- 每次长度缩小为 `1/3`，保留 8 个副本。
- 理论分形维数是 `log(8) / log(3) ≈ 1.8928`。
- box counting 在多个网格尺度统计非空格子。
- `log(N)` 对 `log(1/scale)` 的拟合斜率就是估计维数。
- 估计值接近 1.8928，说明程序生成的结构符合理论。

## 老师可能追问

**为什么 Mandelbrot/Julia 仍然有一个 Python 的迭代循环？** 迭代在时间上依赖上一步，不能全部同时完成；但循环中的每一步会一次并行更新整张图的所有像素。

**为什么 Sierpinski 是“substantially different”？** Mandelbrot/Julia 使用复数二次迭代和逃逸时间；Sierpinski 使用几何递归/三进制坐标删除规则，没有复数动力系统。

**AI 做了什么？** AI 帮助组织代码、提出向量化实现和分析方法。提示词与修改记录在 `AI_USAGE_LOG.md`。我本人运行、检查结果、修改参数，并能解释每一部分。

**如何证明这是你的 GitHub？** 登录自己的账户，打开仓库主页，显示 commit history，并准备按老师要求验证账户。

## 演示前硬性检查

- 完成 Git Introduction 短课（4 分）。
- 先问 demonstrator 是否需要对 Sierpinski carpet 额外批准。
- GitHub 仓库至少有数次有意义的 commit。
- 五张图片都能重新生成。
- AI log 已补充所有之后的提示词。
- 能在现场改角度、Julia 常量或 Sierpinski 层数并重新运行。
