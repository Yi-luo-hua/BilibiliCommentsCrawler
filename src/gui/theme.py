"""
主题与样式常量 — 支持 Light / Dark 双模式
"""

import customtkinter as ctk


class Theme:
    """
    主题系统。
    所有颜色属性提供 Light 模式默认值。
    Dark 模式的差异色通过 DARK_OVERRIDES 覆盖。
    """

    # -------- 基础色板 (Light) --------
    PRIMARY = "#FB7299"       # B站粉
    ACCENT = "#23ADE5"        # B站蓝
    BACKGROUND = "#F6F7F9"    # 浅灰白
    SURFACE = "#FFFFFF"       # 卡片背景
    TEXT_PRIMARY = "#18191C"
    TEXT_SECONDARY = "#61666D"
    BORDER = "#E3E5E7"

    # 统计卡片强调色
    STAT_PINK = "#FB7299"
    STAT_BLUE = "#23ADE5"
    STAT_GREEN = "#52C41A"
    STAT_ORANGE = "#FF9F43"

    # 统计卡片浅色底
    STAT_BG_PINK = "#FFF0F3"
    STAT_BG_BLUE = "#EFF8FF"
    STAT_BG_GREEN = "#F0FFF0"
    STAT_BG_ORANGE = "#FFF8EF"

    # 按钮
    DANGER = "#e74c3c"
    DANGER_HOVER = "#c0392b"
    DISABLED_BG = "#F0F0F0"
    DISABLED_FG = "#BBBBBB"

    # -------- Dark 色板覆盖 --------
    DARK_OVERRIDES = {
        "BACKGROUND": "#1B1B1F",
        "SURFACE": "#2B2B30",
        "TEXT_PRIMARY": "#E8E8E8",
        "TEXT_SECONDARY": "#9E9E9E",
        "BORDER": "#3E3E44",
        "STAT_BG_PINK": "#3A2028",
        "STAT_BG_BLUE": "#1E2A38",
        "STAT_BG_GREEN": "#1E3020",
        "STAT_BG_ORANGE": "#382E1E",
        "DISABLED_BG": "#3A3A3E",
        "DISABLED_FG": "#666666",
    }

    # -------- 圆角 --------
    RADIUS_CARD = 10
    RADIUS_INPUT = 6
    RADIUS_BUTTON = 20

    # -------- 字体 --------
    FONT_TITLE = ("Microsoft YaHei UI", 20, "bold")
    FONT_SECTION = ("Microsoft YaHei UI", 14, "bold")
    FONT_NORMAL = ("Microsoft YaHei UI", 12)
    FONT_MONO = ("Consolas", 11)

    # -------- 当前模式 --------
    _mode = "light"

    @classmethod
    def set_mode(cls, mode: str):
        cls._mode = mode

    @classmethod
    def get(cls, key: str) -> str:
        """根据当前模式返回颜色值"""
        if cls._mode == "dark" and key in cls.DARK_OVERRIDES:
            return cls.DARK_OVERRIDES[key]
        return getattr(cls, key, "#FFFFFF")


def init_theme():
    """初始化 customtkinter 全局主题。"""
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
