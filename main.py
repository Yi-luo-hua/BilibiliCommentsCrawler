"""
B站评论爬虫工具 - 主程序入口
"""
import sys
import os

import tkinter as tk
from tkinter import messagebox

def show_error_and_exit(title, message):
    """显示错误弹窗并退出"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()
    sys.exit(1)

def check_dependencies():
    """检查必要的依赖是否已安装"""
    missing_packages = []
    required_packages = {
        'requests': 'requests',
        'pandas': 'pandas',
        'bs4': 'beautifulsoup4',
        'lxml': 'lxml',
        'customtkinter': 'customtkinter'
    }
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        error_msg = (
            "❌ 缺少必要的依赖包!\n\n"
            f"缺少的包: {', '.join(missing_packages)}\n\n"
            "请运行以下命令安装:\n"
            "pip install -r requirements.txt\n\n"
            f"或单独安装:\npip install {' '.join(missing_packages)}"
        )
        show_error_and_exit("依赖检查失败", error_msg)

def setup_tk_environment():
    """设置Tcl/Tk库路径"""
    python_dir = sys.base_prefix
    tcl_path = os.path.join(python_dir, 'tcl', 'tcl8.6')
    tk_path = os.path.join(python_dir, 'tcl', 'tk8.6')
    
    if os.path.exists(tcl_path):
        os.environ['TCL_LIBRARY'] = tcl_path
    if os.path.exists(tk_path):
        os.environ['TK_LIBRARY'] = tk_path

def main():
    """主函数"""
    setup_tk_environment()
    check_dependencies()
    
    from src.gui.main_window import main as gui_main
    gui_main()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        show_error_and_exit(
            "程序启动失败",
            f"错误信息:\n{str(e)}\n\n详细堆栈:\n{error_detail[:500]}"
        )