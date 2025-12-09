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

