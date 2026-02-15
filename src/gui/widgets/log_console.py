"""
日志输出控件
"""
import customtkinter as ctk
from src.gui.theme import Theme


class LogConsole(ctk.CTkFrame):
    def __init__(self, master, dark_mode: bool = False, *args, **kwargs):
        super().__init__(
            master,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS_CARD,
            border_width=0,
            *args,
            **kwargs,
        )
        fg = "#2B2B2B" if dark_mode else "#F1F2F3"
        text_color = "#DADADA" if dark_mode else Theme.TEXT_PRIMARY

        self.text = ctk.CTkTextbox(
            self,
            fg_color=fg,
            text_color=text_color,
            font=Theme.FONT_MONO,
            corner_radius=Theme.RADIUS_CARD,
            border_width=0,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=8)

    def write(self, message: str):
        self.text.insert("end", message + "\n")
        self.text.see("end")

    def clear(self):
        self.text.delete("1.0", "end")

    def set_dark(self, dark: bool):
        fg = "#1E1E22" if dark else "#F1F2F3"
        text_color = "#DADADA" if dark else Theme.TEXT_PRIMARY
        self.text.configure(fg_color=fg, text_color=text_color)

    def update_theme(self, dark: bool):
        """主题切换时更新"""
        self.configure(fg_color=Theme.get("SURFACE"))
        self.set_dark(dark)
