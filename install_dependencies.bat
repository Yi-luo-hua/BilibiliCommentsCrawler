@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   B站评论爬虫工具 - 依赖安装脚本
echo ========================================
echo.
echo 正在检查 Python 环境...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.8 或更高版本
    echo.
    pause
    exit /b 1
)

python --version
echo.
echo 正在安装依赖包...
echo.
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   ✓ 依赖安装成功！
    echo ========================================
    echo.
    echo 正在验证安装...
    python -c "import requests, pandas, customtkinter; print('所有依赖已正确安装！')"
    echo.
    echo 现在可以运行 python main.py 启动程序了
) else (
    echo.
    echo ========================================
    echo   ✗ 依赖安装失败
    echo ========================================
    echo.
    echo 请尝试以下方法：
    echo 1. 使用管理员权限运行此脚本
    echo 2. 或手动运行: pip install --user -r requirements.txt
    echo 3. 或手动运行: pip3 install -r requirements.txt
)

echo.
pause
