# 核心引擎：颜色提取、HLS 着色、双色/锚点替换
from PIL import Image
import colorsys


def get_color_from_reference(ref_path, x, y):
    """从参考图中读取 (x, y) 坐标的 RGB 颜色"""
    with Image.open(ref_path) as img:
        rgb = img.getpixel((x, y))
        if isinstance(rgb, int):
            rgb = (rgb, rgb, rgb)
        else:
            rgb = rgb[:3]
    return rgb


def colorize_image(img, color_rgb):
    """HLS 着色：保留原图亮度（L），替换色相（H）和饱和度（S）"""
    target_h, _, target_s = colorsys.rgb_to_hls(
        color_rgb[0] / 255.0, color_rgb[1] / 255.0, color_rgb[2] / 255.0
    )
    has_alpha = img.mode == "RGBA"
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            _, l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            nr, ng, nb = colorsys.hls_to_rgb(target_h, l, target_s)
            pixels[x, y] = (
                max(0, min(255, round(nr * 255))),
                max(0, min(255, round(ng * 255))),
                max(0, min(255, round(nb * 255))),
                a,
            )

    if not has_alpha:
        img = img.convert("RGB")
    return img


def colorize_image_full(img, color_rgb):
    """用目标色完整 HLS 着色：替换色相（H）、饱和度（S）和亮度（L）"""
    target_h, target_l, target_s = colorsys.rgb_to_hls(
        color_rgb[0] / 255.0, color_rgb[1] / 255.0, color_rgb[2] / 255.0
    )
    has_alpha = img.mode == "RGBA"
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            a = pixels[x, y][3]
            if a == 0:
                continue
            nr, ng, nb = colorsys.hls_to_rgb(target_h, target_l, target_s)
            pixels[x, y] = (
                max(0, min(255, round(nr * 255))),
                max(0, min(255, round(ng * 255))),
                max(0, min(255, round(nb * 255))),
                a,
            )

    if not has_alpha:
        img = img.convert("RGB")
    return img


def colorize_image_mapped(img, color_rgb, strength=0.6):
    """HLS 着色：用目标色 H 和 S，原图亮度向目标色亮度偏移
    strength=0 → 完全保留原图亮度（同 colorize_image）
    strength=1 → 完全使用目标色亮度（同 colorize_image_full）
    保留原图明暗相对关系，但整体亮度范围向目标色靠近"""
    target_h, target_l, target_s = colorsys.rgb_to_hls(
        color_rgb[0] / 255.0, color_rgb[1] / 255.0, color_rgb[2] / 255.0
    )
    has_alpha = img.mode == "RGBA"
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            _, original_l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            mapped_l = original_l * (1 - strength) + target_l * strength
            nr, ng, nb = colorsys.hls_to_rgb(target_h, mapped_l, target_s)
            pixels[x, y] = (
                max(0, min(255, round(nr * 255))),
                max(0, min(255, round(ng * 255))),
                max(0, min(255, round(nb * 255))),
                a,
            )

    if not has_alpha:
        img = img.convert("RGB")
    return img


def colorize_image_multiply(img, color_rgb, strength=1.0):
    """Multiply blend 着色（带强度控制）

    纯 Multiply：result = src * target / 255
    混合版：result = src * (1-strength) + multiply * strength
    strength=0：原图不变，strength=1：纯 Multiply"""
    tr, tg, tb = color_rgb
    has_alpha = img.mode == "RGBA"
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            mr = r * tr // 255
            mg = g * tg // 255
            mb = b * tb // 255
            nr = round(r * (1 - strength) + mr * strength)
            ng = round(g * (1 - strength) + mg * strength)
            nb = round(b * (1 - strength) + mb * strength)
            pixels[x, y] = (
                max(0, min(255, nr)),
                max(0, min(255, ng)),
                max(0, min(255, nb)),
                a,
            )

    if not has_alpha:
        img = img.convert("RGB")
    return img


def colorize_image_hue_overlay(img, color_rgb, overlay_alpha=0.35):
    """先 HLS 改色相（保留亮度），再叠加目标色增加饱和度

    两步法：
    1. colorize_image → 把色相和饱和度改为目标色，保留原图亮度
    2. overlay_color → 叠加目标色 RGB，增加颜色深度"""
    result = colorize_image(img, color_rgb)
    result = overlay_color(result, color_rgb, overlay_alpha)
    return result


def get_anchor_colors(img, xy_a, xy_b):
    """从目标图上读取两个锚点坐标的 RGB 值"""
    pixels = img.load()
    x1, y1 = xy_a
    x2, y2 = xy_b
    anchor_a = pixels[x1, y1][:3]
    anchor_b = pixels[x2, y2][:3]
    return anchor_a, anchor_b


def color_distance(c1, c2):
    """RGB 欧氏距离"""
    return sum((a - b) ** 2 for a, b in zip(c1, c2))


def colorize_dual(img, target_a_rgb, target_b_rgb, anchor_a_rgb, anchor_b_rgb,
                  full_a=False, full_b=False):
    """双色着色：按到锚点的颜色距离分类，分别用对应的目标色着色"""
    target_a_h, target_a_l, target_a_s = colorsys.rgb_to_hls(
        target_a_rgb[0] / 255.0, target_a_rgb[1] / 255.0, target_a_rgb[2] / 255.0
    )
    target_b_h, target_b_l, target_b_s = colorsys.rgb_to_hls(
        target_b_rgb[0] / 255.0, target_b_rgb[1] / 255.0, target_b_rgb[2] / 255.0
    )

    has_alpha = img.mode == "RGBA"
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            d_a = color_distance((r, g, b), anchor_a_rgb)
            d_b = color_distance((r, g, b), anchor_b_rgb)
            use_a = d_a <= d_b
            if use_a:
                target_h, target_s = target_a_h, target_a_s
                target_l = target_a_l if full_a else None
            else:
                target_h, target_s = target_b_h, target_b_s
                target_l = target_b_l if full_b else None
            if target_l is not None:
                l = target_l
            else:
                _, l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            nr, ng, nb = colorsys.hls_to_rgb(target_h, l, target_s)
            pixels[x, y] = (
                max(0, min(255, round(nr * 255))),
                max(0, min(255, round(ng * 255))),
                max(0, min(255, round(nb * 255))),
                a,
            )

    if not has_alpha:
        img = img.convert("RGB")
    return img


def colorize_anchor(img, target_rgb, anchor_rgb, threshold=2000):
    """单锚点着色：只替换与锚点颜色距离 ≤ threshold 的像素，其余保持不变"""
    target_h, _, target_s = colorsys.rgb_to_hls(
        target_rgb[0] / 255.0, target_rgb[1] / 255.0, target_rgb[2] / 255.0
    )

    has_alpha = img.mode == "RGBA"
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if color_distance((r, g, b), anchor_rgb) <= threshold:
                _, l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
                nr, ng, nb = colorsys.hls_to_rgb(target_h, l, target_s)
                pixels[x, y] = (
                    max(0, min(255, round(nr * 255))),
                    max(0, min(255, round(ng * 255))),
                    max(0, min(255, round(nb * 255))),
                    a,
                )

    if not has_alpha:
        img = img.convert("RGB")
    return img


def colorize_anchor_multiply(img, target_rgb, anchor_rgb, threshold=2000):
    """单锚点着色（Multiply 版）：只替换与锚点颜色距离 ≤ threshold 的像素

    与 colorize_anchor 区别：用 Multiply blend 而非 HLS 着色，
    产生更深更丰富的颜色。其余像素不变。"""
    tr, tg, tb = target_rgb
    has_alpha = img.mode == "RGBA"
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if color_distance((r, g, b), anchor_rgb) <= threshold:
                pixels[x, y] = (
                    r * tr // 255,
                    g * tg // 255,
                    b * tb // 255,
                    a,
                )

    if not has_alpha:
        img = img.convert("RGB")
    return img


def apply_opacity(img, opacity=0.8):
    """将 alpha 通道乘以 opacity 因子 (0~1)，保持 RGB 不变"""
    has_alpha = img.mode == "RGBA"
    if not has_alpha:
        img = img.convert("RGBA")

    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            new_a = max(0, min(255, round(a * opacity)))
            pixels[x, y] = (r, g, b, new_a)

    if not has_alpha:
        img = img.convert("RGB")
    return img


def overlay_color(img, color_rgb, alpha=0.2):
    """将图像与纯色混合: result = img * (1-alpha) + color * alpha"""
    has_alpha = img.mode == "RGBA"
    if not has_alpha:
        img = img.convert("RGBA")

    pixels = img.load()
    cr, cg, cb = color_rgb
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            nr = max(0, min(255, round(r * (1 - alpha) + cr * alpha)))
            ng = max(0, min(255, round(g * (1 - alpha) + cg * alpha)))
            nb = max(0, min(255, round(b * (1 - alpha) + cb * alpha)))
            pixels[x, y] = (nr, ng, nb, a)

    if not has_alpha:
        img = img.convert("RGB")
    return img


def crop_center_top(img, target_w, target_h):
    """从图像顶部居中裁剪出 target_w x target_h 区域"""
    rgba = img.convert("RGBA")
    x = max(0, (rgba.width - target_w) // 2)
    right = min(rgba.width, x + target_w)
    bottom = min(rgba.height, target_h)
    return rgba.crop((x, 0, right, bottom))


# ===== OPPO 工具函数 =====

def resize_canvas(img, new_width, new_height, anchor='center'):
    """图案居中（或指定锚点），画布放大/缩小至 new_width x new_height，透明背景"""
    rgba = img.convert("RGBA")
    canvas = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    x = (new_width - rgba.width) // 2
    y = (new_height - rgba.height) // 2
    if anchor == 'top':
        y = 0
    elif anchor == 'bottom':
        y = new_height - rgba.height
    elif anchor == 'left':
        x = 0
    canvas.paste(rgba, (x, y))
    return canvas


def scale_proportional(img, target_w, target_h):
    """图案等比例缩放至刚好填满 target 尺寸，画布同步缩放"""
    rgba = img.convert("RGBA")
    ratio = min(target_w / rgba.width, target_h / rgba.height)
    new_w = max(1, round(rgba.width * ratio))
    new_h = max(1, round(rgba.height * ratio))
    scaled = rgba.resize((new_w, new_h), Image.LANCZOS)
    return scaled


def change_color_to_ref(img, ref_path, x, y, exclude_white=False):
    """将 img 中非透明（且非白色）像素改为参考图 (x,y) 处的颜色，保留原图亮度"""
    target_rgb = get_color_from_reference(ref_path, x, y)
    target_h, _, target_s = colorsys.rgb_to_hls(
        target_rgb[0] / 255.0, target_rgb[1] / 255.0, target_rgb[2] / 255.0
    )
    has_alpha = img.mode == "RGBA"
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    for py in range(rgba.height):
        for px in range(rgba.width):
            r, g, b, a = pixels[px, py]
            if a == 0:
                continue
            if exclude_white and r > 240 and g > 240 and b > 240:
                continue
            _, l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
            nr, ng, nb = colorsys.hls_to_rgb(target_h, l, target_s)
            pixels[px, py] = (
                max(0, min(255, round(nr * 255))),
                max(0, min(255, round(ng * 255))),
                max(0, min(255, round(nb * 255))),
                a,
            )
    if not has_alpha:
        rgba = rgba.convert("RGB")
    return rgba


def replace_color(img, from_rgb, to_rgb, threshold=30):
    """将 img 中颜色与 from_rgb 相近的像素替换为 to_rgb（保留 alpha）"""
    has_alpha = img.mode == "RGBA"
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    for py in range(rgba.height):
        for px in range(rgba.width):
            r, g, b, a = pixels[px, py]
            if a == 0:
                continue
            if color_distance((r, g, b), from_rgb) <= threshold:
                pixels[px, py] = (to_rgb[0], to_rgb[1], to_rgb[2], a)
    if not has_alpha:
        rgba = rgba.convert("RGB")
    return rgba


# ===== 电池切片函数 =====

def composite_images(base_img, overlay_img):
    """将 overlay_img 合成到 base_img 上方（alpha 合成），返回新 RGBA 图片"""
    base = base_img.convert("RGBA") if base_img.mode != "RGBA" else base_img.copy()
    overlay = overlay_img.convert("RGBA") if overlay_img.mode != "RGBA" else overlay_img
    result = Image.alpha_composite(base, overlay)
    return result


def create_frame_slice(img, frame_idx, total_frames=20):
    """将图片按 x 轴内容宽度均匀切片，只显示前 (frame_idx+1)/total_frames 部分

    扫描所有行找到最左和最右非透明像素，计算内容宽度。
    对第 frame_idx 帧，从 leftmost 到 cut_x 的内容保留，右侧设为透明。
    """
    img_rgba = img.convert("RGBA") if img.mode != "RGBA" else img.copy()
    pixels = img_rgba.load()
    w, h = img_rgba.size

    # 找到内容边界（所有行的最左和最右非透明像素）
    leftmost = w
    rightmost = 0
    for y in range(h):
        for x in range(w):
            _, _, _, a = pixels[x, y]
            if a > 0:
                if x < leftmost:
                    leftmost = x
                if x > rightmost:
                    rightmost = x

    if rightmost <= leftmost:
        # 没有或只有一个非透明像素，返回原图
        return img_rgba

    content_width = rightmost - leftmost
    # 计算切割位置：第 frame_idx 帧（0-based）显示 (frame_idx+1)/total_frames
    cut_x = leftmost + content_width * (frame_idx + 1) // total_frames

    # 将 cut_x 右侧的像素设为透明
    for y in range(h):
        for x in range(cut_x, w):
            r, g, b, a = pixels[x, y]
            if a > 0:
                pixels[x, y] = (r, g, b, 0)

    return img_rgba
