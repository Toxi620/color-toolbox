#!/bin/bash
# macOS 构建脚本 — 配色工具
# 放在 color_toolbox/ 内，直接双击运行

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PKG_DIR="$PARENT_DIR/color_toolbox"

if [ ! -d "$PKG_DIR" ]; then
    echo "错误：找不到 $PKG_DIR"
    exit 1
fi

# 检查/安装 PyInstaller
if ! command -v pyinstaller &>/dev/null; then
    echo "PyInstaller 未安装，正在安装..."
    pip3 install pyinstaller
fi

echo "========================================"
echo " 配色工具 — macOS 打包"
echo "========================================"

echo ""
echo "--- 打包：配色工具（含 OPPO）---"
pyinstaller --onefile --console \
    --name "配色工具" \
    --distpath "$PARENT_DIR" \
    --add-data "$PKG_DIR:color_toolbox" \
    --workpath "$PKG_DIR/build/pyinstaller_main" \
    --specpath "$PKG_DIR" \
    "$PKG_DIR/main.py"

echo ""
echo "--- 打包：配色工具_无OPPO ---"
pyinstaller --onefile --console \
    --name "配色工具_无OPPO" \
    --distpath "$PARENT_DIR" \
    --add-data "$PKG_DIR:color_toolbox" \
    --workpath "$PKG_DIR/build/pyinstaller_no_oppo" \
    --specpath "$PKG_DIR" \
    "$PKG_DIR/main_no_oppo.py"

echo ""
echo "========================================"
echo " 创建 .app 包裹..."
echo "========================================"

create_app_bundle() {
    local exe_name="$1"
    local app_name="${exe_name}.app"
    local exe_path="$PARENT_DIR/$exe_name"
    local app_dir="$PARENT_DIR/$app_name"

    if [ ! -f "$exe_path" ]; then
        echo "  跳过：$exe_name 不存在"
        return
    fi

    rm -rf "$app_dir"
    mkdir -p "$app_dir/Contents/MacOS"

    # 复制可执行文件到 .app 内
    cp "$exe_path" "$app_dir/Contents/MacOS/$exe_name"

    # 创建启动包装脚本（launcher 作为入口，固定指向当前 exe）
    cat > "$app_dir/Contents/MacOS/launcher" << LAUNCHER_EOF
#!/bin/bash
DIR="\$(cd "\$(dirname "\$0")" && pwd)"
EXE="\$DIR/${exe_name}"

if [ -n "\$TERM_PROGRAM" ] || [ -n "\$TERM" ]; then
    exec "\$EXE"
else
    osascript -e "tell application \"Terminal\" to activate" \\
              -e "tell application \"Terminal\" to do script \"clear && echo '=== 配色工具 ===' && cd '\${DIR}' && exec '\${EXE}'\""
fi
LAUNCHER_EOF
    chmod +x "$app_dir/Contents/MacOS/launcher"
    chmod +x "$app_dir/Contents/MacOS/$exe_name"

    # 创建 PkgInfo
    echo "APPL????" > "$app_dir/Contents/PkgInfo"

    # 创建 Info.plist
    cat > "$app_dir/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleDisplayName</key>
    <string>${exe_name}</string>
    <key>CFBundleName</key>
    <string>${exe_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.colortoolbox.${exe_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
</dict>
</plist>
EOF

    echo "  ✅ $app_name 创建完成"
}

create_app_bundle "配色工具"
create_app_bundle "配色工具_无OPPO"

echo ""
echo "--- 删除裸可执行文件（只保留 .app）---"
rm -f "$PARENT_DIR/配色工具" "$PARENT_DIR/配色工具_无OPPO"

echo ""
echo "--- 清理 ---"
rm -rf "$PKG_DIR/build" "$PKG_DIR/__pycache__"
rm -f "$PKG_DIR/配色工具.spec" "$PKG_DIR/配色工具_无OPPO.spec"

echo ""
echo "========================================"
echo " 打包完成！"
ls -lh "$PARENT_DIR/配色工具"* 2>/dev/null
echo "========================================"
