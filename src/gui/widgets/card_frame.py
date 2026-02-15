"""
卡片容器，带圆角与内边距
"""
import customtkinter as ctk
from src.gui.theme import Theme


class CardFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS_CARD,
            border_width=0,
            *args,
            **kwargs,
        )

    def update_theme(self):
        """主题切换时更新背景"""
        self.configure(fg_color=Theme.get("SURFACE"))
