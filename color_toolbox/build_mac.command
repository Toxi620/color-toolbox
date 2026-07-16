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
echo "--- 清理 ---"
rm -rf "$PKG_DIR/build" "$PKG_DIR/__pycache__"
rm -f "$PKG_DIR/配色工具.spec" "$PKG_DIR/配色工具_无OPPO.spec"

echo ""
echo "========================================"
echo " 打包完成！"
ls -lh "$PARENT_DIR/配色工具"* 2>/dev/null
echo "========================================"
