# OPPO 全局配色处理模块
# 按章节实现 OPPO全局.txt 中的全部图像处理操作
import os
from PIL import Image, ImageFilter

from color_toolbox.config import OPPO_COLOR_DEFS, OPPO_BASE_DIR, OPPO_REF_PATH
from color_toolbox.engine import (
    get_color_from_reference, colorize_image_full,
    resize_canvas, scale_proportional, change_color_to_ref, apply_opacity,
    crop_center_top,
)


def _oppo_path(base_dir, *parts):
    return os.path.join(base_dir, OPPO_BASE_DIR, *parts)


def _vivo_path(base_dir, *parts):
    """拼接到 VIVO配色\\01vivo基础 的路径"""
    return os.path.join(base_dir, "VIVO配色", "01vivo基础", *parts)


def _ref_path(base_dir):
    return os.path.join(base_dir, OPPO_REF_PATH)


def _color(base_dir, name):
    """从参考图获取 OPPO_COLOR_DEFS 中定义的颜色"""
    return get_color_from_reference(_ref_path(base_dir), *OPPO_COLOR_DEFS[name])


# ============================================================
# 章节 (8) — 07-控制中心元素（生成颜色变体）
# ============================================================
def process_section_8(base_dir):
    """从07-控制中心元素的 _active 源图生成 _inactive/_unavailable/_anim 等变体"""
    folder = _oppo_path(base_dir, "07-控制中心元素")
    if not os.path.isdir(folder):
        print(f"  [08] 错误：目录不存在 '{folder}'")
        return

    color2 = _color(base_dir, "控制中心颜色2")
    color3 = _color(base_dir, "控制中心颜色3")
    print(f"  控制中心颜色2: RGB{color2}")
    print(f"  控制中心颜色3: RGB{color3}")

    # 构建映射：源文件名 → [(目标文件名, 目标RGB), ...]
    mappings = []

    # ---- status_bar_qs_ 4变体组：_active → _inactive / _unavailable / _anim ----
    qs_4v = [
        "airplane", "alipay", "aliscan", "auto_brigtness", "battery",
        "black_screen", "calculator", "cast", "children", "clean",
        "clock", "data", "dnd", "flashlight", "hotspot",
        "location", "lock", "mute", "nfc", "red_packet",
        "rotation", "smallscreen", "vibrate",
    ]
    # bluetooth 和 wifi 额外有 _off
    qs_5v = ["bluetooth", "wifi"]
    # 无 _anim 组
    qs_3v_no_anim = ["google_now", "no_disturb", "screenshot", "wechat_pay", "wechat_scan"]

    for name in qs_4v:
        src = f"status_bar_qs_{name}_active.png"
        targets = [
            (f"status_bar_qs_{name}_inactive.png", color2),
            (f"status_bar_qs_{name}_unavailable.png", color3),
            (f"status_bar_qs_{name}_anim.png", color3),
        ]
        mappings.append((src, targets))

    for name in qs_5v:
        src = f"status_bar_qs_{name}_active.png"
        targets = [
            (f"status_bar_qs_{name}_inactive.png", color2),
            (f"status_bar_qs_{name}_off.png", color2),
            (f"status_bar_qs_{name}_unavailable.png", color3),
            (f"status_bar_qs_{name}_anim.png", color3),
        ]
        mappings.append((src, targets))

    for name in qs_3v_no_anim:
        src = f"status_bar_qs_{name}_active.png"
        targets = [
            (f"status_bar_qs_{name}_inactive.png", color2),
            (f"status_bar_qs_{name}_unavailable.png", color3),
        ]
        mappings.append((src, targets))

    # ---- 特殊 status_bar_qs_ 组 ----
    # OshareTileService_bg
    mappings.append(("status_bar_qs_OshareTileService_bg_active.png", [
        ("status_bar_qs_OshareTileService_bg_inactive.png", color2),
        ("status_bar_qs_OshareTileService_bg_unavailable.png", color3),
    ]))
    # TVTileService_bg
    mappings.append(("status_bar_qs_TVTileService_bg_active.png", [
        ("status_bar_qs_TVTileService_bg_inactive.png", color2),
        ("status_bar_qs_TVTileService_bg_unavailable.png", color3),
    ]))
    # QuickPanelService (源是 _active，目标是 bg_inactive / bg_unavailable)
    mappings.append(("status_bar_qs_QuickPanelService_active.png", [
        ("status_bar_qs_QuickPanelService_bg_inactive.png", color2),
        ("status_bar_qs_QuickPanelService_bg_unavailable.png", color3),
    ]))
    # WindowsLinkTileService_bg (只有 _unavailable，没有 _inactive)
    mappings.append(("status_bar_qs_WindowsLinkTileService_bg_active.png", [
        ("status_bar_qs_WindowsLinkTileService_bg_unavailable.png", color3),
    ]))
    # eyes._bg (只有 _unavailable，没有 _inactive，也没有 _anim)
    mappings.append(("status_bar_qs_eyes._bg_active.png", [
        ("status_bar_qs_eyes._bg_unavailable.png", color3),
    ]))

    # 仅有 _inactive 的组（源为 _inactive，需要改回颜色1作为源，或者直接从现有 _inactive 生成）
    # 但对于这两种，_inactive 已经是颜色2了，所以不需要生成其他文件
    # multi_system / super_power_save 只有 _inactive，没有其他变体

    # ---- 非 status_bar_qs_ 系列 ----
    mappings.append(("darkmode_on_status_bar.png", [
        ("darkmode_off_status_bar.png", color2),
    ]))
    mappings.append(("dolby_notification_icon_active.png", [
        ("dolby_notification_icon_normal.png", color2),
        ("dolby_notification_icon_unavailable.png", color3),
    ]))
    mappings.append(("osie_notification_active.png", [
        ("osie_notification.png", color2),
        ("osie_notification_unavailable.png", color3),
    ]))
    mappings.append(("screen_share_icon_on.png", [
        ("screen_share_icon_off.png", color2),
    ]))
    mappings.append(("status_bar_screen_temperature_active.png", [
        ("status_bar_screen_temperature.png", color2),
    ]))

    # 这些变体文件应从 108x108 源缩放到 54x54
    SIZE_54_VARIANTS = {
        "dolby_notification_icon_normal.png",
        "osie_notification.png",
        "status_bar_screen_temperature.png",
    }

    # ---- 执行 ----
    generated = 0
    skipped = 0
    for src_name, targets in mappings:
        src_path = os.path.join(folder, src_name)
        if not os.path.exists(src_path):
            print(f"  [08] 警告：源文件不存在 '{src_name}'，跳过")
            skipped += 1
            continue
        with Image.open(src_path) as src_img:
            for dst_name, target_color in targets:
                dst_path = os.path.join(folder, dst_name)
                result = colorize_image_full(src_img.copy(), target_color)
                if dst_name in SIZE_54_VARIANTS:
                    # 先裁出图案（非透明像素），再等比缩放到刚好放进 54x54
                    rgba = result.convert("RGBA")
                    px = rgba.load()
                    rw, rh = rgba.size
                    l, r, t, b = rw, 0, rh, 0
                    for y in range(rh):
                        for x in range(rw):
                            if px[x, y][3] > 0:
                                l = min(l, x); r = max(r, x)
                                t = min(t, y); b = max(b, y)
                    if r > l and b > t:
                        cropped = rgba.crop((l, t, r + 1, b + 1))
                        scaled = scale_proportional(cropped, 54, 54)
                        result = resize_canvas(scaled, 54, 54, anchor='center')
                    else:
                        result = resize_canvas(rgba, 54, 54, anchor='center')
                result.save(dst_path)
                generated += 1
        print(f"  [08] {src_name} → 生成 {len(targets)} 个变体")

    # 无变体的直接复制文件：ic_scene_mode, ic_tile, online_status_bar_eyes, tile_icon_input_method
    # 这些本身没有颜色变体，不需要处理

    print(f"  [08] 完成：生成 {generated} 文件，跳过 {skipped} 源\n")


# ============================================================
# 章节 (9) — 07-控制中心元素
# ============================================================
def _section_9_zoom_content(img, target_84=False):
    """裁剪图案 → 1.05x 缩放 → 返回 zoomed RGBA（不改变画布大小）"""
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    l, r, t, b = w, 0, h, 0
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 0:
                l = min(l, x); r = max(r, x)
                t = min(t, y); b = max(b, y)
    if r > l and b > t:
        cropped = rgba.crop((l, t, r + 1, b + 1))
        cw, ch = cropped.size
        scaled = cropped.resize(
            (max(1, round(cw * 1.05)), max(1, round(ch * 1.05))),
            Image.BICUBIC,
        )
        # 50% 边缘柔化（原图与 SMOOTH 混合，效果减半）
        return Image.blend(scaled, scaled.filter(ImageFilter.SMOOTH), 0.5)
    return rgba


def process_section_9(base_dir):
    """从07-控制中心元素的_active源图出发：裁剪图案→1.05x→着色→全部变体→84x84输出"""
    src_folder = _oppo_path(base_dir, "07-控制中心元素")
    dst_folder = _oppo_path(base_dir, "07-15版本的控制中心元素")
    os.makedirs(dst_folder, exist_ok=True)

    if not os.path.isdir(src_folder):
        print(f"  [09] 错误：源目录不存在 '{src_folder}'")
        return

    color2 = _color(base_dir, "控制中心颜色2")
    color3 = _color(base_dir, "控制中心颜色3")
    print(f"  控制中心颜色2: RGB{color2}")
    print(f"  控制中心颜色3: RGB{color3}")

    # ---- 构建映射：源 (_active) → [(目标名, RGB|None)], None=保持原色 ----
    mappings = []

    def _add(src_name, dst_list):
        mappings.append((src_name, dst_list))

    # status_bar_qs_ 4 变体组
    for name in [
        "airplane", "alipay", "aliscan", "auto_brigtness", "battery",
        "black_screen", "calculator", "cast", "children", "clean",
        "clock", "data", "dnd", "flashlight", "hotspot",
        "location", "lock", "mute", "nfc", "red_packet",
        "rotation", "smallscreen", "vibrate",
    ]:
        _add(f"status_bar_qs_{name}_active.png", [
            (f"status_bar_qs_{name}_active.png", None),
            (f"status_bar_qs_{name}_inactive.png", color2),
            (f"status_bar_qs_{name}_unavailable.png", color3),
            (f"status_bar_qs_{name}_anim.png", color3),
        ])

    for name in ["bluetooth", "wifi"]:
        _add(f"status_bar_qs_{name}_active.png", [
            (f"status_bar_qs_{name}_active.png", None),
            (f"status_bar_qs_{name}_inactive.png", color2),
            (f"status_bar_qs_{name}_off.png", color2),
            (f"status_bar_qs_{name}_unavailable.png", color3),
            (f"status_bar_qs_{name}_anim.png", color3),
        ])

    for name in ["google_now", "no_disturb", "screenshot", "wechat_pay", "wechat_scan"]:
        _add(f"status_bar_qs_{name}_active.png", [
            (f"status_bar_qs_{name}_active.png", None),
            (f"status_bar_qs_{name}_inactive.png", color2),
            (f"status_bar_qs_{name}_unavailable.png", color3),
        ])

    # 特殊 QS
    _add("status_bar_qs_OshareTileService_bg_active.png", [
        ("status_bar_qs_OshareTileService_bg_active.png", None),
        ("status_bar_qs_OshareTileService_bg_inactive.png", color2),
        ("status_bar_qs_OshareTileService_bg_unavailable.png", color3),
    ])
    _add("status_bar_qs_TVTileService_bg_active.png", [
        ("status_bar_qs_TVTileService_bg_active.png", None),
        ("status_bar_qs_TVTileService_bg_inactive.png", color2),
        ("status_bar_qs_TVTileService_bg_unavailable.png", color3),
    ])
    _add("status_bar_qs_QuickPanelService_active.png", [
        ("status_bar_qs_QuickPanelService_active.png", None),
        ("status_bar_qs_QuickPanelService_bg_inactive.png", color2),
        ("status_bar_qs_QuickPanelService_bg_unavailable.png", color3),
    ])
    _add("status_bar_qs_WindowsLinkTileService_bg_active.png", [
        ("status_bar_qs_WindowsLinkTileService_bg_active.png", None),
        ("status_bar_qs_WindowsLinkTileService_bg_unavailable.png", color3),
    ])
    _add("status_bar_qs_eyes._bg_active.png", [
        ("status_bar_qs_eyes._bg_active.png", None),
        ("status_bar_qs_eyes._bg_unavailable.png", color3),
    ])

    # 非 QS
    _add("darkmode_on_status_bar.png", [
        ("darkmode_on_status_bar.png", None),
        ("darkmode_off_status_bar.png", color2),
    ])
    _add("dolby_notification_icon_active.png", [
        ("dolby_notification_icon_active.png", None),
        ("dolby_notification_icon_normal.png", color2),
        ("dolby_notification_icon_unavailable.png", color3),
    ])
    _add("osie_notification_active.png", [
        ("osie_notification_active.png", None),
        ("osie_notification.png", color2),
        ("osie_notification_unavailable.png", color3),
    ])
    _add("screen_share_icon_on.png", [
        ("screen_share_icon_on.png", None),
        ("screen_share_icon_off.png", color2),
    ])
    _add("status_bar_screen_temperature_active.png", [
        ("status_bar_screen_temperature_active.png", None),
        ("status_bar_screen_temperature.png", color2),
    ])

    # ---- 独立文件（无颜色变体，仅 1.05x 缩放后复制） ----
    STANDALONE = {
        "ic_scene_mode.png",
        "ic_tile.png",
        "online_status_bar_eyes.png",
        "tile_icon_input_method.png",
        # 仅有 _inactive 无 _active 源的特殊两项
        "status_bar_qs_multi_system_inactive.png",
        "status_bar_qs_super_power_save_inactive.png",
    }

    # ---- 收集所有将生成的目标文件名，避免重复写入 ----
    generated_targets = set()
    for _, targets in mappings:
        for dst_name, _ in targets:
            generated_targets.add(dst_name)

    # ---- 执行映射 ----
    generated = 0
    skipped = 0
    for src_name, targets in mappings:
        src_path = os.path.join(src_folder, src_name)
        if not os.path.exists(src_path):
            print(f"  [09] 警告：源文件不存在 '{src_name}'，跳过")
            skipped += 1
            continue

        with Image.open(src_path) as img:
            zoomed = _section_9_zoom_content(img)

            for dst_name, target_color in targets:
                dst_path = os.path.join(dst_folder, dst_name)
                if target_color is None:
                    result = zoomed.copy()
                else:
                    result = colorize_image_full(zoomed.copy(), target_color)
                result = resize_canvas(result, 84, 84, anchor='center')
                result.save(dst_path)
                generated += 1

        print(f"  [09] {src_name} → 生成 {len(targets)} 文件")

    # ---- 独立文件直接 1.05x → 84x84 ----
    for fname in STANDALONE:
        src_path = os.path.join(src_folder, fname)
        if not os.path.exists(src_path):
            print(f"  [09] 警告：独立文件不存在 '{fname}'，跳过")
            skipped += 1
            continue
        dst_path = os.path.join(dst_folder, fname)
        with Image.open(src_path) as img:
            zoomed = _section_9_zoom_content(img)
            result = resize_canvas(zoomed, 84, 84, anchor='center')
            result.save(dst_path)
        generated += 1
        print(f"  [09] 独立: {fname} → 1.05x + 84x84")

    print(f"  [09] 完成：生成 {generated} 文件，跳过 {skipped} 源\n")


# ============================================================
# 章节 (11) — 08-状态栏（AOD 数字改色）
# ============================================================
def process_section_11(base_dir):
    """修改 AOD 时钟数字颜色为不可用态"""
    folder = _oppo_path(base_dir, "08-状态栏")
    if not os.path.isdir(folder):
        print(f"  [11] 错误：目录不存在 '{folder}'")
        return

    target_rgb = _color(base_dir, "桌面文字色")

    for i in range(10):
        fname = f"aod_clock_drawable_vertical_{i}.png"
        fpath = os.path.join(folder, fname)
        if not os.path.exists(fpath):
            print(f"  [11] 警告：文件不存在 '{fname}'")
            continue
        with Image.open(fpath) as img:
            result = colorize_image_full(img, target_rgb)
            result.save(fpath)
        print(f"  [11] 已修改: {fname} → RGB{target_rgb}")

    print(f"  [11] 完成\n")


# ============================================================
# 章节 (1) — 01+04设置图标-拨号盘
# ============================================================
def process_section_1(base_dir):
    """时间改色、气泡复制、透明度、裁剪、拨号键等"""
    folder = _oppo_path(base_dir, "01+04设置图标-拨号盘")
    if not os.path.isdir(folder):
        print(f"  [01] 错误：目录不存在 '{folder}'")
        return
    ref = _ref_path(base_dir)

    def _copy(src, dst):
        sp = os.path.join(folder, src); dp = os.path.join(folder, dst)
        if not os.path.exists(sp): return False
        with Image.open(sp) as img: img.save(dp)
        return True

    # --- 时间改色：不可用态 (25,625) ---
    time_list = ["hor_widget_preview.png", "ic_clock_widget_num_colon.png",
        "multi_vertical_preview.png", "one_plus_clock_widget_preview.png",
        "refresh_weather_info.png", "single_hor_widget_preview.png",
        "vertical_widget_preview.png"]
    time_list += [f"ic_clock_widget_num_{i}.png" for i in range(10)]
    for fn in sorted(set(time_list)):
        fp = os.path.join(folder, fn)
        if not os.path.exists(fp):
            print(f"  [01] 警告：时间文件不存在 '{fn}'")
            continue
        with Image.open(fp) as img:
            change_color_to_ref(img, ref, 25, 625).save(fp)
        print(f"  [01] 时间改色: {fn}")

    # --- 气泡复制：coui_bottom_alert_dialog_bg.9.png → 5个 ---
    for dst in ["coui_center_alert_dialog_bg.9.png", "coui_popup_window_bg.9.png",
                "coui_snack_bar_background.9.png", "pb_bg_dial_header_tips.9.png",
                "pb_bg_shape_top_tips.9.png"]:
        if _copy("coui_bottom_alert_dialog_bg.9.png", dst):
            print(f"  [01] 气泡: → {dst}")

    # --- coui_detail_floating_background.9.png → coui_tool_tips_background.9.png ---
    if _copy("coui_detail_floating_background.9.png", "coui_tool_tips_background.9.png"):
        print(f"  [01] 复制: → coui_tool_tips_background.9.png")

    # --- coui_back_arrow_normal.png → 90%(pressed) + 50%(disabled) ---
    arrow_src = os.path.join(folder, "coui_back_arrow_normal.png")
    if os.path.exists(arrow_src):
        with Image.open(arrow_src) as img:
            apply_opacity(img.copy(), 0.5).save(os.path.join(folder, "coui_back_arrow_pressed.png"))
            apply_opacity(img.copy(), 0.5).save(os.path.join(folder, "coui_back_arrow_disabled.png"))
        print(f"  [01] 箭头: → pressed(50%) + disabled(50%)")
    else:
        print(f"  [01] 警告：箭头文件不存在")

    # --- floating_tab_view_button_background.9.png → item ---
    if _copy("floating_tab_view_button_background.9.png", "floating_tab_view_button_item_background.9.png"):
        print(f"  [01] 复制: → floating_tab_view_button_item_background.9.png")

    # --- _selected → _normal + 80%透明度 ---
    sel_pairs = [
        ("pb_dr_business_selected.png", "pb_dr_business_normal.png"),
        ("pb_dr_contacts_selected.png", "pb_dr_contacts_normal.png"),
        ("pb_dr_dialer_selected.png", "pb_dr_dialer_normal.png"),
        ("pb_dr_star_selected.png", "pb_dr_star_normal.png"),
        ("pb_dr_voice_mail_selected.png", "pb_dr_voice_mail_normal.png"),
        ("mms_ic_tab_message_selected.png", "mms_ic_tab_message_normal.png"),
        ("mms_ic_tab_notification_selected.png", "mms_ic_tab_notification_normal.png"),
        ("mms_ic_tab_message_selected_16.png", "mms_ic_tab_message_normal_16.png"),
        ("mms_ic_tab_notification_selected_16.png", "mms_ic_tab_notification_normal_16.png"),
        ("pb_dr_business_selected_16.png", "pb_dr_business_normal_16.png"),
        ("pb_dr_contacts_selected_16.png", "pb_dr_contacts_normal_16.png"),
        ("pb_dr_dialer_selected_16.png", "pb_dr_dialer_normal_16.png"),
        ("pb_dr_star_selected_16.png", "pb_dr_star_normal_16.png"),
        ("pb_dr_voice_mail_selected_16.png", "pb_dr_voice_mail_normal_16.png"),
    ]
    for s, d in sel_pairs:
        sp = os.path.join(folder, s); dp = os.path.join(folder, d)
        if not os.path.exists(sp):
            print(f"  [01] 警告：源不存在 '{s}'"); continue
        with Image.open(sp) as img: apply_opacity(img, 0.5).save(dp)
        print(f"  [01] 50% opacity: {s} → {d}")

    # --- pb_dr_hide_dial_normal.png → pb_ic_hide_dial.png ---
    if _copy("pb_dr_hide_dial_normal.png", "pb_ic_hide_dial.png"):
        print(f"  [01] 复制: → pb_ic_hide_dial.png")

    # --- pb_dr_hide_dial_normal.png → 60%透明度 → pb_dr_hide_dial_pressed.png ---
    hide_pressed_src = os.path.join(folder, "pb_dr_hide_dial_normal.png")
    hide_pressed_dst = os.path.join(folder, "pb_dr_hide_dial_pressed.png")
    if os.path.exists(hide_pressed_src):
        with Image.open(hide_pressed_src) as img:
            apply_opacity(img, 0.6).save(hide_pressed_dst)
        print(f"  [01] 60% opacity: → pb_dr_hide_dial_pressed.png")

    # --- pb_dr_hide_dial_normal.png → 150x150 → pb_ic_floating_dial_show.png ---
    fp_src = os.path.join(folder, "pb_dr_hide_dial_normal.png")
    fp_dst = os.path.join(folder, "pb_ic_floating_dial_show.png")
    if os.path.exists(fp_src):
        with Image.open(fp_src) as img:
            resize_canvas(img, 150, 150, anchor='center').save(fp_dst)
        print(f"  [01] 画布放大150x150: → pb_ic_floating_dial_show.png")

    # --- pb_dr_dial_delete_normal.png → disabled + pressed (80%) ---
    del_src = os.path.join(folder, "pb_dr_dial_delete_normal.png")
    if os.path.exists(del_src):
        for dn in ["pb_dr_dial_delete_disabled.png", "pb_dr_dial_delete_pressed.png"]:
            dp = os.path.join(folder, dn)
            with Image.open(del_src) as img: apply_opacity(img, 0.8).save(dp)
            print(f"  [01] 删除键: → {dn}")

    # --- 拨号键 _normal → _pressed (复制) ---
    key_bases = ["zero","one","two","three","four","five","six","seven","eight","nine"]
    for b in key_bases + ["pound","star"]:
        _copy(f"pb_dr_dial_key_{b}_normal.png", f"pb_dr_dial_key_{b}_pressed.png")
    for b in key_bases:
        _copy(f"pb_dr_dial_key_strokes_{b}_normal.png", f"pb_dr_dial_key_strokes_{b}_pressed.png")

    # --- 裁剪 49x72 顶对齐居中 (拨号键) ---
    crop_72 = [(f"pb_dr_dial_key_{b}_normal.png", f"pb_ic_dial_key_{b}.png") for b in key_bases] + [
        ("pb_dr_dial_key_star_normal.png", "pb_ic_dial_key_star.png"),
        ("pb_dr_dial_key_pound_normal.png", "pb_ic_dial_key_pound.png"),
    ]
    for s, d in crop_72:
        sp = os.path.join(folder, s); dp = os.path.join(folder, d)
        if os.path.exists(sp):
            with Image.open(sp) as img: crop_center_top(img, 49, 72).save(dp)
            print(f"  [01] 49x72 crop: → {d}")

    # --- 裁剪 49x125 顶对齐居中 (笔画键) ---
    for b in key_bases:
        s = f"pb_dr_dial_key_strokes_{b}_normal.png"
        d = f"pb_ic_dial_key_strokes_{b}.png"
        sp = os.path.join(folder, s); dp = os.path.join(folder, d)
        if os.path.exists(sp):
            with Image.open(sp) as img: crop_center_top(img, 49, 125).save(dp)
            print(f"  [01] 49x125 crop: → {d}")

    print(f"  [01] 完成\n")


# ============================================================
# 章节 (2) — 01+04设置图标-拨号盘-14版本
# ============================================================
def process_section_2(base_dir):
    """自动扫描所有 _selected.png → 50%透明度 → _normal.png"""
    folder = _oppo_path(base_dir, "01+04设置图标-拨号盘-14版本")
    if not os.path.isdir(folder):
        print(f"  [02] 错误：目录不存在 '{folder}'"); return

    count = 0
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith("_selected.png"):
            continue
        dst = fn.replace("_selected.png", "_normal.png")
        sp = os.path.join(folder, fn); dp = os.path.join(folder, dst)
        with Image.open(sp) as img:
            apply_opacity(img, 0.5).save(dp)
        print(f"  [02] 50% opacity: {fn} → {dst}")
        count += 1

    if count == 0:
        print(f"  [02] 未找到 _selected.png 文件")
    else:
        print(f"  [02] 完成：处理 {count} 个文件")


# ============================================================
# 章节 (3) — 02-点九色适配
# ============================================================
def _colorize_preserve_9patch(img, target_rgb, is_ninepatch=True):
    """染色，对 .9.png 保留 1 像素九宫格边框（黑色拉伸标记）"""
    rgba = img.convert("RGBA")
    if is_ninepatch:
        px = rgba.load()
        w, h = rgba.size
        border = {}
        for x in range(w):
            border[('t', x)] = px[x, 0]
            border[('b', x)] = px[x, h - 1]
        for y in range(h):
            border[('l', y)] = px[0, y]
            border[('r', y)] = px[w - 1, y]

    result = colorize_image_full(rgba, target_rgb)

    if is_ninepatch:
        rpx = result.load()
        w, h = result.size
        for x in range(w):
            rpx[x, 0] = border[('t', x)]
            rpx[x, h - 1] = border[('b', x)]
        for y in range(h):
            rpx[0, y] = border[('l', y)]
            rpx[w - 1, y] = border[('r', y)]

    return result


def _apply_opacity_preserve_9patch(img, opacity, is_ninepatch=True):
    """应用透明度，对 .9.png 保留 1 像素九宫格边框"""
    rgba = img.convert("RGBA")
    if is_ninepatch:
        px = rgba.load()
        w, h = rgba.size
        border = {}
        for x in range(w):
            border[('t', x)] = px[x, 0]
            border[('b', x)] = px[x, h - 1]
        for y in range(h):
            border[('l', y)] = px[0, y]
            border[('r', y)] = px[w - 1, y]

    result = apply_opacity(rgba, opacity)

    if is_ninepatch:
        rpx = result.load()
        for x in range(w):
            rpx[x, 0] = border[('t', x)]
            rpx[x, h - 1] = border[('b', x)]
        for y in range(h):
            rpx[0, y] = border[('l', y)]
            rpx[w - 1, y] = border[('r', y)]

    return result


# .9.png 边框标准模式（来自检查组参考文件）
_9PATCH_BORDERS = {
    # 会话气泡 (mms) 150x150
    (150, 150): {
        "上": [(71, 72)], "下": [(43, 106)],
        "左": [(73, 74)], "右": [(43, 106)],
    },
    # 会话气泡 (rcs) 137x137 — 下方全宽，右侧有断口
    (137, 137): {
        "上": [(63, 64)], "下": [(1, 135)],
        "左": [(57, 57)], "右": [(1, 95), (108, 135)],
    },
}


def _apply_9patch_border(img, target_size):
    """将标准边框标记应用到图片四周"""
    pattern = _9PATCH_BORDERS.get(target_size)
    if pattern is None:
        return img
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    # 先清空边框
    for x in range(w):
        px[x, 0] = (0, 0, 0, 0)
        px[x, h - 1] = (0, 0, 0, 0)
    for y in range(h):
        px[0, y] = (0, 0, 0, 0)
        px[w - 1, y] = (0, 0, 0, 0)
    # 画黑色标记
    for (start, end) in pattern["上"]:
        for x in range(start, end + 1):
            px[x, 0] = (0, 0, 0, 255)
    for (start, end) in pattern["下"]:
        for x in range(start, end + 1):
            px[x, h - 1] = (0, 0, 0, 255)
    for (start, end) in pattern["左"]:
        for y in range(start, end + 1):
            px[0, y] = (0, 0, 0, 255)
    for (start, end) in pattern["右"]:
        for y in range(start, end + 1):
            px[w - 1, y] = (0, 0, 0, 255)
    return rgba


def _scale_9patch_from_source(src_img, target_w, target_h, anchor='center'):
    """等比例缩放 .9.png 源图，应用标准边框标记"""
    s = scale_proportional(src_img, target_w, target_h)
    result = resize_canvas(s, target_w, target_h, anchor=anchor)
    result = _apply_9patch_border(result, (target_w, target_h))
    return result


def process_section_3(base_dir):
    """全部图片改为点九色，4个例外跳过"""
    folder = _oppo_path(base_dir, "02-点九色适配")
    if not os.path.isdir(folder):
        print(f"  [03] 错误：目录不存在 '{folder}'"); return

    target_rgb = _color(base_dir, "点九色")
    EXCLUDED = {
        "alert_panel_background.9-1.png",
        "launcher_alert_panel_view_bg.9-1.png",
        "switch_themed_loading_unchecked_background.png",
        "switch_themed_unchecked_drawable.png",
    }

    # mms_bg_compose_edit_text.9.png 需要保留内部灰色区域的形状
    # （染色后叠一层10%黑色保持区域区分）
    INNER_OVERLAY_FILES = {
        "mms_bg_compose_edit_text.9.png": {
            "inner_color": (229, 228, 215),
            "overlay_rgb": (0, 0, 0),
            "overlay_alpha": 0.1,
        },
    }

    for fn in sorted(os.listdir(folder)):
        if not fn.lower().endswith(".png"): continue
        fp = os.path.join(folder, fn)
        if fn in EXCLUDED: continue
        is_ninepatch = fn.endswith('.9.png')

        with Image.open(fp) as img:

            # 对特殊文件：染色前记录内部区域mask，染色后叠黑色遮罩
            overlay_info = INNER_OVERLAY_FILES.get(fn)
            if overlay_info:
                rgba = img.convert("RGBA")
                px = rgba.load()
                inner_color = overlay_info["inner_color"]
                mask = set()
                for y in range(rgba.height):
                    for x in range(rgba.width):
                        if px[x, y][3] > 0 and px[x, y][:3] == inner_color:
                            mask.add((x, y))

                # 保存九宫格边框
                if is_ninepatch:
                    w, h = rgba.size
                    border = {}
                    for x in range(w):
                        border[('t', x)] = px[x, 0]
                        border[('b', x)] = px[x, h - 1]
                    for y in range(h):
                        border[('l', y)] = px[0, y]
                        border[('r', y)] = px[w - 1, y]

                # 染色
                result = colorize_image_full(rgba, target_rgb)

                # 恢复九宫格边框
                if is_ninepatch:
                    rpx = result.load()
                    for x in range(w):
                        rpx[x, 0] = border[('t', x)]
                        rpx[x, h - 1] = border[('b', x)]
                    for y in range(h):
                        rpx[0, y] = border[('l', y)]
                        rpx[w - 1, y] = border[('r', y)]

                # 叠黑色遮罩（mask区域）
                rpx = result.load()
                o_r, o_g, o_b = overlay_info["overlay_rgb"]
                oa = overlay_info["overlay_alpha"]
                for (mx, my) in mask:
                    r, g, b, a = rpx[mx, my]
                    rpx[mx, my] = (
                        max(0, min(255, round(r * (1 - oa) + o_r * oa))),
                        max(0, min(255, round(g * (1 - oa) + o_g * oa))),
                        max(0, min(255, round(b * (1 - oa) + o_b * oa))),
                        a,
                    )
                result.save(fp)
                print(f"  [03] 改色+内部遮罩: {fn}")
            else:
                result = _colorize_preserve_9patch(img, target_rgb, is_ninepatch)
                result.save(fp)
                print(f"  [03] 改色: {fn}")

    # 复制：alert_panel_background.9-1.png → launcher_alert_panel_view_bg.9-1.png
    src = os.path.join(folder, "alert_panel_background.9-1.png")
    dst = os.path.join(folder, "launcher_alert_panel_view_bg.9-1.png")
    if os.path.exists(src):
        with Image.open(src) as img: img.save(dst)
        print(f"  [03] 复制: alert → launcher_alert_panel_view_bg.9-1.png")

    print(f"  [03] 完成\n")


# ============================================================
# 章节 (4) — 03-高亮色适配
# ============================================================
def process_section_4(base_dir):
    """复制点九色适配的switch，等比例缩放气泡，改色等"""
    folder = _oppo_path(base_dir, "03-高亮色适配")
    sec1 = _oppo_path(base_dir, "01+04设置图标-拨号盘")
    sec3 = _oppo_path(base_dir, "02-点九色适配")
    ref = _ref_path(base_dir)
    if not os.path.isdir(folder):
        print(f"  [04] 错误：目录不存在 '{folder}'"); return

    # --- 从02-点九色适配复制 switch ---
    cp_from_sec3 = [
        ("switch_themed_loading_unchecked_background.png", "switch_themed_checked_drawable.png"),
        ("switch_themed_unchecked_drawable.png", "switch_themed_loading_checked_background.png"),
    ]
    for s, d in cp_from_sec3:
        sp = os.path.join(sec3, s); dp = os.path.join(folder, d)
        if os.path.exists(sp):
            with Image.open(sp) as img: img.save(dp)
            print(f"  [04] 从02复制: {s} → {d}")

    # --- 从01拨号盘复制气泡 + 等比例缩小 ---
    # coui_alert_dialog_background.9.png → 150x150 → 2个
    alert_src = os.path.join(sec1, "coui_alert_dialog_background.9.png")
    if os.path.exists(alert_src):
        for bn in ["会话气泡mms_bg_send_out_message_normal.9.png",
                    "会话气泡mms_bg_send_out_message_normal_rtl.9.png"]:
            bp = os.path.join(folder, bn)
            with Image.open(alert_src) as img:
                result = _scale_9patch_from_source(img, 150, 150, 'center')
                result.save(bp)
            print(f"  [04] 气泡150x150: → {bn}")

    # 气泡 → 80%透明度 → 2个pressed
    for base_name in ["会话气泡mms_bg_send_out_message_normal.9.png"]:
        base_p = os.path.join(folder, base_name)
        if os.path.exists(base_p):
            for pn in ["会话气泡-按下mms_bg_send_out_message_pressed.9.png",
                       "会话气泡-按下mms_bg_send_out_message_pressed_rtl.9.png"]:
                pp = os.path.join(folder, pn)
                with Image.open(base_p) as img:
                    result = _apply_opacity_preserve_9patch(img, 0.8, True)
                    result.save(pp)
                print(f"  [04] 气泡80%: → {pn}")

    # coui_bottom_alert_dialog_bg.9.png → 137x137 → 2个rcs气泡
    bottom_src = os.path.join(sec1, "coui_bottom_alert_dialog_bg.9.png")
    if os.path.exists(bottom_src):
        for bn in ["会话气泡rcs_bg_send_out_message_normal.9.png",
                    "会话气泡rcs_bg_send_out_message_normal_rtl.9.png"]:
            bp = os.path.join(folder, bn)
            with Image.open(bottom_src) as img:
                result = _scale_9patch_from_source(img, 137, 137, 'center')
                result.save(bp)
            print(f"  [04] rcs气泡137x137: → {bn}")

    # rcs气泡 → 80% → 2个pressed
    for base_name in ["会话气泡rcs_bg_send_out_message_normal.9.png"]:
        base_p = os.path.join(folder, base_name)
        if os.path.exists(base_p):
            for pn in ["会话气泡rcs_bg_send_out_message_pressed.9.png",
                       "会话气泡rcs_bg_send_out_message_pressed_rtl.9.png"]:
                pp = os.path.join(folder, pn)
                with Image.open(base_p) as img:
                    result = _apply_opacity_preserve_9patch(img, 0.8, True)
                    result.save(pp)
                print(f"  [04] rcs气泡80%: → {pn}")

    # --- switch_themed_checked_drawable.png → 画布扩大到114x72 ---
    chk_src = os.path.join(folder, "switch_themed_checked_drawable.png")
    if os.path.exists(chk_src):
        for dn in ["switch_themed_checked_drawable-1.png",
                   "switch_themed_loading_checked_background-1.png"]:
            dp = os.path.join(folder, dn)
            with Image.open(chk_src) as img:
                resize_canvas(img, 114, 72, anchor='center').save(dp)
            print(f"  [04] 画布114x72: → {dn}")

    # switch_themed_checked_drawable-1.png → 80% → switch_themed_checked_disabled.png
    chk1 = os.path.join(folder, "switch_themed_checked_drawable-1.png")
    chk_dis = os.path.join(folder, "switch_themed_checked_disabled.png")
    if os.path.exists(chk1):
        with Image.open(chk1) as img: apply_opacity(img, 0.8).save(chk_dis)
        print(f"  [04] 80%: → switch_themed_checked_disabled.png")

    # switch_themed_loading_checked_background.png → 画布114x72
    lod_src = os.path.join(folder, "switch_themed_loading_checked_background.png")
    lod1 = os.path.join(folder, "switch_themed_loading_checked_background-1.png")
    if os.path.exists(lod_src):
        with Image.open(lod_src) as img:
            resize_canvas(img, 114, 72, anchor='center').save(lod1)
        print(f"  [04] 画布114x72: → switch_themed_loading_checked_background-1.png")

    # --- 改色为浅色 (1030,180) ---
    light_color = _color(base_dir, "浅色")
    for fn in ["coui_touch_search_popup_bg.png",
               "按钮large_main_button_bg_normal.9.png",
               "按钮large_main_button_bg_pressed.9.png",
               "按钮small_main_button_bg_normal.9.png",
               "按钮small_main_button_bg_pressed.9.png"]:
        fp = os.path.join(folder, fn)
        if not os.path.exists(fp):
            print(f"  [04] 警告：文件不存在 '{fn}'"); continue
        with Image.open(fp) as img:
            result = _colorize_preserve_9patch(img, light_color, fn.endswith('.9.png'))
            result.save(fp)
        print(f"  [04] 改色浅色: {fn}")

    # --- 改色为深色 (1030,230) ---
    dark_color = _color(base_dir, "深色")
    for fn in ["提示color_tool_tips_arrow_down.png",
               "提示color_tool_tips_arrow_up.png",
               "提示coui_tool_tips_arrow_left.png",
               "提示coui_tool_tips_arrow_right.png",
               "提示coui_tool_tips_background.9.png"]:
        fp = os.path.join(folder, fn)
        if not os.path.exists(fp):
            print(f"  [04] 警告：文件不存在 '{fn}'"); continue
        with Image.open(fp) as img:
            result = _colorize_preserve_9patch(img, dark_color, fn.endswith('.9.png'))
            result.save(fp)
        print(f"  [04] 改色深色: {fn}")

    # --- 发送信息 透明度50% ---
    for s, d in [("发送信息-发送mms_btn_send_message_normal.png",
                   "发送信息-按下mms_btn_send_message_pressed.png"),
                  ("发送信息-发送rcs_btn_send_message_normal.png",
                   "发送信息-按下rcs_btn_send_message_pressed.png")]:
        sp = os.path.join(folder, s); dp = os.path.join(folder, d)
        if os.path.exists(sp):
            with Image.open(sp) as img: apply_opacity(img, 0.5).save(dp)
            print(f"  [04] 50%: → {d}")

    print(f"  [04] 完成\n")


# ============================================================
# 章节 (5) — 04-高亮色13版本 (不存在则新建)
# ============================================================
def process_section_5(base_dir):
    """从03-高亮色适配复制6个来电图，放大至204x204"""
    src_folder = _oppo_path(base_dir, "03-高亮色适配")
    dst_folder = _oppo_path(base_dir, "04-高亮色13版本")
    os.makedirs(dst_folder, exist_ok=True)
    if not os.path.isdir(src_folder):
        print(f"  [05] 错误：源目录不存在 '{src_folder}'"); return

    files = [
        "来电wifi-拨号incall_btn_vowifi_voice_answer.png",
        "来电-wifi视频incall_btn_vowifi_video_answer.png",
        "来电-拨号incall_btn_voice_answer.png",
        "来电-蓝牙incall_btn_bluetooth_video_answer.png",
        "来电-蓝牙拨号incall_btn_bluetooth_voice_answer.png",
        "来电-视频incall_btn_video_answer.png",
    ]
    for fn in files:
        sp = os.path.join(src_folder, fn); dp = os.path.join(dst_folder, fn)
        if not os.path.exists(sp):
            print(f"  [05] 警告：源不存在 '{fn}'"); continue
        with Image.open(sp) as img:
            s = scale_proportional(img, 204, 204)
            resize_canvas(s, 204, 204, anchor='center').save(dp)
        print(f"  [05] 204x204: {fn}")
    print(f"  [05] 完成\n")


# ============================================================
# 章节 (6) — 06-控制中心
# ============================================================
def process_section_6(base_dir):
    """控制中心大量复制/透明度/重命名/缩放操作"""
    folder = _oppo_path(base_dir, "06-控制中心")
    sec3 = _oppo_path(base_dir, "02-点九色适配")
    if not os.path.isdir(folder):
        print(f"  [06] 错误：目录不存在 '{folder}'"); return

    def _copy(src, dst, src_dir=folder):
        sp = os.path.join(src_dir, src); dp = os.path.join(folder, dst)
        if not os.path.exists(sp): return False
        with Image.open(sp) as img: img.save(dp)
        return True

    # 1) 从02复制switch文件
    for s, d in [("switch_themed_loading_unchecked_background.png",
                   "switch_themed_checked_drawable.png"),
                  ("switch_themed_unchecked_drawable.png",
                   "switch_themed_unchecked_drawable.png")]:
        if _copy(s, d, sec3): print(f"  [06] 从02复制: {s} → {d}")

    # 2) color_toolbar_menu_icon_more_normal.png → 80%(pressed) + 50%(disabled)
    more_src = os.path.join(folder, "color_toolbar_menu_icon_more_normal.png")
    if os.path.exists(more_src):
        for op, name in [(0.8, "pressed"), (0.5, "disabled")]:
            dp = os.path.join(folder, f"color_toolbar_menu_icon_more_{name}.png")
            with Image.open(more_src) as img: apply_opacity(img, op).save(dp)
            print(f"  [06] color_toolbar {name}({int(op*100)}%): →")

    # 3) coui_btn_next_disabled.png → normal + pressed
    for dn in ["coui_btn_next_normal.png", "coui_btn_next_pressed.png"]:
        if _copy("coui_btn_next_disabled.png", dn): print(f"  [06] 复制: → {dn}")

    # 4) coui_toolbar_menu_icon_more_normal.png → 80%(pressed) + 50%(disable)
    #    这个文件可能还不存在（在后续步骤复制），跳过
    cmore_src = os.path.join(folder, "coui_toolbar_menu_icon_more_normal.png")
    if os.path.exists(cmore_src):
        for op, name in [(0.8, "pressed"), (0.5, "disable")]:
            dp = os.path.join(folder, f"coui_toolbar_menu_icon_more_{name}.png")
            with Image.open(cmore_src) as img: apply_opacity(img, op).save(dp)
            print(f"  [06] coui_toolbar {name}({int(op*100)}%): →")

    # 5) 复制+重命名 映射表
    rename_map = [
        ("color_toolbar_menu_icon_more_normal.png", "coui_toolbar_menu_icon_more_normal.png"),
        ("ic_volume_alarm_light.png", "ic_volume_alarm_multi_app_light.png"),
        ("ic_volume_media_grade_0_to_2_light.png", "ic_volume_media_grade_0_to_3_light.png"),
        ("ic_volume_media_grade_0_to_2_light.png", "ic_volume_media_light.png"),
        ("ic_volume_media_grade_2_to_0_light.png", "ic_volume_media_grade_3_to_0_light.png"),
        ("ic_volume_notification_mute_light.png", "ic_volume_notification_on_light.png"),
        ("mms_dr_menu_search.png", "pb_ic_menu_search_disabled.png"),
        ("mms_dr_menu_search.png", "pb_ic_menu_search_normal.png"),
        ("mms_dr_menu_search.png", "pb_ic_menu_search_pressed.png"),
        ("pb_bg_unavaliable_contact.9.png", "status_bar_qs_footer_setting_button_selector.png"),
        ("pb_bg_unavaliable_contact.9.png", "systemui_icon_volume_settings_button.png"),
        ("status_bar_qs_footer_edit_icon.png", "systemui_icon_volume_more.png"),
        ("systemui_icon_volume_settings_media.png", "systemui_icon_volume_settings_system.png"),
        ("ic_volume_media_grade_0_to_2_light.png", "systemui_icon_volume_media.png"),
        ("ic_volume_media_grade_2_to_0_light.png", "systemui_icon_volume_media_mute.png"),
        ("systemui_icon_volume_ringer_mute.png", "systemui_icon_volume_ringer_mute_multi_app.png"),
        ("systemui_icon_volume_ringer_vibrate.png", "systemui_icon_volume_ringer_vibrate_mute.png"),
        ("systemui_icon_volume_ringer_multi_app.png", "systemui_icon_volume_ringer_multi_app_multi_app.png"),
        ("ic_volume_ringer_on_light.png", "systemui_icon_volume_ringer.png"),
    ]
    for s, d in rename_map:
        if _copy(s, d): print(f"  [06] 重命名: → {d}")

    # 6) switch_themed_checked_drawable.png → loading_checked_background
    if _copy("switch_themed_checked_drawable.png", "switch_themed_loading_checked_background.png"):
        print(f"  [06] 复制: → switch_themed_loading_checked_background.png")

    # 7) switch_themed_checked_drawable.png → 画布114x72 → 2个
    chk_src = os.path.join(folder, "switch_themed_checked_drawable.png")
    if os.path.exists(chk_src):
        for dn in ["switch_themed_checked_drawable-1.png",
                   "switch_themed_loading_checked_background-1.png"]:
            dp = os.path.join(folder, dn)
            with Image.open(chk_src) as img:
                resize_canvas(img, 114, 72, anchor='center').save(dp)
            print(f"  [06] 画布114x72: → {dn}")

    # 8) switch_themed_loading_checked_background-1.png → 50% → checked_disabled
    lod1 = os.path.join(folder, "switch_themed_loading_checked_background-1.png")
    chk_dis = os.path.join(folder, "switch_themed_checked_disabled.png")
    if os.path.exists(lod1):
        with Image.open(lod1) as img: apply_opacity(img, 0.5).save(chk_dis)
        print(f"  [06] 50%: → switch_themed_checked_disabled.png")

    # 9) switch_themed_unchecked_drawable.png → 画布114x72 → 2个
    unc_src = os.path.join(folder, "switch_themed_unchecked_drawable.png")
    if os.path.exists(unc_src):
        for dn in ["switch_themed_loading_unchecked_background-1.png",
                   "switch_themed_unchecked_drawable-1.png"]:
            dp = os.path.join(folder, dn)
            with Image.open(unc_src) as img:
                resize_canvas(img, 114, 72, anchor='center').save(dp)
            print(f"  [06] 画布114x72: → {dn}")

    # 10) switch_themed_unchecked_drawable-1.png → 50% → switch_unchecked_disabled.png
    unc1 = os.path.join(folder, "switch_themed_unchecked_drawable-1.png")
    unc_dis = os.path.join(folder, "switch_unchecked_disabled.png")
    if os.path.exists(unc1):
        with Image.open(unc1) as img: apply_opacity(img, 0.5).save(unc_dis)
        print(f"  [06] 50%: → switch_unchecked_disabled.png")

    # 11) 从VIVO复制电池素材
    vivo = _vivo_path(base_dir)
    bat_sources = [
        ("框.png", 53, 30, "stat_battery.png"),
        ("正常.png", 42, 22, "stat_battery_pb.png"),
    ]
    for fn, tw, th, out in bat_sources:
        sp = os.path.join(vivo, fn); dp = os.path.join(folder, out)
        if os.path.exists(sp):
            with Image.open(sp) as img:
                s = scale_proportional(img, tw, th)
                resize_canvas(s, tw, th, anchor='center').save(dp)
            print(f"  [06] 电池: {fn} → {out}")

    print(f"  [06] 完成\n")


# ============================================================
# 章节 (7) — 06-控制中心-15版本
# ============================================================
def process_section_7(base_dir):
    """从06-控制中心复制、画布调整、缩放、重命名"""
    folder = _oppo_path(base_dir, "06-控制中心-15版本")
    sec6 = _oppo_path(base_dir, "06-控制中心")
    vivo = _vivo_path(base_dir)
    if not os.path.isdir(folder):
        print(f"  [07] 错误：目录不存在 '{folder}'"); return

    def _copy(src, dst, src_dir=sec6):
        sp = os.path.join(src_dir, src); dp = os.path.join(folder, dst)
        if not os.path.exists(sp): return False
        with Image.open(sp) as img: img.save(dp)
        return True

    # 1) ic_sysbar_back/home/recent → 画布270x132
    for fn in ["ic_sysbar_back.png", "ic_sysbar_home.png", "ic_sysbar_recent.png"]:
        sp = os.path.join(sec6, fn); dp = os.path.join(folder, fn)
        if os.path.exists(sp):
            with Image.open(sp) as img:
                resize_canvas(img, 270, 132, anchor='center').save(dp)
            print(f"  [07] 270x132: {fn}")

    # 2) status_bar_qs_brightness_icon.png → 1个
    if _copy("status_bar_qs_brightness_icon.png", "status_bar_qs_brightness_icon.png"):
        print(f"  [07] 复制: → status_bar_qs_brightness_icon.png")

    # 3) status_bar_qs_brightness_icon_auto.png → 1个
    if _copy("status_bar_qs_brightness_icon_auto.png", "status_bar_qs_brightness_icon_auto.png"):
        print(f"  [07] 复制: → status_bar_qs_brightness_icon_auto.png")

    # 4) systemui_icon_volume_settings_system_button.png → 居中缩放126x126
    btn_src = os.path.join(sec6, "systemui_icon_volume_settings_system_button.png")
    btn_dst = os.path.join(folder, "status_bar_qs_edit.png")
    if os.path.exists(btn_src):
        with Image.open(btn_src) as img:
            s = scale_proportional(img, 126, 126)
            resize_canvas(s, 126, 126, anchor='center').save(btn_dst)
        print(f"  [07] 126x126: → status_bar_qs_edit.png")

    # 5) status_bar_brightness_normal_icon_sun.png → 缩放72x72
    sun_src = os.path.join(sec6, "status_bar_brightness_normal_icon_sun.png")
    sun_dst = os.path.join(folder, "status_bar_brightness_normal_icon_sun.png")
    if os.path.exists(sun_src):
        with Image.open(sun_src) as img:
            s = scale_proportional(img, 72, 72)
            resize_canvas(s, 72, 72, anchor='center').save(sun_dst)
        print(f"  [07] 72x72: → status_bar_brightness_normal_icon_sun.png")

    # 6) 从VIVO复制电池素材
    vivo_bat = [
        ("电池底.png", 66, 36, "stat_battery_horizontal_bg.png"),
        ("框.png", 66, 36, "stat_battery_horizontal_frame.png"),
        ("正常.png", 66, 36, "stat_battery_horizontal_progress_bg.png"),
    ]
    for fn, tw, th, out in vivo_bat:
        sp = os.path.join(vivo, fn); dp = os.path.join(folder, out)
        if os.path.exists(sp):
            with Image.open(sp) as img:
                s = scale_proportional(img, tw, th)
                resize_canvas(s, tw, th, anchor='center').save(dp)
            print(f"  [07] VIVO电池: {fn} → {out}")

    # 7) 电池底.png → 画布78x48
    bat_bg_src = os.path.join(vivo, "电池底.png")
    bat_bg_dst = os.path.join(folder, "stat_battery_horizontal_percent_out_no_padding_bg.png")
    if os.path.exists(bat_bg_src):
        with Image.open(bat_bg_src) as img:
            resize_canvas(img, 78, 48, anchor='center').save(bat_bg_dst)
        print(f"  [07] 电池底78x48: → stat_battery_horizontal_percent_out_no_padding_bg.png")

    # 8) VIVO图标 → 画布78x48
    for icon_fn, out in [("give_powr_icon.png", "stat_battery_horizontal_out_normal_charge.png"),
                          ("double_powr_icon.png", "stat_battery_horizontal_out_fast_charge.png"),
                          ("fast_powr_icon.png", "stat_battery_horizontal_out_wireless_normal_charge.png")]:
        sp = os.path.join(vivo, icon_fn); dp = os.path.join(folder, out)
        if os.path.exists(sp):
            with Image.open(sp) as img:
                resize_canvas(img, 78, 48, anchor='center').save(dp)
            print(f"  [07] 78x48: {icon_fn} → {out}")

    # 9) VIVO图标 → 居中缩放 画布30x48
    for icon_fn, out in [("give_powr_icon.png", "stat_charge_normal.png"),
                          ("double_powr_icon.png", "stat_charge_super_vooc.png"),
                          ("fast_powr_icon.png", "stat_charge_wireless_normal.png")]:
        sp = os.path.join(vivo, icon_fn); dp = os.path.join(folder, out)
        if os.path.exists(sp):
            with Image.open(sp) as img:
                s = scale_proportional(img, 30, 48)
                resize_canvas(s, 30, 48, anchor='center').save(dp)
            print(f"  [07] 30x48缩放: {icon_fn} → {out}")

    # 10) stat_charge_wireless_vooc.png → 画布78x48
    #     如果不存在则跳过
    for src_n, dst_n, (tw, th), do_scale in [
        ("stat_charge_wireless_vooc.png", "stat_battery_horizontal_out_wireless_fast_charge.png", (78, 48), False),
        ("无线快充.png", "stat_charge_wireless_vooc.png", (30, 48), False),
    ]:
        sp = os.path.join(folder, src_n); dp = os.path.join(folder, dst_n)
        if not os.path.exists(sp): continue
        with Image.open(sp) as img:
            if do_scale:
                s = scale_proportional(img, tw, th)
                resize_canvas(s, tw, th, anchor='center').save(dp)
            else:
                resize_canvas(img, tw, th, anchor='center').save(dp)
        print(f"  [07] 画布{tw}x{th}: {src_n} → {dst_n}")

    # 11) 媒体控制按钮 复制+重命名（源在当前文件夹内）
    media_map = [
        ("ic_notification_control_play.png", "ic_oplus_media_panel_action_play.png"),
        ("ic_notification_control_next.png", "ic_oplus_media_panel_action_next.png"),
        ("ic_notification_has_fav.png", "ic_oplus_media_panel_action_fav.png"),
        ("ic_notification_music_player_like.png", "ic_oplus_media_panel_action_like.png"),
        ("ic_notification_pause.png", "ic_oplus_media_panel_action_pause.png"),
        ("ic_notification_control_prev.png", "ic_oplus_media_panel_action_pre.png"),
    ]
    for s, d in media_map:
        sp = os.path.join(folder, s); dp = os.path.join(folder, d)
        if os.path.exists(sp):
            with Image.open(sp) as img: img.save(dp)
            print(f"  [07] 重命名: {s} → {d}")

    # 12) USB图标改色 (排除白色) → (1025,525) 即控制中心颜色1
    usb_color = get_color_from_reference(_ref_path(base_dir), 1025, 525)
    for fn in ["usb_selection_dialog_menu_charge_icon.png",
               "usb_selection_dialog_menu_file_icon.png",
               "usb_selection_dialog_menu_midi_icon.png",
               "usb_selection_dialog_menu_photo_icon.png",
               "usb_selection_dialog_menu_usb_tethering_icon.png"]:
        fp = os.path.join(folder, fn)
        if not os.path.exists(fp):
            print(f"  [07] 警告：USB文件不存在 '{fn}'"); continue
        with Image.open(fp) as img:
            change_color_to_ref(img, _ref_path(base_dir), 1025, 525, exclude_white=True).save(fp)
        print(f"  [07] USB改色: {fn}")
    # (1025,525) 不在 OPPO_COLOR_DEFS 中，直接使用 get_color_from_reference

    print(f"  [07] 完成\n")


# ============================================================
# 章节 (10) — 08-状态栏15版本 (不存在则新建)
# ============================================================
def process_section_10(base_dir):
    """从08-状态栏15版本复制 stat_* 文件，按08-状态栏标准尺寸缩放/裁切"""
    src_folder = _oppo_path(base_dir, "08-状态栏15版本")
    dst_folder = _oppo_path(base_dir, "08-状态栏")
    if not os.path.isdir(src_folder):
        print(f"  [10] 错误：源目录不存在 '{src_folder}'"); return
    if not os.path.isdir(dst_folder):
        print(f"  [10] 错误：目标目录不存在 '{dst_folder}'"); return

    processed = 0
    skipped = 0
    for fn in sorted(os.listdir(src_folder)):
        if not fn.lower().endswith(".png"):
            continue

        src_path = os.path.join(src_folder, fn)
        dst_path = os.path.join(dst_folder, fn)

        # 读取目标标准尺寸
        if not os.path.exists(dst_path):
            print(f"  [10] 跳过（目标不存在）: {fn}")
            skipped += 1
            continue

        with Image.open(dst_path) as dst_img:
            target_w, target_h = dst_img.size

        with Image.open(src_path) as src_img:
            # 检测实际图案边界（非透明像素）
            px = src_img.load()
            w, h = src_img.size
            left, right, top, bottom = w, 0, h, 0
            for y in range(h):
                for x in range(w):
                    if px[x, y][3] > 0:
                        left = min(left, x)
                        right = max(right, x)
                        top = min(top, y)
                        bottom = max(bottom, y)

            if right <= left or bottom <= top:
                # 全透明或空内容
                result = resize_canvas(src_img, target_w, target_h, anchor='center')
                result.save(dst_path)
                print(f"  [10] 空图: {fn} → {target_w}x{target_h}")
            else:
                content_w = right - left + 1
                content_h = bottom - top + 1
                cropped = src_img.crop((left, top, right + 1, bottom + 1))

                # 阶段一：图案尺寸 ≤ 目标 → 直接居中（不缩放）
                if content_w <= target_w and content_h <= target_h:
                    result = resize_canvas(cropped, target_w, target_h, anchor='center')
                    result.save(dst_path)
                    print(f"  [10] 居中: {fn} (图案{content_w}x{content_h} → {target_w}x{target_h})")
                else:
                    # 阶段二：图案太大 → 等比例缩放到刚好能放下，居中
                    scaled = scale_proportional(cropped, target_w, target_h)
                    result = resize_canvas(scaled, target_w, target_h, anchor='center')
                    result.save(dst_path)
                    print(f"  [10] 缩放+居中: {fn} (图案{content_w}x{content_h} → {result.size[0]}x{result.size[1]} → 画布{target_w}x{target_h})")
            processed += 1

    print(f"  [10] 完成：处理 {processed} 文件，跳过 {skipped} 文件\n")


# ============================================================
# 章节 (12) — OPPO-09音量
# ============================================================
def process_section_12(base_dir):
    """从06-控制中心复制音量图标，画布放大至96x96"""
    folder = _oppo_path(base_dir, "OPPO-09音量")
    sec6 = _oppo_path(base_dir, "06-控制中心")
    if not os.path.isdir(folder):
        print(f"  [12] 错误：目录不存在 '{folder}'"); return

    def _copy_96(src, dst, src_dir=sec6):
        sp = os.path.join(src_dir, src); dp = os.path.join(folder, dst)
        if not os.path.exists(sp): return False
        with Image.open(sp) as img:
            resize_canvas(img, 96, 96, anchor='center').save(dp)
        return True

    # 各组复制映射
    groups = [
        ("ic_volume_alarm_light.png", [
            "ic_volume_alarm_light.png", "ic_volume_alarm_multi_app_light.png",
            "systemui_icon_volume_alarm.png", "systemui_icon_volume_alarm_multi_app.png",
        ]),
        ("ic_volume_media_grade_0_to_2_light.png", [
            "ic_volume_media_grade_0_to_2_light.png", "ic_volume_media_grade_0_to_3_light.png",
            "ic_volume_media_light.png", "systemui_icon_volume_media.png",
            "systemui_icon_volume_media_multi_app.png",
        ]),
        ("ic_volume_media_grade_2_to_0_light.png", [
            "ic_volume_media_grade_2_to_0_light.png", "ic_volume_media_grade_3_to_0_light.png",
            "systemui_icon_volume_media_mute.png", "systemui_icon_volume_media_mute_multi_app.png",
        ]),
        ("ic_volume_ringer_on_light.png", [
            "ic_volume_notification_on_light.png.png",
            "systemui_icon_volume_notification_multi_app.png",
        ]),
        ("systemui_icon_volume_ringer_mute.png", [
            "systemui_icon_volume_notification_mute_multi_app.png",
            "systemui_icon_volume_ringer_mute.png",
            "systemui_icon_volume_ringer_mute_multi_app.png",
        ]),
        ("ic_volume_ringer_vibrate_mute_light.png", [
            "ic_volume_ringer_vibrate_mute_light-1.png",
            "systemui_icon_volume_ringer_vibrate_mute.png",
            "systemui_icon_volume_ringer_vibrate_mute_multi_appe.png",
        ]),
        ("ic_volume_ringer_vibrate_on_light.png", [
            "ic_volume_ringer_vibrate_on_light.png.png",
            "systemui_icon_volume_ringer_vibrate.png",
            "systemui_icon_volume_ringer_vibrate_multi_app.png",
            "systemui_icon_volume_ringer_vibrate-1.png",
        ]),
        ("systemui_icon_volume_bt_sco.png", [
            "systemui_icon_volume_bt_sco.png",
            "systemui_icon_volume_bt_sco_multi_app.png",
        ]),
        ("systemui_icon_volume_accessibility.png", [
            "systemui_icon_volume_accessibility.png",
            "systemui_icon_volume_accessibility_multi_app.png",
        ]),
        ("systemui_icon_volume_media_bt.png", [
            "systemui_icon_volume_media_bt.png",
            "systemui_icon_volume_media_bt_multi_app.png",
        ]),
        ("systemui_icon_volume_media_bt_mute.png", [
            "systemui_icon_volume_media_bt_mute.png",
            "systemui_icon_volume_media_bt_mute_multi_app.png",
        ]),
        ("systemui_icon_volume_voice.png", [
            "systemui_icon_volume_voice.png",
            "systemui_icon_volume_voice_multi_app.png",
        ]),
        ("systemui_icon_volume_wired.png", [
            "systemui_icon_volume_wired.png",
            "systemui_icon_volume_wired_multi_app.png",
        ]),
        ("systemui_icon_volume_wired_mute.png", [
            "systemui_icon_volume_wired_mute.png",
            "systemui_icon_volume_wired_mute_multi_app.png",
        ]),
    ]
    for src, targets in groups:
        for t in targets:
            if _copy_96(src, t):
                print(f"  [12] 96x96: {src} → {t}")

    # systemui_icon_volume_settings_system_button.png → 画布156x156
    btn_src = os.path.join(sec6, "systemui_icon_volume_settings_system_button.png")
    btn_dst = os.path.join(folder, "systemui_icon_volume_settings_system_button.png")
    if os.path.exists(btn_src):
        with Image.open(btn_src) as img:
            resize_canvas(img, 156, 156, anchor='center').save(btn_dst)
        print(f"  [12] 156x156: → systemui_icon_volume_settings_system_button.png")

    # ic_volume_media_grade_0_to_2_light.png → 居中缩放94x74 + 画布144x144
    media_src = os.path.join(sec6, "ic_volume_media_grade_0_to_2_light.png")
    media_dst = os.path.join(folder, "systemui_icon_volume_settings_system.png")
    if os.path.exists(media_src):
        with Image.open(media_src) as img:
            s = scale_proportional(img, 94, 74)
            resize_canvas(s, 144, 144, anchor='center').save(media_dst)
        print(f"  [12] 94x74+144x144: → systemui_icon_volume_settings_system.png")

    # 文档中还有两条（行342-343），但 source 在 folder 内或 sec6
    # ic_volume_ringer_on_light.png → 2个multi_app (源在当前folder? 看行342是在folder内)
    ring_src1 = os.path.join(folder, "ic_volume_ringer_on_light.png")
    if not os.path.exists(ring_src1):
        ring_src1 = os.path.join(sec6, "ic_volume_ringer_on_light.png")
    for rn in ["ic_volume_ringer_vibrate_on_light.png",
               "systemui_icon_volume_ringer_multi_app.png",
               "systemui_icon_volume_ringer_multi_app_multi_app.png"]:
        rp = os.path.join(folder, rn)
        if os.path.exists(ring_src1):
            with Image.open(ring_src1) as img:
                resize_canvas(img, 96, 96, anchor='center').save(rp)
            print(f"  [12] 96x96: ic_volume_ringer_on_light → {rn}")

    # more_row_stream_app.png → 居中缩放91x98 + 画布144x144
    more_src = os.path.join(folder, "more_row_stream_app.png")
    more_dst = os.path.join(folder, "systemui_icon_volume_settings_media.png")
    if os.path.exists(more_src):
        with Image.open(more_src) as img:
            s = scale_proportional(img, 91, 98)
            resize_canvas(s, 144, 144, anchor='center').save(more_dst)
        print(f"  [12] 91x98+144x144: → systemui_icon_volume_settings_media.png")

    print(f"  [12] 完成\n")


# ============================================================
# 主入口
# ============================================================
def process_oppo_tasks(base_dir):
    """按顺序执行全部 OPPO 章节处理"""
    print("正在处理 OPPO 全局配色...")
    print()
    print("--- (1) 01+04设置图标-拨号盘 ---")
    process_section_1(base_dir)
    print("--- (2) 01+04设置图标-拨号盘-14版本 ---")
    process_section_2(base_dir)
    print("--- (3) 02-点九色适配 ---")
    process_section_3(base_dir)
    print("--- (4) 03-高亮色适配 ---")
    process_section_4(base_dir)
    print("--- (5) 04-高亮色13版本 ---")
    process_section_5(base_dir)
    print("--- (6) 06-控制中心 ---")
    process_section_6(base_dir)
    print("--- (7) 06-控制中心-15版本 ---")
    process_section_7(base_dir)
    print("--- (8) 07-15版本的控制中心元素 ---")
    process_section_8(base_dir)
    print("--- (9) 07-控制中心元素 ---")
    process_section_9(base_dir)
    print("--- (10) 08-状态栏15版本 ---")
    process_section_10(base_dir)
    print("--- (11) 08-状态栏 (AOD数字) ---")
    process_section_11(base_dir)
    print("--- (12) OPPO-09音量 ---")
    process_section_12(base_dir)
