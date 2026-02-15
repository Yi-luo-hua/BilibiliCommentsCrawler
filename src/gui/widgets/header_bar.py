"""
顶部标题栏
"""
import customtkinter as ctk
from src.gui.theme import Theme


class HeaderBar(ctk.CTkFrame):
    def __init__(self, master, on_toggle_theme, *args, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.BACKGROUND,
            corner_radius=0,
            border_width=0,
            *args,
            **kwargs,
        )

        self.on_toggle_theme = on_toggle_theme

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="B站视频评论爬虫工具",
            font=Theme.FONT_TITLE,
            text_color=Theme.PRIMARY,
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.toggle_btn = ctk.CTkButton(
            self,
            text="🌙",
            width=50,
            height=34,
            corner_radius=14,
            fg_color=Theme.SURFACE,
            text_color=Theme.TEXT_PRIMARY,
            hover_color=Theme.BORDER,
            border_width=1,
            border_color=Theme.BORDER,
            font=("Segoe UI Emoji", 16),
            command=self._toggle,
        )
        self.toggle_btn.grid(row=0, column=1, padx=(8, 0))

    def _toggle(self):
        if self.on_toggle_theme:
            self.on_toggle_theme()

    def set_mode_icon(self, mode: str):
        self.toggle_btn.configure(text="🌙" if mode == "light" else "☀️")

    def update_theme(self):
        """主题切换时更新自身颜色"""
        self.configure(fg_color=Theme.get("BACKGROUND"))
        self.toggle_btn.configure(
            fg_color=Theme.get("SURFACE"),
            text_color=Theme.get("TEXT_PRIMARY"),
            hover_color=Theme.get("BORDER"),
            border_color=Theme.get("BORDER"),
        )
