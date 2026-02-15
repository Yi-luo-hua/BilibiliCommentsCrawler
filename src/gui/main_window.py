"""
使用 customtkinter 的现代化 B站风格 GUI
"""
import logging
import threading
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from typing import Optional

import customtkinter as ctk

from src.crawler.comment_crawler import CommentCrawler
from src.exporter.csv_exporter import CSVExporter
from src.processor.data_processor import DataProcessor
from src.gui.theme import Theme, init_theme
from src.gui.widgets.header_bar import HeaderBar
from src.gui.widgets.card_frame import CardFrame
from src.gui.widgets.stat_card import StatCard
from src.gui.widgets.log_console import LogConsole

logger = logging.getLogger(__name__)


class MainWindow:
    """主窗口类（customtkinter版）"""

    def __init__(self, root: ctk.CTk):
        self.root = root
        init_theme()
        self.appearance = "light"

        self.root.title("B站视频评论爬虫工具")
        self.root.geometry("960x820")
        self.root.minsize(880, 720)
        self.root.configure(fg_color=Theme.BACKGROUND)

        # 逻辑
        self.crawler: Optional[CommentCrawler] = None
        self.crawler_thread: Optional[threading.Thread] = None
        self.is_crawling = False
        self.comments = []
        self.stat_cards = {}
        self._all_cards = []  # 收集所有 CardFrame 用于主题切换

        self._build_layout()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    # ============================================================
    #  UI 构建
    # ============================================================
    def _build_layout(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)

        # 顶部栏
        self.header = HeaderBar(self.root, on_toggle_theme=self._toggle_theme)
        self.header.grid(row=0, column=0, sticky="we", padx=20, pady=(16, 6))

        self._build_video_card()
        self._build_params_card()
        self._build_actions()
        self._build_stat_cards()
        self._build_log_console()

    def _build_video_card(self):
        card = CardFrame(self.root)
        card.grid(row=1, column=0, sticky="we", padx=20, pady=6)
        card.grid_columnconfigure(1, weight=1)
        self._all_cards.append(card)

        title = ctk.CTkLabel(card, text="视频信息", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY)
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 4))
        self._video_title_label = title

        label = ctk.CTkLabel(card, text="视频链接 / BV号", text_color=Theme.TEXT_SECONDARY, font=Theme.FONT_NORMAL)
        label.grid(row=1, column=0, sticky="w", padx=14, pady=(6, 12))
        self._video_label = label

        self.video_entry = ctk.CTkEntry(
            card,
            placeholder_text="例如 https://www.bilibili.com/video/BVxxxx 或 BVxxxx",
            corner_radius=Theme.RADIUS_INPUT,
            border_width=1,
            fg_color=Theme.SURFACE,
            border_color=Theme.BORDER,
            font=Theme.FONT_NORMAL,
            text_color=Theme.TEXT_PRIMARY,
        )
        self.video_entry.grid(row=1, column=1, sticky="we", padx=14, pady=(6, 12))

    def _build_params_card(self):
        card = CardFrame(self.root)
        card.grid(row=2, column=0, sticky="we", padx=20, pady=6)
        for i in range(3):
            card.grid_columnconfigure(i, weight=1)
        self._all_cards.append(card)

        title = ctk.CTkLabel(card, text="爬取参数", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY)
        title.grid(row=0, column=0, columnspan=3, sticky="w", padx=14, pady=(12, 6))
        self._params_title_label = title

        # 开关
        self.include_replies_var = ctk.BooleanVar(value=True)
        self.include_switch = ctk.CTkSwitch(
            card,
            text="包含子评论/回复",
            variable=self.include_replies_var,
            onvalue=True,
            offvalue=False,
            fg_color=Theme.BORDER,
            progress_color=Theme.PRIMARY,
            button_color=Theme.SURFACE,
            button_hover_color=Theme.BORDER,
            text_color=Theme.TEXT_PRIMARY,
            font=Theme.FONT_NORMAL,
        )
        self.include_switch.grid(row=1, column=0, sticky="w", padx=14, pady=(4, 10))

        # 最大爬取页数
        self._pages_label = ctk.CTkLabel(
            card, text="最大爬取页数", text_color=Theme.TEXT_SECONDARY, font=Theme.FONT_NORMAL
        )
        self._pages_label.grid(row=1, column=1, sticky="w", padx=14, pady=(4, 2))
        self.max_pages_var = ctk.StringVar(value="100")
        self.max_pages_entry = ctk.CTkEntry(
            card,
            textvariable=self.max_pages_var,
            width=120,
            corner_radius=Theme.RADIUS_INPUT,
            border_width=1,
            fg_color=Theme.SURFACE,
            border_color=Theme.BORDER,
            font=Theme.FONT_NORMAL,
            text_color=Theme.TEXT_PRIMARY,
        )
        self.max_pages_entry.grid(row=2, column=1, sticky="w", padx=14, pady=(0, 10))

        # 排序模式
        self._sort_label = ctk.CTkLabel(
            card, text="排序模式", text_color=Theme.TEXT_SECONDARY, font=Theme.FONT_NORMAL
        )
        self._sort_label.grid(row=1, column=2, sticky="w", padx=14, pady=(4, 2))
        self.sort_mode_var = ctk.StringVar(value="3")
        self.sort_segment = ctk.CTkSegmentedButton(
            card,
            values=["按时间", "按热度"],
            font=("Microsoft YaHei UI", 13),
            width=200,
            fg_color=Theme.BORDER,
            selected_color=Theme.PRIMARY,
            selected_hover_color=Theme.PRIMARY,
            unselected_color=Theme.SURFACE,
            unselected_hover_color=Theme.PRIMARY,
            corner_radius=Theme.RADIUS_INPUT,
            command=self._on_sort_change,
        )
        self.sort_segment.set("按时间")
        self.sort_segment.grid(row=2, column=2, sticky="w", padx=14, pady=(0, 10))

    def _build_actions(self):
        frame = CardFrame(self.root)
        frame.grid(row=3, column=0, sticky="we", padx=20, pady=(4, 6))
        frame.grid_columnconfigure(0, weight=1)
        self._all_cards.append(frame)

        self._path_label = ctk.CTkLabel(
            frame, text="导出路径", text_color=Theme.TEXT_SECONDARY, font=Theme.FONT_NORMAL
        )
        self._path_label.grid(row=0, column=0, sticky="w", padx=14, pady=(10, 4))

        path_frame = ctk.CTkFrame(frame, fg_color="transparent")
        path_frame.grid(row=1, column=0, sticky="we", padx=14, pady=(0, 10))
        path_frame.grid_columnconfigure(0, weight=1)

        self.export_path_var = ctk.StringVar(value="bilibili_comments.csv")
        self.path_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.export_path_var,
            corner_radius=Theme.RADIUS_INPUT,
            border_width=1,
            fg_color=Theme.SURFACE,
            border_color=Theme.BORDER,
            font=Theme.FONT_NORMAL,
            text_color=Theme.TEXT_PRIMARY,
        )
        self.path_entry.grid(row=0, column=0, sticky="we", padx=(0, 8))

        self.browse_btn = ctk.CTkButton(
            path_frame,
            text="浏览...",
            width=90,
            height=34,
            corner_radius=Theme.RADIUS_BUTTON,
            fg_color=Theme.ACCENT,
            hover_color="#1f9bcb",
            text_color="white",
            command=self._browse_file,
        )
        self.browse_btn.grid(row=0, column=1, sticky="w")

        btn_wrap = ctk.CTkFrame(frame, fg_color="transparent")
        btn_wrap.grid(row=2, column=0, columnspan=2, sticky="e", padx=8, pady=(4, 10))

        self.start_button = ctk.CTkButton(
            btn_wrap,
            text="▶ 开始爬取",
            height=38,
            width=130,
            corner_radius=Theme.RADIUS_BUTTON,
            fg_color=Theme.PRIMARY,
            hover_color="#f25f88",
            text_color="white",
            border_width=0,
            font=("Microsoft YaHei UI", 13, "bold"),
            command=self._start_crawling,
        )
        self.start_button.pack(side="left", padx=6)

        self.stop_button = ctk.CTkButton(
            btn_wrap,
            text="⏹ 停止",
            height=38,
            width=100,
            corner_radius=Theme.RADIUS_BUTTON,
            fg_color=Theme.DISABLED_BG,
            hover_color=Theme.DISABLED_BG,
            text_color=Theme.DISABLED_FG,
            border_width=0,
            font=("Microsoft YaHei UI", 13),
            state="disabled",
            command=self._stop_crawling,
        )
        self.stop_button.pack(side="left", padx=6)

        self.export_button = ctk.CTkButton(
            btn_wrap,
            text="💾 导出 CSV",
            height=38,
            width=130,
            corner_radius=Theme.RADIUS_BUTTON,
            fg_color=Theme.DISABLED_BG,
            hover_color=Theme.DISABLED_BG,
            text_color=Theme.DISABLED_FG,
            border_width=0,
            font=("Microsoft YaHei UI", 13),
            state="disabled",
            command=self._export_csv,
        )
        self.export_button.pack(side="left", padx=6)

    def _build_stat_cards(self):
        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.grid(row=4, column=0, sticky="we", padx=20, pady=4)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
        self._stat_frame = frame

        self.stat_cards["total"] = StatCard(
            frame, "📊", "总评论数", "0", Theme.STAT_PINK, bg_tint=Theme.STAT_BG_PINK
        )
        self.stat_cards["main"] = StatCard(
            frame, "💬", "主评论", "0", Theme.STAT_BLUE, bg_tint=Theme.STAT_BG_BLUE
        )
        self.stat_cards["replies"] = StatCard(
            frame, "↩️", "回复", "0", Theme.STAT_GREEN, bg_tint=Theme.STAT_BG_GREEN
        )
        self.stat_cards["likes"] = StatCard(
            frame, "👍", "总点赞", "0", Theme.STAT_ORANGE, bg_tint=Theme.STAT_BG_ORANGE
        )

        for idx, key in enumerate(["total", "main", "replies", "likes"]):
            self.stat_cards[key].grid(row=0, column=idx, padx=6, pady=4, sticky="we")

    def _build_log_console(self):
        self.log_card = CardFrame(self.root)
        self.log_card.grid(row=5, column=0, sticky="nsew", padx=20, pady=(4, 16))
        self.root.grid_rowconfigure(5, weight=1)
        self.log_card.grid_columnconfigure(0, weight=1)
        self.log_card.grid_rowconfigure(1, weight=1)
        self._all_cards.append(self.log_card)

        self._log_title = ctk.CTkLabel(
            self.log_card, text="日志输出", font=Theme.FONT_SECTION, text_color=Theme.TEXT_PRIMARY
        )
        self._log_title.grid(row=0, column=0, sticky="w", padx=14, pady=(12, 4))

        self.log_console = LogConsole(self.log_card, dark_mode=False)
        self.log_console.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 10))

        # 进度条 — 初始静止
        self.progress_bar = ctk.CTkProgressBar(
            self.log_card,
            height=8,
            fg_color=Theme.BORDER,
            progress_color=Theme.PRIMARY,
            corner_radius=Theme.RADIUS_INPUT,
            mode="determinate",
        )
        self.progress_bar.grid(row=2, column=0, sticky="we", padx=14, pady=(0, 10))
        self.progress_bar.set(0)  # 空闲时静止

        self.progress_var = ctk.StringVar(value="就绪")
        self.progress_label = ctk.CTkLabel(
            self.log_card,
            textvariable=self.progress_var,
            text_color=Theme.TEXT_SECONDARY,
            font=Theme.FONT_NORMAL,
        )
        self.progress_label.grid(row=3, column=0, sticky="w", padx=14, pady=(0, 12))

    # ============================================================
    #  事件处理
    # ============================================================
    def _on_sort_change(self, value):
        self.sort_mode_var.set("3" if value == "按时间" else "2")

    def _toggle_theme(self):
        self.appearance = "dark" if self.appearance == "light" else "light"
        is_dark = self.appearance == "dark"
        Theme.set_mode(self.appearance)
        ctk.set_appearance_mode(self.appearance)

        # 更新组件
        self.root.configure(fg_color=Theme.get("BACKGROUND"))
        self.header.set_mode_icon(self.appearance)
        self.header.update_theme()

        for card in self._all_cards:
            card.update_theme()

        # 统计卡片
        tint_map = {
            "total": "STAT_BG_PINK",
            "main": "STAT_BG_BLUE",
            "replies": "STAT_BG_GREEN",
            "likes": "STAT_BG_ORANGE",
        }
        for key, tint_key in tint_map.items():
            self.stat_cards[key].update_theme(bg_tint=Theme.get(tint_key))

        # 日志
        self.log_console.update_theme(is_dark)

        # 各种 label
        text_primary = Theme.get("TEXT_PRIMARY")
        text_secondary = Theme.get("TEXT_SECONDARY")
        surface = Theme.get("SURFACE")
        border = Theme.get("BORDER")

        for lbl in [self._video_title_label, self._params_title_label, self._log_title]:
            lbl.configure(text_color=text_primary)
        for lbl in [self._video_label, self._pages_label, self._sort_label, self._path_label]:
            lbl.configure(text_color=text_secondary)
        self.progress_label.configure(text_color=text_secondary)

        # 输入框
        for entry in [self.video_entry, self.max_pages_entry, self.path_entry]:
            entry.configure(
                fg_color=surface,
                border_color=border,
                text_color=text_primary,
            )

        # 开关
        self.include_switch.configure(
            fg_color=border,
            button_color=surface,
            button_hover_color=border,
            text_color=text_primary,
        )

        # 分段按钮
        self.sort_segment.configure(
            fg_color=border,
            unselected_color=surface,
        )

        # 进度条
        self.progress_bar.configure(fg_color=border)

    def _browse_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
        )
        if filename:
            self.export_path_var.set(filename)

    def _log(self, message: str):
        self.log_console.write(message)

    def _thread_safe_log(self, message: str):
        """线程安全的日志回调"""
        self.root.after(0, lambda m=message: self._update_progress(m))

    def _update_progress(self, message: str):
        self.progress_var.set(message)
        self._log(message)

    def _start_crawling(self):
        video_input = self.video_entry.get().strip()
        if not video_input:
            messagebox.showwarning("警告", "请输入视频链接或BV号")
            return

        self.is_crawling = True
        self.start_button.configure(state="disabled", fg_color="#ccc")
        self.stop_button.configure(
            state="normal",
            fg_color=Theme.DANGER,
            hover_color=Theme.DANGER_HOVER,
            text_color="white",
        )
        self.export_button.configure(
            state="disabled",
            fg_color=Theme.get("DISABLED_BG"),
            text_color=Theme.get("DISABLED_FG"),
        )

        # 进度条启动动画
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        self.log_console.clear()
        self.comments = []

        for card in self.stat_cards.values():
            card.update_value("0")

        include_replies = self.include_replies_var.get()
        try:
            max_pages = int(self.max_pages_var.get())
            max_pages = max(1, min(1000, max_pages))
        except ValueError:
            max_pages = 100
        mode = int(self.sort_mode_var.get())

        self.crawler = CommentCrawler(progress_callback=self._thread_safe_log)

        def crawl_thread():
            try:
                comments = self.crawler.crawl_comments(
                    video_input,
                    include_replies=include_replies,
                    max_pages=max_pages,
                    mode=mode,
                )
                processor = DataProcessor()
                cleaned = processor.clean_comments(comments)
                self.comments = cleaned
                stats = processor.get_statistics(self.comments)
                self.root.after(0, lambda: self._crawl_finished(stats))
            except Exception as e:
                logger.error(f"爬取过程异常: {e}", exc_info=True)
                self.root.after(0, lambda: self._crawl_error(str(e)))

        self.crawler_thread = threading.Thread(target=crawl_thread, daemon=True)
        self.crawler_thread.start()

    def _crawl_finished(self, stats: dict):
        self.is_crawling = False
        self.start_button.configure(state="normal", fg_color=Theme.PRIMARY)
        self.stop_button.configure(
            state="disabled",
            fg_color=Theme.get("DISABLED_BG"),
            hover_color=Theme.get("DISABLED_BG"),
            text_color=Theme.get("DISABLED_FG"),
        )
        self.export_button.configure(
            state="normal",
            fg_color=Theme.ACCENT,
            hover_color="#1f9bcb",
            text_color="white",
        )

        # 进度条停止并显示完成
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1.0)
        self.progress_var.set("✅ 爬取完成")

        self.stat_cards["total"].update_value(str(stats["total"]))
        self.stat_cards["main"].update_value(str(stats["main_comments"]))
        self.stat_cards["replies"].update_value(str(stats["replies"]))
        self.stat_cards["likes"].update_value(str(stats["total_likes"]))

        if self.comments:
            messagebox.showinfo("完成", f"成功爬取 {len(self.comments)} 条评论！")
        else:
            messagebox.showwarning("警告", "未获取到任何评论数据")

    def _crawl_error(self, error_msg: str):
        self.is_crawling = False
        self.start_button.configure(state="normal", fg_color=Theme.PRIMARY)
        self.stop_button.configure(
            state="disabled",
            fg_color=Theme.get("DISABLED_BG"),
            hover_color=Theme.get("DISABLED_BG"),
            text_color=Theme.get("DISABLED_FG"),
        )

        # 进度条停止并重置
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.progress_var.set("❌ 爬取失败")

        self._log(f"错误: {error_msg}")
        messagebox.showerror("错误", f"爬取过程中出现错误:\n{error_msg}")

    def _stop_crawling(self):
        if self.crawler:
            self.crawler.stop()
        self._update_progress("正在停止...")

    def _export_csv(self):
        if not self.comments:
            messagebox.showwarning("警告", "没有可导出的数据")
            return

        path_val = self.export_path_var.get().strip()
        if not path_val:
            messagebox.showwarning("警告", "请指定导出文件路径")
            return

        try:
            success = CSVExporter.export(self.comments, path_val)
            if success:
                messagebox.showinfo("成功", f"数据已导出到:\n{path_val}")
            else:
                messagebox.showerror("失败", "导出失败，请查看日志")
        except Exception as e:
            messagebox.showerror("错误", f"导出时出错:\n{str(e)}")

    def _on_closing(self):
        if self.is_crawling:
            if messagebox.askokcancel("退出", "正在爬取中，确定要退出吗？"):
                if self.crawler:
                    self.crawler.stop()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    root = ctk.CTk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
