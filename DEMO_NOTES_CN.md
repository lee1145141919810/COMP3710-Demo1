# COMP3710 Demo 1 现场讲解提纲

这份提纲按 Lab Sheet v2.31 与 Demonstrations Marking Scheme v2.0 整理。演示时不要逐字背诵；用自己的话解释，并准备先预测、再修改、再运行。

## Rubric 重点

- Functional code：20%
- Questions, understanding and ownership：40%
- Programming、documentation 与 fair AI：20%
- Summary and ownership：20%

建议先用约 3 分钟完成陈述，整个 demo 至少约 5 分钟，之后接受追问。

## 三分钟陈述顺序

1. **0:00-0:25**：三个 Part、CPU/CUDA、quick/full workflow、公开 GitHub。
2. **0:25-0:55**：Gaussian、oriented cosine、Gabor。
3. **0:55-1:40**：Mandelbrot zoom、`ns/counts`、Julia 区别。
4. **1:40-2:35**：Sierpinski 的三进制规则、PyTorch 并行、removal depth、box counting、Git short course。
5. **2:35-3:00**：AI 做了什么、自己如何检查/实验，并主动表示可以现场改参数。

## Part 1：Gaussian、二维余弦和 Gabor filter

> 我先创建一张坐标网格，每个像素对应一对 `(x,y)`。Gaussian 在中心最大并随距离衰减。二维 cosine 的相位依赖 x/y，因此形成有方向的条纹。Gaussian 与 cosine 相乘后，条纹只在局部区域明显，这就是 Gabor filter。

公式：

```text
cos(2*pi*(f_x*x + f_y*y))
f_x = frequency*cos(angle)
f_y = frequency*sin(angle)
gabor = gaussian*sinusoid
```

必须会回答：

- `sigma` 控制 Gaussian envelope 的空间范围。
- `sqrt(f_x²+f_y²)` 控制条纹密度。
- `f_x:f_y` 控制频率向量方向；可见条纹与该向量垂直。
- `gaussian * sinusoid` 是 modulation；Gaussian 是 envelope，cosine 是 carrier。
- Gabor 对局部方向和空间频率具有选择性，可用于边缘、纹理和脊线特征。
- `.cpu().numpy()` 先把 CUDA tensor 搬回 CPU，再转换为 Matplotlib/NumPy 可用的数组。
- 现代 PyTorch 默认 eager execution；本项目不训练模型，因此用 `@torch.no_grad()` 避免记录不需要的 autograd 图。

现场可改：`angle: 30°→60°`、`frequency: 0.75→1.5`，或直接尝试 `(f_x,f_y)=(0.8,0)`。

## Part 2：Mandelbrot、`ns` 和 Julia

共同公式：

`z_(n+1) = z_n² + c`

精确表述应使用轨道 **bounded（有界）** 或 **escapes（逃逸）**，不要假设所有黑色点都收敛到同一个极限。

### 官方变量与本项目变量

| Lab Sheet | 含义 | 本项目 |
|---|---|---|
| `z` | 每像素固定的参数 `c` | Mandelbrot 的 `c` / `constant_c` |
| `zs` | 当前轨道状态 | 函数内部的 `z` |
| `zs_` | 下一步候选状态 | `candidate` |
| `not_diverged` | 当前仍在阈值内的 mask | `active` 的更新条件 |
| `ns` | 每像素累计未逃逸轮数 | 整数 `counts` |

> 官方 `ns` 每轮加上 `not_diverged`，所以值越大表示越晚逃逸或在迭代上限内未逃逸；最后用它着色，它不参与轨道更新。官方使用 `zeros_like(z)`，所以 `ns` 继承 complex dtype、虚部保持 0；本项目用 `int32 counts` 更符合计数器语义。

官方 `ns` 与本项目 `counts` 概念对应，但有限迭代数值不保证完全一致：官方从 `zs=c` 开始并检查 `abs(z)<4`；本项目明确从 canonical `z₀=0` 开始并使用标准逃逸半径 2。

### Mandelbrot 与 Julia

- Mandelbrot：每个像素是不同的 `c`，固定 `z₀=0`。
- Julia：每个像素是不同的 `z₀`，整张图固定同一个 `c`。
- Mandelbrot 调用：`escape_counts(torch.zeros_like(c), c, ...)`。
- Julia 调用：`escape_counts(initial_z, julia_constant, ...)`。

当前 Julia 参数为 `c=-0.4+0.6j`，图像是不连通的岛状簇；可以改回 `-0.8+0.156j` 比较卷曲和螺旋结构。

### 如何放大

原题使用：

```python
Y, X = np.mgrid[-1.3:1.3:0.005, -2:1:0.005]
```

本项目使用 `torch.linspace`，等效 spacing 为：

```text
dx = (x_max-x_min)/(width-1)
dy = (y_max-y_min)/(height-1)
```

full Mandelbrot 的横向 `dx≈7.15e-5`，小于原题的 `0.005`；横向视野从 `[-2,1]` 的宽度 3 缩到 0.1，约为 30 倍 field-of-view zoom。

- 缩小坐标范围才是 zoom。
- 增大 width/height 是在当前视野提高采样密度。
- PNG dpi 或 bilinear interpolation 只改变显示，不增加真实分形细节。
- 更深 zoom 通常需要更多 iterations，以区分慢逃逸点。

### active mask 的准确作用

`active` 阻止已逃逸状态继续写回，避免数值继续增长，并允许所有点逃逸时提前结束。当前代码仍先对全图计算 `candidate=z.square()+c`，所以不要说它完全跳过了 inactive 像素；GPU 上的 `bool(active.any())` 还会造成同步。

## Part 3：Sierpinski carpet

形成规则：

1. 把正方形分成 `3×3`。
2. 删除中心小正方形。
3. 对剩余 8 个小正方形重复。

> 坐标的三进制位表示像素在每一层的左/中/右位置。若某一层 x 和 y 的三进制位同时为 1，该像素位于中心格并被删除。代码只对 level 循环；每一层使用 tensor remainder 和 Boolean mask 同时处理所有像素，因此 PyTorch 是算法的主要并行组件。

维数分析：

- 每次长度缩小为 `1/3`，保留 8 个副本。
- 理论维数：`log(8)/log(3)≈1.892789`。
- box counting 在多个尺度统计非空 box。
- `log(N)` 对 `log(1/scale)` 的斜率是估计维数。
- 当前尺度与理想 carpet 的三进制结构对齐，因此结果几乎精确等于理论值；自然或噪声分形通常不会如此精确。

为什么 substantially different：Mandelbrot/Julia 是复数动力系统与 escape time；Sierpinski 是几何自相似与三进制删除规则。

## AI 使用与 ownership

不要只说“AI 帮我写了代码”。应展示：

- `AI_USAGE_LOG.md`；
- 原始对话链接或完整 prompt history；
- AI 输出中发现的问题和后续 refinement；
- 自己亲自运行、改变参数和观察结果的证据。

可以在亲自复核后这样组织回答：

> AI 很快给出了基础结构，但 NumPy 转 PyTorch 不只是替换函数名，还要检查 dtype、device、GPU-to-CPU plotting 和是否需要 autograd。对 Mandelbrot/Julia 还要检查 z₀、固定/变化的参数、逃逸阈值和有限迭代颜色。最终项目使用明确的 `initial_z/constant_c`、整数 `counts`、quick/full 模式、第二种可视化和 box-counting 验证。

必须准确区分 student-run 和 AI-operated checks。目前已有记录表明学生亲自运行 quick mode 并修改/比较 Julia 参数；其他项目只有在本人完成后才能声称“我亲自运行”。

## 高频追问

**为什么仍有 Python for 循环？** 时间迭代依赖前一步，但每轮同时更新整张图的所有像素。

**Tensor 有什么作用？** 用 shape、dtype 和 device 明确表示整张图的坐标、复数状态、Boolean mask 和计数。

**为什么 Part 3 合理使用 PyTorch？** 不是只把 NumPy 数组包装成 tensor，而是每层用 tensor 运算并行处理全部像素。

**如何证明结果正确？** 代码规则对应数学构造；box-counting 数值与理论维数一致；同时保留不同可视化。

**如何证明是自己的 GitHub？** 登录账户，展示 repository 与 commit history，并按要求验证账号。

## 演示前硬性检查

- [ ] 取得并保存 teaching-staff 对 Sierpinski carpet 的批准。
- [ ] 准备 Git Introduction short-course 完成证明（4 marks）。
- [ ] 亲自 Run All notebook 或运行脚本并检查五张图。
- [ ] 亲自做一次 Mandelbrot bounds/spacing 实验并记录观察。
- [ ] 更新全部 AI prompts、输出/推理与修改记录。
- [ ] 准备原始 AI conversation link 或 prompt history。
- [ ] 登录 GitHub 并能展示 commit history。
- [ ] 确认 teaching staff 是否要求明确的开源 licence。
- [ ] 能在 1-2 分钟内修改 Gabor frequency、Mandelbrot span、Julia c 或 Sierpinski level。
