"""
主题与样式常量
"""

import customtkinter as ctk


class Theme:
    # 颜色
    PRIMARY = "#FB7299"     # B站粉
    ACCENT = "#23ADE5"      # B站蓝
    BACKGROUND = "#F6F7F9"  # 浅灰白
    SURFACE = "#FFFFFF"     # 卡片背景
    TEXT_PRIMARY = "#18191C"
    TEXT_SECONDARY = "#61666D"
    BORDER = "#E3E5E7"
    FOCUS = PRIMARY

    # 其他强调色
    STAT_PINK = "#FB7299"
    STAT_BLUE = "#23ADE5"
    STAT_GREEN = "#52C41A"
    STAT_ORANGE = "#FF9F43"

    # 圆角
    RADIUS_CARD = 8
    RADIUS_INPUT = 4
    RADIUS_BUTTON = 20

    # 字体
    FONT_TITLE = ("Microsoft YaHei UI", 20, "bold")
    FONT_SECTION = ("Microsoft YaHei UI", 14, "bold")
    FONT_NORMAL = ("Microsoft YaHei UI", 12)
    FONT_MONO = ("Consolas", 11)


def init_theme():
    """
    初始化 customtkinter 全局主题。
    """
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")  # 基础主题，后续组件自定义颜色

