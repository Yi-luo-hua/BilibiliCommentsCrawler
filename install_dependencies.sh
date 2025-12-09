#!/bin/bash

echo ""
echo "========================================"
echo "  B站评论爬虫工具 - 依赖安装脚本"
echo "========================================"
echo ""

# 检查 Python
echo "正在检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PIP_CMD=pip
else
    echo "[错误] 未找到 Python，请先安装 Python 3.8 或更高版本"
    exit 1
fi

$PYTHON_CMD --version
echo ""

# 安装依赖
echo "正在安装依赖包..."
echo ""
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "  ✓ 依赖安装成功！"
    echo "========================================"
    echo ""
    echo "正在验证安装..."
    $PYTHON_CMD -c "import requests, pandas, customtkinter; print('所有依赖已正确安装！')"
    echo ""
    echo "现在可以运行 $PYTHON_CMD main.py 启动程序了"
else
    echo ""
    echo "========================================"
    echo "  ✗ 依赖安装失败"
    echo "========================================"
    echo ""
    echo "请尝试以下方法："
    echo "1. 使用 sudo 权限运行: sudo $PIP_CMD install -r requirements.txt"
    echo "2. 或手动运行: $PIP_CMD install --user -r requirements.txt"
fi

echo ""
