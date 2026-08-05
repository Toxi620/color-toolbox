# 配置数据：颜色定义、目标文件列表、双色/锚点配置
# 如需新增颜色或目标文件，在此文件修改即可

# ===== 五种颜色在参考图中的取色坐标 =====
COLOR_DEFS = {
    "浅色": (1030, 180),
    "深色": (1030, 230),
    "主高亮色": (1030, 280),
    "光圈色": (1030, 1030),
    "按钮火箭色": (1030, 330),
}

# 使用目标色完整 HLS（含亮度），不保留原图亮度
FULL_COLOR_COLORS = {"主高亮色", "浅色", "深色"}

# ===== 按文件名强制完整 HLS 着色（替换 H+S+L） =====
# 某些图片不需要保留原图亮度，强制用 colorize_image_full
FULL_COLOR_FILES = {"widget_guide_open_bg.png", "aftertwentysencondspause.png"}

# ===== 色相+叠加着色配置 =====
# 先 HLS 改色相（保留原图亮度），再叠加目标色增加饱和度
HUE_OVERLAY_COLORS = {"光圈色"}
HUE_OVERLAY_ALPHA = 0.3  # 叠加透明度，越大颜色越深越饱和

# ===== 可能的原子组件文件夹名称 =====
POSSIBLE_SUBDIRS = ["VIVO蓝色原子组件", "VIVO蓝黑色原子组件"]

# ===== 目标文件 =====
# 格式：颜色名 → [(子文件夹, 文件名), ...]
TARGET_FILES = {
    "浅色": [
        ("01com.vivo.widget.calendar 日程", "a_launcher_white_background.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_widget_view_bg_light.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "shape_corner_bg_5_light.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "shape_corner_bg_ex_light.png"),
    ],
    "深色": [
        ("01com.vivo.widget.calendar 日程", "a_launcher_black_background.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_widget_view_bg.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "shape_corner_bg_5.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "shape_corner_bg_ex.png"),
    ],
    "光圈色": [
        # ---- 02一键清理 ----
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud1.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud1_light.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud2.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud2_light.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud3.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud3_light.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud4.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_cloud4_light.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket_fire_big.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket_fire_big_light.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket_fire_small.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket_fire_small_light.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket_jet.png"),
        ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket_jet-1.png"),
        # ---- 03屏幕使用时间 ----
        ("03com.vivo.widget.timemanager 屏幕使用时间", "wave_anim_background.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "wave_anim_background_light.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "wave_anim_foreground.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "wave_anim_foreground_light.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "wave_anim_light.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "wave_anim_light-1.png"),
        # ---- 06计时器 ----
        ("06com.vivo.countdownwidget 计时器", "static_start.png"),
    ],
    "主高亮色": [
        # ---- 01日程 ----
        ("01com.vivo.widget.calendar 日程", "ic_coffee.png"),
        ("01com.vivo.widget.calendar 日程", "ic_no_schedule.png"),
        ("01com.vivo.widget.calendar 日程", "ic_add_schedule.png"),
        ("01com.vivo.widget.calendar 日程", "voice_image.png"),
        ("01com.vivo.widget.calendar 日程", "ic_create_event_a1.png"),
        ("01com.vivo.widget.calendar 日程", "ic_create_event_night_a1.png"),
        # ---- 03屏幕使用时间 ----
        ("03com.vivo.widget.timemanager 屏幕使用时间", "widget_guide_middle_bg.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "widget_guide_middle_bg_5.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "widget_guide_middle_bg_5-1.png"),
        ("03com.vivo.widget.timemanager 屏幕使用时间", "widget_guide_middle_bg_light.png"),
        # ---- 05录音（排除双色图 + aftertwentysencondspause.png） ----
        ("05com.android.bbksoundrecorder 录音", "aftertwentysenconds.png"),
        ("05com.android.bbksoundrecorder 录音", "label.png"),
        ("05com.android.bbksoundrecorder 录音", "label_black.png"),
        ("05com.android.bbksoundrecorder 录音", "mark_two.png"),
        ("05com.android.bbksoundrecorder 录音", "mark_two_black.png"),
        ("05com.android.bbksoundrecorder 录音", "saverecording.png"),
        ("05com.android.bbksoundrecorder 录音", "saverecording_black.png"),
        ("05com.android.bbksoundrecorder 录音", "save_two.png"),
        ("05com.android.bbksoundrecorder 录音", "save_two_black.png"),
        # ---- 06计时器（排除双色图 + static_start.png） ----
        ("06com.vivo.countdownwidget 计时器", "center_mark_line.png"),
        ("06com.vivo.countdownwidget 计时器", "center_mark_line_night.png"),
        ("06com.vivo.countdownwidget 计时器", "center_mark_point.png"),
        ("06com.vivo.countdownwidget 计时器", "center_mark_point_night.png"),
        ("06com.vivo.countdownwidget 计时器", "pause_to_start.png"),
        ("06com.vivo.countdownwidget 计时器", "static_pause.png"),
    ],
    "按钮火箭色": [
        # ---- 03屏幕使用时间 ----
        ("03com.vivo.widget.timemanager 屏幕使用时间", "widget_guide_open_bg.png"),
        # ---- 05录音 ----
        ("05com.android.bbksoundrecorder 录音", "aftertwentysencondspause.png"),
    ],
}


# ===== 双色替换配置（锚点坐标法） =====
# 格式: (子文件夹, 文件名): (目标色A, x1, y1, 目标色B, x2, y2)
DUAL_COLORS = {
    # ---- 05录音 ----
    ("05com.android.bbksoundrecorder 录音", "goingon.png"):
        ("浅色", 60, 57, "主高亮色", 53, 48),
    ("05com.android.bbksoundrecorder 录音", "goingon_black.png"):
        ("深色", 60, 57, "主高亮色", 53, 48),
    ("05com.android.bbksoundrecorder 录音", "initplay.png"):
        ("浅色", 77, 75, "主高亮色", 106, 106),
    ("05com.android.bbksoundrecorder 录音", "initplay_black.png"):
        ("深色", 77, 75, "主高亮色", 106, 106),
    ("05com.android.bbksoundrecorder 录音", "pausemiddle.png"):
        ("浅色", 60, 57, "主高亮色", 53, 48),
    ("05com.android.bbksoundrecorder 录音", "pausemiddle_black.png"):
        ("深色", 60, 57, "主高亮色", 53, 48),
    ("05com.android.bbksoundrecorder 录音", "record_background.png"):
        ("浅色", 100, 100, "主高亮色", 63, 60),
    ("05com.android.bbksoundrecorder 录音", "record_background_black.png"):
        ("深色", 100, 100, "主高亮色", 63, 60),
    ("05com.android.bbksoundrecorder 录音", "record_start.png"):
        ("浅色", 60, 57, "主高亮色", 53, 48),
    ("05com.android.bbksoundrecorder 录音", "record_start_black.png"):
        ("深色", 60, 57, "主高亮色", 53, 48),
    # ---- 06计时器 ----
    ("06com.vivo.countdownwidget 计时器", "button_background.png"):
        ("浅色", 193, 180, "主高亮色", 100, 100),
    ("06com.vivo.countdownwidget 计时器", "button_background_night.png"):
        ("深色", 193, 181, "主高亮色", 100, 100),
    ("06com.vivo.countdownwidget 计时器", "reset_button.png"):
        ("浅色", 175, 182, "主高亮色", 110, 93),
    ("06com.vivo.countdownwidget 计时器", "reset_button_night.png"):
        ("深色", 175, 182, "主高亮色", 110, 93),
}


# ===== 单锚点替换配置 =====
ANCHOR_THRESHOLD = 2000
ANCHOR_COLORS = {
    # ---- 02一键清理 ----
    ("02com.vivo.widget.cleanspeed 一键清理", "clean_lightning.png"): ("按钮火箭色", 11, 19),
    ("02com.vivo.widget.cleanspeed 一键清理", "clean_normal.png"): ("按钮火箭色", 12, 24),
    ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket.png"): ("按钮火箭色", 78, 55),
    ("02com.vivo.widget.cleanspeed 一键清理", "clean_rocket_light.png"): ("按钮火箭色", 78, 55),
    ("02com.vivo.widget.cleanspeed 一键清理", "clean_shield.png"): ("按钮火箭色", 79, 69),
    ("02com.vivo.widget.cleanspeed 一键清理", "clean_shield_light.png"): ("按钮火箭色", 79, 69),
}


# ===== 80% 透明度复制+重命名任务 =====
OPACITY_80_TASKS = [
    # ---- VIVO配色 / 01vivo基础 ----
    ("VIVO配色/01vivo基础", "bbk_dialer_del.png", "bbk_dialer_del_gray.png"),
    ("VIVO配色/01vivo基础", "dialer_ic_theme_os2_bbk_dialer_call.png", "dialer_ic_theme_os2_bbk_dialer_call_press.png"),
    ("VIVO配色/01vivo基础", "ic_bbk_dialer_open_dialpad.png", "ic_bbk_dialer_open_dialpad_sel.png"),
    ("VIVO配色/01vivo基础", "theme_bottom_collect_sel.png", "theme_bottom_collect_default.png"),
    ("VIVO配色/01vivo基础", "theme_bottom_contact_sel.png", "theme_bottom_contact_default.png"),
    ("VIVO配色/01vivo基础", "theme_bottom_dialer_sel.png", "theme_bottom_dialer_default.png"),
]

# ===== 60% 透明度复制+重命名任务（华为点九按压态） =====
OPACITY_60_TASKS = [
    # ---- 华为配色 / 华为点九 (规则1: 追加 _press) ----
    ("华为配色/华为点九", "dial_num_0_blk.png", "dial_num_0_blk_press.png"),
    ("华为配色/华为点九", "dial_num_1_blk.png", "dial_num_1_blk_press.png"),
    ("华为配色/华为点九", "dial_num_2_blk.png", "dial_num_2_blk_press.png"),
    ("华为配色/华为点九", "dial_num_3_blk.png", "dial_num_3_blk_press.png"),
    ("华为配色/华为点九", "dial_num_4_blk.png", "dial_num_4_blk_press.png"),
    ("华为配色/华为点九", "dial_num_5_blk.png", "dial_num_5_blk_press.png"),
    ("华为配色/华为点九", "dial_num_6_blk.png", "dial_num_6_blk_press.png"),
    ("华为配色/华为点九", "dial_num_7_blk.png", "dial_num_7_blk_press.png"),
    ("华为配色/华为点九", "dial_num_8_blk.png", "dial_num_8_blk_press.png"),
    ("华为配色/华为点九", "dial_num_9_blk.png", "dial_num_9_blk_press.png"),
    # ---- 华为配色 / 华为点九 (规则2: 追加 press, 无下划线) ----
    ("华为配色/华为点九", "jing.png", "jingpress.png"),
    ("华为配色/华为点九", "xing.png", "xingpress.png"),
]

# ===== 纯色叠加任务 =====
OVERLAY_TASKS = [
    # (rel_dir, src, dst, color_rgb, alpha)
    ("华为配色/华为点九", "scrubber_control_normal_emui.png",
     "scrubber_control_disabled_emui.png", (255, 255, 255), 0.2),
    ("华为配色/华为点九", "scrubber_control_normal_emui.png",
     "scrubber_control_pressed_emui.png", (0, 0, 0), 0.2),
]

# ===== 纯复制重命名任务 =====
COPY_RENAME_TASKS = [
    # ---- 荣耀状态栏 / 规则1: _on → _off ----
    ("荣耀状态栏", "ic_airplanemode_tile_on.png", "ic_airplanemode_tile_off.png"),
    ("荣耀状态栏", "ic_busymode_tile_on.png", "ic_busymode_tile_off.png"),
    ("荣耀状态栏", "ic_eyecomfort_tile_on.png", "ic_eyecomfort_tile_off.png"),
    ("荣耀状态栏", "ic_flashlight_tile_on.png", "ic_flashlight_tile_off.png"),
    ("荣耀状态栏", "ic_gps_tile_on.png", "ic_gps_tile_off.png"),
    ("荣耀状态栏", "ic_instantshare_tile_on.png", "ic_instantshare_tile_off.png"),
    ("荣耀状态栏", "ic_motion_ebook_on.png", "ic_motion_ebook_off.png"),
    ("荣耀状态栏", "ic_motion_extra_dim_on.png", "ic_motion_extra_dim_off.png"),
    ("荣耀状态栏", "ic_motion_relieve_car_sickness_auto_mode_off_to_offcar.png", "ic_motion_relieve_car_sickness_auto_mode_offcar_to_off.png"),
    ("荣耀状态栏", "ic_relieve_car_sickness_auto_on.png", "ic_relieve_car_sickness_auto_off.png"),
    ("荣耀状态栏", "ic_wireless_projection_on.png", "ic_wireless_projection_off.png"),
    # ---- 荣耀状态栏 / 规则1 特例 ----
    ("荣耀状态栏", "ic_superpowermode_tile_def.png", "ic_superpowermode_tile_disable.png"),
    # ---- 荣耀状态栏 / 规则2: _on → _off + _disable ----
    ("荣耀状态栏", "ic_dataswitch_tile_on.png", "ic_dataswitch_tile_off.png"),
    ("荣耀状态栏", "ic_dataswitch_tile_on.png", "ic_dataswitch_tile_disable.png"),
    ("荣耀状态栏", "ic_hotspot_tile_on.png", "ic_hotspot_tile_off.png"),
    ("荣耀状态栏", "ic_hotspot_tile_on.png", "ic_hotspot_tile_disable.png"),
    ("荣耀状态栏", "ic_lowpowermode_tile_on.png", "ic_lowpowermode_tile_off.png"),
    ("荣耀状态栏", "ic_lowpowermode_tile_on.png", "ic_lowpowermode_tile_disable.png"),
    ("荣耀状态栏", "ic_suspendtasks_tile_on.png", "ic_suspendtasks_tile_off.png"),
    ("荣耀状态栏", "ic_suspendtasks_tile_on.png", "ic_suspendtasks_tile_disable.png"),
    # ---- 荣耀状态栏 / 规则2 特例 (nfc: 4 种变体) ----
    ("荣耀状态栏", "ic_nfc_tile_on.png", "ic_nfc_tile_off.png"),
    ("荣耀状态栏", "ic_nfc_tile_on.png", "ic_nfc_tile_disable.png"),
    ("荣耀状态栏", "ic_nfc_tile_on.png", "ic_nfc_tile_process.png"),
]

# ===== 电池切片制作配置 =====
BATTERY_SOURCE_DIR = "VIVO配色/01vivo基础"
BATTERY_OUTPUT_DIR = "VIVO配色/04电池切片"

# (type_name, fill_base)  fill_base 用于非 bg 版本
BATTERY_TYPES = [
    ("double_powr", "正常"), ("fast_powr", "正常"), ("give_powr", "正常"),
    ("low_powr", "正常"), ("nornal_powr", "正常"), ("save_powr", "省电"),
]

# (output_prefix, fill_00_03, fill_04_19)
BATTERY_SLICE_SERIES = [
    ("vivo_battery_20", "低电量", "正常"),
    ("vivo_save_mode_battery_20", "低电量", "省电"),
    ("vivo_battery_percent_in_20", "低电量", "正常"),
]

# (output_prefix, icon_name, icon_width, fill_04_19)
# fill_04_19 为 None 表示用"正常"
BATTERY_CHARGE_SERIES = [
    ("vivo_battery_charge_20", "give_powr_icon", 18, None),
    ("vivo_battery_engine_charge_20", "double_powr_icon", 30, None),
    ("vivo_battery_flash_charge_20", "fast_powr_icon", 33, None),
    ("vivo_save_mode_battery_charge_20", "double_powr_icon", 30, "省电"),
    ("vivo_battery_percent_in_charge_20", "give_powr_icon", 18, None),
]

# 有图标的类型（前 3 种）
BATTERY_ICON_TYPES = ["double_powr", "fast_powr", "give_powr"]

# ===== OPPO 全局配色配置 =====
OPPO_BASE_DIR = "OPPO全局配色"
OPPO_REF_PATH = "全局配色.png"

# OPPO 取色坐标（全局配色.png）
OPPO_COLOR_DEFS = {
    "点九色": (25, 25),
    "不可用态": (25, 1180),
    "浅色": (1030, 180),
    "深色": (1030, 230),
    "主高亮色": (1030, 280),
    "控制中心颜色1": (25, 525),
    "控制中心颜色2": (25, 575),
    "控制中心颜色3": (25, 625),
    "桌面文字色": (25, 1125),
}
