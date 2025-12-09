@echo off
chcp 65001 > nul
cd /d "%~dp0"
python main.py
if %errorlevel% neq 0 (
    echo.
    echo 程序异常退出，请查看上方错误信息
    pause
)
