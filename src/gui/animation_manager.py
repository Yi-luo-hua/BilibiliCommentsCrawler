"""
动画管理器
"""
import tkinter as tk
from typing import Callable, Optional


class AnimationManager:
    """动画管理器类，负责各种动画效果"""
    
    @staticmethod
    def animate_color(
        widget,
        start_color: str,
        end_color: str,
        duration: int = 200,
        callback: Optional[Callable] = None
    ):
        """
        颜色渐变动画
        
        Args:
            widget: 目标组件
            start_color: 起始颜色（十六进制）
            end_color: 结束颜色（十六进制）
            duration: 动画时长（毫秒）
            callback: 动画完成后的回调函数
        """
        def hex_to_rgb(hex_color: str) -> tuple:
            """将十六进制颜色转换为RGB"""
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb: tuple) -> str:
            """将RGB转换为十六进制颜色"""
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        steps = max(1, duration // 16)  # 约60fps
        current_step = [0]
        
        def animate():
            if current_step[0] <= steps:
                t = current_step[0] / steps
                # 使用缓动函数（ease-in-out）
                t = t * t * (3 - 2 * t)
                
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
                
                color = rgb_to_hex((r, g, b))
                
                try:
                    widget.configure(bg=color)
                except:
                    pass
                
                current_step[0] += 1
                widget.after(16, animate)
            else:
                if callback:
                    callback()
        
        animate()
    
    @staticmethod
    def fade_in(widget, duration: int = 300):
        """
        淡入动画
        
        Args:
            widget: 目标组件
            duration: 动画时长（毫秒）
        """
        # tkinter不支持透明度，这里可以实现其他效果
        # 例如：改变背景色从透明色到目标色
        pass
    
    @staticmethod
    def smooth_scroll(text_widget, target_line: int, duration: int = 300):
        """
        平滑滚动到指定行
        
        Args:
            text_widget: 文本组件
            target_line: 目标行号
            duration: 动画时长（毫秒）
        """
        current_line = float(text_widget.index("end-1c").split('.')[0])
        if current_line == target_line:
            return
        
        steps = max(1, duration // 16)
        step_size = (target_line - current_line) / steps
        current_step = [0]
        
        def scroll():
            if current_step[0] < steps:
                line = current_line + step_size * current_step[0]
                text_widget.see(f"{int(line)}.0")
                current_step[0] += 1
                text_widget.after(16, scroll)
            else:
                text_widget.see(f"{target_line}.0")
        
        scroll()

