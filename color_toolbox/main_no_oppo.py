# 入口：路径选择 + 主流程编排（不含 OPPO 全局配色）
import os
import sys
from PIL import Image

from color_toolbox.config import (
    COLOR_DEFS, FULL_COLOR_COLORS, HUE_OVERLAY_COLORS, POSSIBLE_SUBDIRS,
    TARGET_FILES, DUAL_COLORS, ANCHOR_THRESHOLD, ANCHOR_COLORS,
    OPACITY_80_TASKS, OPACITY_60_TASKS, OVERLAY_TASKS, COPY_RENAME_TASKS,
    BATTERY_SOURCE_DIR, BATTERY_OUTPUT_DIR,
    BATTERY_TYPES, BATTERY_SLICE_SERIES, BATTERY_CHARGE_SERIES,
    BATTERY_ICON_TYPES, FULL_COLOR_FILES,
)
from color_toolbox.engine import (
    get_color_from_reference,
    colorize_image, colorize_image_full, colorize_image_hue_overlay,
    get_anchor_colors, colorize_dual, colorize_anchor,
    apply_opacity, overlay_color,
    composite_images, create_frame_slice,
)


def get_base_dir():
    """交互式获取基础目录路径"""
    raw = input("请输入UI包路径: ").strip(" \t\n\r﻿")
    if raw:
        if not os.path.isdir(raw):
            print(f"错误：路径不存在 '{raw}'")
            return None
        base_dir = raw
        print(f"已找到: {base_dir}")
    else:
        # 兼容旧版：直接使用脚本/EXE 所在目录
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
    return base_dir


def find_subdir(base_dir):
    """在 base_dir 中搜索原子组件文件夹"""
    for name in POSSIBLE_SUBDIRS:
        full = os.path.join(base_dir, name)
        if os.path.isdir(full):
            return name
    return None


def process_single_colors(base_dir, base_subdir, ref_path):
    """处理单色替换（TARGET_FILES）"""
    for color_name, (x, y) in COLOR_DEFS.items():
        print(f"正在提取 {color_name} (坐标 {x},{y}) ...")
        color_rgb = get_color_from_reference(ref_path, x, y)
        print(f"  颜色值: RGB{color_rgb}")

        file_list = TARGET_FILES.get(color_name, [])
        if not file_list:
            print(f"  提示：{color_name} 没有配置目标文件，跳过。\n")
            continue

        for subdir, filename in file_list:
            src_path = os.path.join(base_dir, base_subdir, subdir, filename)
            if not os.path.exists(src_path):
                print(f"  警告：文件不存在，跳过 - {src_path}")
                continue

            print(f"  正在处理: [{subdir}] {filename}")
            with Image.open(src_path) as img:
                if filename in FULL_COLOR_FILES:
                    result = colorize_image_full(img, color_rgb)
                elif color_name in HUE_OVERLAY_COLORS:
                    # 统一完整 HLS（无论亮暗都用目标色完全替换）
                    result = colorize_image_full(img, color_rgb)
                elif color_name in FULL_COLOR_COLORS:
                    result = colorize_image_full(img, color_rgb)
                else:
                    result = colorize_image(img, color_rgb)
                result.save(src_path)

        print()


def process_dual_colors(base_dir, base_subdir, ref_path):
    """处理双色替换（DUAL_COLORS）"""
    if not DUAL_COLORS:
        return
    print("=== 处理双色替换 ===")
    for (subdir, filename), (color_a_name, x1, y1, color_b_name, x2, y2) in DUAL_COLORS.items():
        src_path = os.path.join(base_dir, base_subdir, subdir, filename)
        if not os.path.exists(src_path):
            print(f"  警告：文件不存在，跳过 - {src_path}")
            continue

        target_a_rgb = get_color_from_reference(ref_path, *COLOR_DEFS[color_a_name])
        target_b_rgb = get_color_from_reference(ref_path, *COLOR_DEFS[color_b_name])

        print(f"  正在处理: [{subdir}] {filename}")
        print(f"    {color_a_name} @ ({x1},{y1}), {color_b_name} @ ({x2},{y2})")

        with Image.open(src_path) as img:
            anchor_a_rgb, anchor_b_rgb = get_anchor_colors(img, (x1, y1), (x2, y2))
            print(f"    锚点A({color_a_name}): RGB{anchor_a_rgb}, 锚点B({color_b_name}): RGB{anchor_b_rgb}")
            result = colorize_dual(img, target_a_rgb, target_b_rgb,
                                   anchor_a_rgb, anchor_b_rgb,
                                   color_a_name in FULL_COLOR_COLORS,
                                   color_b_name in FULL_COLOR_COLORS)
            result.save(src_path)
    print()


def process_anchor_colors(base_dir, base_subdir, ref_path):
    """处理单锚点替换（ANCHOR_COLORS）"""
    if not ANCHOR_COLORS:
        return
    print("=== 处理单锚点替换 ===")
    for (subdir, filename), (color_name, ax, ay) in ANCHOR_COLORS.items():
        src_path = os.path.join(base_dir, base_subdir, subdir, filename)
        if not os.path.exists(src_path):
            print(f"  警告：文件不存在，跳过 - {src_path}")
            continue

        target_rgb = get_color_from_reference(ref_path, *COLOR_DEFS[color_name])

        print(f"  正在处理: [{subdir}] {filename}")
        print(f"    目标色: {color_name} RGB{target_rgb}, 锚点 @ ({ax},{ay})")

        with Image.open(src_path) as img:
            anchor_rgb = img.load()[ax, ay][:3]
            print(f"    锚点颜色: RGB{anchor_rgb}")
            result = colorize_anchor(img, target_rgb, anchor_rgb, ANCHOR_THRESHOLD)
            result.save(src_path)
    print()


def _run_opacity_batch(base_dir, tasks, opacity, label):
    """批量处理透明度 + 重命名任务"""
    processed = 0
    skipped = 0
    errors = 0
    for rel_dir, src_name, dst_name in tasks:
        src_path = os.path.join(base_dir, rel_dir, src_name)
        dst_path = os.path.join(base_dir, rel_dir, dst_name)
        if not os.path.exists(src_path):
            print(f"  警告：源文件不存在，跳过 - {rel_dir}\\{src_name}")
            errors += 1
            continue
        try:
            print(f"  处理: {rel_dir}\\{src_name} → {dst_name}")
            with Image.open(src_path) as img:
                result = apply_opacity(img, opacity)
                result.save(dst_path)
            processed += 1
        except Exception as e:
            print(f"  错误: {dst_name} - {e}")
            errors += 1
    print(f"  [{label}] 完成: {processed} 已处理, {skipped} 已跳过, {errors} 错误\n")


def process_opacity_tasks(base_dir):
    """处理透明度 + 重命名任务"""
    print("\n=== 批量处理：透明度 + 重命名 ===")
    _run_opacity_batch(base_dir, OPACITY_80_TASKS, 0.8, "80%透明度")
    _run_opacity_batch(base_dir, OPACITY_60_TASKS, 0.6, "60%透明度")


def process_overlay_tasks(base_dir):
    """处理纯色叠加任务 (OVERLAY_TASKS)"""
    print("=== 批量处理：纯色叠加 ===")
    processed = 0
    skipped = 0
    errors = 0
    for rel_dir, src_name, dst_name, color_rgb, alpha in OVERLAY_TASKS:
        src_path = os.path.join(base_dir, rel_dir, src_name)
        dst_path = os.path.join(base_dir, rel_dir, dst_name)
        if not os.path.exists(src_path):
            print(f"  警告：源文件不存在，跳过 - {rel_dir}\\{src_name}")
            errors += 1
            continue
        try:
            color_desc = f"RGB{color_rgb}"
            print(f"  叠加 {color_desc} x {alpha}: {rel_dir}\\{src_name} → {dst_name}")
            with Image.open(src_path) as img:
                result = overlay_color(img, color_rgb, alpha)
                result.save(dst_path)
            processed += 1
        except Exception as e:
            print(f"  错误: {dst_name} - {e}")
            errors += 1
    print(f"  完成: {processed} 已处理, {skipped} 已跳过, {errors} 错误\n")


def process_copy_rename_tasks(base_dir):
    """处理复制 + 重命名任务 (COPY_RENAME_TASKS)"""
    print("=== 批量处理：复制重命名 ===")
    processed = 0
    skipped = 0
    errors = 0
    for rel_dir, src_name, dst_name in COPY_RENAME_TASKS:
        src_path = os.path.join(base_dir, rel_dir, src_name)
        dst_path = os.path.join(base_dir, rel_dir, dst_name)
        if not os.path.exists(src_path):
            print(f"  警告：源文件不存在，跳过 - {rel_dir}\\{src_name}")
            errors += 1
            continue
        try:
            print(f"  复制: {rel_dir}\\{src_name} → {dst_name}")
            with Image.open(src_path) as img:
                img.save(dst_path)
            processed += 1
        except Exception as e:
            print(f"  错误: {dst_name} - {e}")
            errors += 1
    print(f"  完成: {processed} 已处理, {skipped} 已跳过, {errors} 错误\n")


def process_battery_tasks(base_dir):
    """制作电池切片：叠加图标 + 动画切片 + 充电动画切片"""
    src_dir = os.path.join(base_dir, BATTERY_SOURCE_DIR)
    out_dir = os.path.join(base_dir, BATTERY_OUTPUT_DIR)

    if not os.path.isdir(src_dir):
        print(f"  错误：源目录不存在 '{src_dir}'")
        return
    os.makedirs(out_dir, exist_ok=True)

    print("\n=== 第一步：叠加图标 ===")
    for type_name, fill_base in BATTERY_TYPES:
        base_path = os.path.join(src_dir, f"{fill_base}.png")
        dianchi_path = os.path.join(src_dir, "电池底.png")
        kuang_path = os.path.join(src_dir, "框.png")

        if not all(os.path.exists(p) for p in [base_path, dianchi_path, kuang_path]):
            print(f"  警告：源文件缺失，跳过 {type_name}")
            continue

        with Image.open(base_path) as base_img, Image.open(kuang_path) as kuang_img:
            result = composite_images(base_img, kuang_img)
            result.save(os.path.join(out_dir, f"{type_name}.png"))
            result.save(os.path.join(out_dir, f"{type_name}_deep.png"))

        with Image.open(dianchi_path) as dianchi_img, Image.open(kuang_path) as kuang_img:
            result = composite_images(dianchi_img, kuang_img)
            result.save(os.path.join(out_dir, f"{type_name}_bg.png"))
            result.save(os.path.join(out_dir, f"{type_name}_bg_deep.png"))

        if type_name in BATTERY_ICON_TYPES:
            icon_src = os.path.join(src_dir, f"{type_name}_icon.png")
            if os.path.exists(icon_src):
                img = Image.open(icon_src)
                img.save(os.path.join(out_dir, f"{type_name}_icon.png"))
                img.save(os.path.join(out_dir, f"{type_name}_icon_deep.png"))
                img.close()

        print(f"  {type_name} 完成")

    print("\n=== 第二步：电池动画切片 ===")
    dianchi_path = os.path.join(src_dir, "电池底.png")
    kuang_path = os.path.join(src_dir, "框.png")

    for prefix, fill_00_03, fill_04_19 in BATTERY_SLICE_SERIES:
        fill_03_path = os.path.join(src_dir, f"{fill_00_03}.png")
        fill_19_path = os.path.join(src_dir, f"{fill_04_19}.png")

        for frame in range(20):
            fill_path = fill_03_path if frame < 4 else fill_19_path
            with Image.open(dianchi_path) as dianchi_img, \
                 Image.open(fill_path) as fill_img, \
                 Image.open(kuang_path) as kuang_img:

                slice_img = create_frame_slice(fill_img, frame, 20)
                tmp = composite_images(dianchi_img, slice_img)
                result = composite_images(tmp, kuang_img)

                color_name = f"{prefix}_{frame:02d}_color.png"
                result.save(os.path.join(out_dir, color_name))
                white_name = f"{prefix}_{frame:02d}_white.png"
                result.save(os.path.join(out_dir, white_name))

        print(f"  {prefix} 完成")

    print("\n=== 第三步：带图标的充电动画切片 ===")
    for prefix, icon_name, icon_width, fill_04_19 in BATTERY_CHARGE_SERIES:
        icon_path = os.path.join(src_dir, f"{icon_name}.png")
        fill_03 = "低电量"
        fill_19 = fill_04_19 if fill_04_19 else "正常"
        fill_03_path = os.path.join(src_dir, f"{fill_03}.png")
        fill_19_path = os.path.join(src_dir, f"{fill_19}.png")

        total_width = 72 + icon_width

        for frame in range(20):
            fill_path = fill_03_path if frame < 4 else fill_19_path
            with Image.open(icon_path) as icon_img, \
                 Image.open(dianchi_path) as dianchi_img, \
                 Image.open(fill_path) as fill_img, \
                 Image.open(kuang_path) as kuang_img:

                slice_img = create_frame_slice(fill_img, frame, 20)
                tmp = composite_images(dianchi_img, slice_img)
                battery_part = composite_images(tmp, kuang_img)

                canvas = Image.new("RGBA", (total_width, 40), (0, 0, 0, 0))
                canvas.paste(icon_img, (0, 0))
                canvas.paste(battery_part, (icon_width, 0))

                color_name = f"{prefix}_{frame:02d}_color.png"
                canvas.save(os.path.join(out_dir, color_name))
                white_name = f"{prefix}_{frame:02d}_white.png"
                canvas.save(os.path.join(out_dir, white_name))

        print(f"  {prefix} 完成 ({total_width}x40)")

    print(f"\n电池切片制作完成！输出目录: {out_dir}")


def main():
    print("=== 配色工具（无 OPPO 全局配色）===\n")

    base_dir = get_base_dir()
    if base_dir is None:
        input("按回车键退出...")
        return

    ref_path = os.path.join(base_dir, "全局配色.png")
    if not os.path.exists(ref_path):
        print(f"错误：找不到参考图 '{ref_path}'")
        input("按回车键退出...")
        return

    base_subdir = find_subdir(base_dir)
    if base_subdir is None:
        print(f"错误：找不到文件夹 {POSSIBLE_SUBDIRS}")
        input("按回车键退出...")
        return

    print(f"参考图: {ref_path}")
    print(f"原子组件: {base_subdir}\n")

    print("=== 自动取色并 Colorize 着色目标图片 ===")
    process_single_colors(base_dir, base_subdir, ref_path)
    process_dual_colors(base_dir, base_subdir, ref_path)
    process_anchor_colors(base_dir, base_subdir, ref_path)

    print("\n=== 批量图片处理 ===")
    process_opacity_tasks(base_dir)
    process_overlay_tasks(base_dir)
    process_copy_rename_tasks(base_dir)

    print("\n=== 电池切片制作 ===")
    process_battery_tasks(base_dir)

    print("全部完成！")
    input("按回车键退出...")


if __name__ == "__main__":
    main()
