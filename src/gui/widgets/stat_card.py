"""
彩色统计卡片
"""
import customtkinter as ctk
from src.gui.theme import Theme


class StatCard(ctk.CTkFrame):
    def __init__(self, master, icon: str, label: str, value: str, color: str, *args, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS_CARD,
            border_width=0,
            *args,
            **kwargs,
        )

        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI Emoji", 18),
            text_color=color,
            width=40,
        )
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=12, pady=10, sticky="n")

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Microsoft YaHei UI", 18, "bold"),
            text_color=color,
        )
        self.value_label.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=(10, 0))

        self.text_label = ctk.CTkLabel(
            self,
            text=label,
            font=("Microsoft YaHei UI", 12),
            text_color=Theme.TEXT_SECONDARY,
        )
        self.text_label.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=(0, 10))

        self.grid_columnconfigure(1, weight=1)

    def update_value(self, value: str):
        self.value_label.configure(text=value)

