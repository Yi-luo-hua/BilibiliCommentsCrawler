"""
彩色统计卡片 — 带浅色背景底色
"""
import customtkinter as ctk
from src.gui.theme import Theme


def _lighten(hex_color: str, factor: float = 0.7) -> str:
    """将颜色向白色混合，factor=0 原色，factor=1 纯白"""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


class StatCard(ctk.CTkFrame):
    def __init__(self, master, icon: str, label: str, value: str, color: str, bg_tint: str = None, *args, **kwargs):
        border = _lighten(color, 0.65)
        super().__init__(
            master,
            fg_color=bg_tint or Theme.SURFACE,
            corner_radius=Theme.RADIUS_CARD,
            border_width=1,
            border_color=border,
            *args,
            **kwargs,
        )
        self._bg_tint = bg_tint
        self._color = color

        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI Emoji", 22),
            text_color=color,
            width=44,
        )
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=12, pady=12, sticky="n")

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Microsoft YaHei UI", 22, "bold"),
            text_color=color,
        )
        self.value_label.grid(row=0, column=1, sticky="w", padx=(0, 14), pady=(12, 0))

        self.text_label = ctk.CTkLabel(
            self,
            text=label,
            font=("Microsoft YaHei UI", 12),
            text_color=Theme.TEXT_SECONDARY,
        )
        self.text_label.grid(row=1, column=1, sticky="w", padx=(0, 14), pady=(0, 12))

        self.grid_columnconfigure(1, weight=1)

    def update_value(self, value: str):
        self.value_label.configure(text=value)

    def update_theme(self, bg_tint: str = None):
        """主题切换时更新背景"""
        if bg_tint:
            self._bg_tint = bg_tint
            self.configure(fg_color=bg_tint)
        self.text_label.configure(text_color=Theme.get("TEXT_SECONDARY"))
