# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: 配色工具 (color_toolbox)

Android VIVO/OPPO 主题配色工具 — 从参考图 `全局配色.png` 取色，自动对着色目标图片做 HLS 着色、双色替换、锚点替换、透明度调整、纯色叠加、电池切片制作等图像处理。支持 OPPO 全局配色的 12 章节批量处理流水线。

## 运行命令

```bash
# 运行含 OPPO 版本（交互式输入路径）
python -m color_toolbox.main

# 运行无 OPPO 版本
python -m color_toolbox.main_no_oppo

# 直接输入路径（免交互）
echo "d:/test/配色素材" | python -m color_toolbox.main
```

## 打包命令（PyInstaller）

```bash
# Windows
pyinstaller --onefile --console --name "配色工具" --distpath . --workpath "color_toolbox/build/pyinstaller_main" --specpath "color_toolbox" "color_toolbox/main.py"

# 无 OPPO 版本
pyinstaller --onefile --console --name "配色工具_无OPPO" --distpath . --workpath "color_toolbox/build/pyinstaller_no_oppo" --specpath "color_toolbox" "color_toolbox/main_no_oppo.py"
```

### macOS 打包

Mac 打包时 `--add-data` 用 `color_toolbox:color_toolbox`（Windows 用 `;` 分隔）。

**推荐方式**：在 `color_toolbox/` 目录下双击 `build_mac.command`，会自动：
1. 安装 PyInstaller（如未安装）
2. 打包含 OPPO / 无 OPPO 两个版本
3. 为每个版本创建 **`.app` bundle 包裹**（双击可直接运行，传给其他 Mac 也可用）
4. 清理中间文件，最终产物：`配色工具.app` + `配色工具_无OPPO.app`

```bash
# 或手动打包 macOS 版（.app 需用 build_mac.command 自动创建）
pyinstaller --onefile --console --name "配色工具" --distpath . --add-data "color_toolbox:color_toolbox" --workpath "color_toolbox/build/pyinstaller_main" --specpath "color_toolbox" "color_toolbox/main.py"
```

## 项目架构

### 文件包结构 `color_toolbox/`

| 文件 | 职责 |
|------|------|
| `config.py` | 纯配置数据 — VIVO 5 种 + OPPO 9 种取色坐标、目标文件列表、双色/锚点替换配置、批处理任务列表 |
| `engine.py` | 核心图像处理引擎 — HLS 着色系列、双色/锚点着色、画布操作、透明度、混合、电池切片 |
| `main.py` | 入口 + 流程编排（含 OPPO 12 章节） |
| `main_no_oppo.py` | 无 OPPO 版入口（**与 main.py 独立副本**，非 import 复用） |
| `oppo_tasks.py` | OPPO 12 章节流水线，各 process_section_N 独立函数 |

### 处理流程（main.py）

```
全局配色.png 取色
  → 单色替换（HLS 着色 TARGET_FILES）
  → 双色替换（锚点距离法 DUAL_COLORS）
  → 锚点替换（阈值筛选 ANCHOR_COLORS）
  → 批处理（80%透明度 / 纯色叠加 / 复制重命名）
  → 电池切片制作（叠加图标 + 20帧动画切片）
  → OPPO 12 章节
```

### 着色方式

- **HLS 着色**（`colorize_image` 默认）：替换色相 H 和饱和度 S，保留原图亮度 L。
- **完整 HLS**（`colorize_image_full`）：替换 H/L/S 全部通道，颜色与目标色完全一致。用于 `FULL_COLOR_COLORS`（主高亮色、浅色、深色）、`FULL_COLOR_FILES`（按文件名强制完整 HLS）、以及**光圈色**（统一完整 HLS，不再叠加）。
- **双色着色**（`colorize_dual`）：按像素到两个锚点的 RGB 欧氏距离分类，分别用不同目标色着色。
- **锚点着色**（`colorize_anchor`）：只替换与锚点颜色距离 ≤ ANCHOR_THRESHOLD（2000）的像素。

### 取色坐标

**OPPO（全局配色.png）** — 9 个：

| 颜色名 | 坐标 | 用于 |
|--------|------|------|
| 点九色 | (1025, 25) | Section 3 点九色适配 |
| 不可用态 | (25, 1180) | Section 1 时间改色 |
| 浅色 | (1030, 180) | Section 4 按钮改色 |
| 深色 | (1030, 230) | Section 4 提示改色 |
| 主高亮色 | (1030, 280) | 保留 |
| 控制中心颜色1 | (25, 525) | `_active` 源色 |
| 控制中心颜色2 | (25, 575) | `_inactive` / `_off` |
| 控制中心颜色3 | (25, 625) | `_unavailable` / `_anim` |
| 桌面文字色 | (25, 1125) | Section 11 AOD 数字改色 |

**VIVO（全局配色.png）** — 5 个：浅色(1030,180)、深色(1030,230)、主高亮色(1030,280)、光圈色(1030,1030)、按钮火箭色(1030,330)。

### 着色优先级

处理单色替换时，判断顺序如下：

```
if filename in FULL_COLOR_FILES:       → 完整 HLS（按文件名强制）
elif color_name in HUE_OVERLAY_COLORS: → 完整 HLS（光圈色统一处理）
elif color_name in FULL_COLOR_COLORS:  → 完整 HLS（主高亮色/浅色/深色）
else:                                   → 默认 HLS（保留亮度）
```

### OPPO 章节流水线

| 章节 | 目录 | 主要操作 |
|------|------|---------|
| 1 | 01+04设置图标-拨号盘 | 时间改色(不可用态)、气泡复制、箭头**50%**透明度、_selected→_normal **50%**透明度、拨号键 _normal→_pressed、49x72/49x125 裁剪 |
| 2 | 01+04设置图标-14版本 | **自动扫描**所有 `_selected.png` → 50%透明度 → `_normal.png`（mms 文件改为 `_unselected.png`） |
| 3 | 02-点九色适配 | 全部改点九色（保留 .9.png 边框标记），特殊文件叠10%黑色遮罩 |
| 4 | 03-高亮色适配 | 从02/01复制气泡、缩放（150x150/137x137 带九宫格）、改浅色/深色、透明度 |
| 5 | 04-高亮色13版本 | 从03复制6个来电图→scale_proportional+204x204 居中 |
| 6 | 06-控制中心 | 大量复制/透明度/重命名/缩放、VIVO电池素材缩放 |
| 7 | 06-控制中心-15版本 | 画布270x132/78x48、VIVO电池素材、USB图标改色(排除白色) |
| 8 | 07-控制中心元素 | 从 `_active` 源图生成 `_inactive`/`_unavailable`/`_anim`/`_off` 变体（color2/color3），3个特殊文件裁图案→等比缩放54x54 |
| 9 | 07-控制中心元素→15版本 | 取 `_active` 源图→裁剪图案→1.05x缩放(50%柔化)→着色生成全部变体→居中84x84输出到`07-15版本`；独立文件直接1.05x缩放 |
| 10 | 08-状态栏15版本→08-状态栏 | 从15版本(48px高)复制 stat_* →按08标准尺寸(36px高)内容检测缩放：图案能放下→居中，太大→等比缩小 |
| 11 | 08-状态栏 (AOD数字) | AOD 时钟数字 `aod_clock_drawable_vertical_0~9.png` 改桌面文字色 |
| 12 | OPPO-09音量 | 从06复制音量图标→96x96，特殊缩放(94x74+144x144 等) |

### .9.png 处理注意

`.9.png` 四周 1px 边框包含九宫格拉伸标记（黑色像素）。`_colorize_preserve_9patch` 和 `_apply_opacity_preserve_9patch` 在处理时会保存边框再恢复。`_apply_9patch_border` 用于为缩放后的图片重新生成标准边框标记。

Section 4 中预定义了 2 组标准边框模式（150x150 会话气泡、137x137 rcs 气泡），通过 `_scale_9patch_from_source` 统一处理。

### 已知注意事项

- **PIL paste 掩码问题**：`canvas.paste(rgba, (x, y), rgba)` 会将 alpha 再次作为混合权重，导致透明度降低。正确用法：`canvas.paste(rgba, (x, y))` 不带 mask 参数。已在 engine.py 修复。
- **main_no_oppo.py 独立副本**：不含 OPPO 流程，但与 main.py 是独立副本（非 import 复用），两处需同步修改。
- **dead code in engine.py**：`colorize_image_mapped`、`colorize_image_multiply`、`colorize_anchor_multiply`、`replace_color` 定义了但未被其他文件 import 调用。
- **dead code in config.py**：`HUE_OVERLAY_ALPHA` 已不再用于处理逻辑（光圈色改为统一完整 HLS），保留仅供参考。
- **OPPO 不可用态坐标**：Section 1 时间改色用的坐标已从 (25, 625) 修正为 (25, 1180)。(25, 625) 现在是控制中心颜色3，两者不同。
- **Section 9 是先缩放后着色**：从 108×108 `_active` 源裁剪图案→1.05x 缩放(50%柔化)→再 colorize，质量优于先着色再缩放。
- **Section 2 自动扫描**：自动匹配文件夹内所有 `_selected.png` 后缀文件，新增图片无需改代码。`mms_ic_tab_` 开头的文件输出为 `_unselected.png`，其他文件输出为 `_normal.png`。
- **FULL_COLOR_FILES 优先级最高**：独立于颜色组，在 HUE_OVERLAY_COLORS/FULL_COLOR_COLORS 之前判断。
