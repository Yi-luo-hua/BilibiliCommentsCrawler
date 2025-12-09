"""
B站评论爬虫工具 - 主程序入口
"""
import sys
import os

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
        print("\n" + "="*60)
        print("❌ 缺少必要的依赖包!")
        print("="*60)
        print("\n缺少的包:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\n请运行以下命令安装所有依赖:")
        print("\n  pip install -r requirements.txt")
        print("\n或者单独安装缺少的包:")
        print(f"\n  pip install {' '.join(missing_packages)}")
        print("\n" + "="*60)
        input("\n按回车键退出...")
        sys.exit(1)

# 设置Tcl/Tk库路径（修复tkinter问题）
python_dir = sys.base_prefix
# python_dir = os.path.dirname(sys.executable)
tcl_path = os.path.join(python_dir, 'tcl', 'tcl8.6')
tk_path = os.path.join(python_dir, 'tcl', 'tk8.6')

if os.path.exists(tcl_path):
    os.environ['TCL_LIBRARY'] = tcl_path
if os.path.exists(tk_path):
    os.environ['TK_LIBRARY'] = tk_path

# 检查依赖
check_dependencies()

try:
    from src.gui.main_window import main
    
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"\n启动失败: {e}")
    import traceback
    traceback.print_exc()
    input("\n按回车键退出...")
