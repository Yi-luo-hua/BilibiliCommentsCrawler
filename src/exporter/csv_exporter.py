"""
CSV导出功能模块
"""
import pandas as pd
from typing import List, Dict, Optional
from config.config import CSV_ENCODING


class CSVExporter:
    """CSV导出器类"""
    
    @staticmethod
    def export(
        comments: List[Dict],
        filepath: str,
        columns: Optional[List[str]] = None,
        index: bool = False
    ) -> bool:
        """
        导出评论数据到CSV文件
        
        Args:
            comments: 评论列表
            filepath: 输出文件路径
            columns: 要导出的列名列表，如果为None则导出所有列
            index: 是否包含索引列
            
        Returns:
            如果导出成功返回True，否则返回False
        """
        if not comments:
            print("警告: 没有数据可导出")
            return False
        
        try:
            # 转换为DataFrame
            df = pd.DataFrame(comments)
            
            # 选择要导出的列
            if columns:
                # 确保所有指定的列都存在
                available_columns = [col for col in columns if col in df.columns]
                if not available_columns:
                    print(f"警告: 指定的列都不存在，将导出所有列")
                    available_columns = df.columns.tolist()
                df = df[available_columns]
            
            # 重命名列名为中文（可选）
            column_mapping = {
                'comment_id': '评论ID',
                'root_id': '根评论ID',
                'parent_id': '父评论ID',
                'is_reply': '是否为回复',
                'video_oid': '视频OID',
                'user_id': '用户ID',
                'username': '用户名',
                'user_level': '用户等级',
                'content': '评论内容',
                'like_count': '点赞数',
                'reply_count': '回复数',
                'ctime': '时间戳',
                'ctime_text': '时间',
                'ip_location': 'IP归属地',
            }
            
            # 重命名列
            df = df.rename(columns=column_mapping)
            
            # 导出到CSV
            df.to_csv(filepath, index=index, encoding=CSV_ENCODING)
            print(f"成功导出 {len(comments)} 条评论到: {filepath}")
            return True
            
        except Exception as e:
            print(f"导出CSV时出错: {e}")
            return False
    
    @staticmethod
    def get_default_columns() -> List[str]:
        """
        获取默认导出的列名
        
        Returns:
            默认列名列表
        """
        return [
            'comment_id',
            'root_id',
            'is_reply',
            'username',
            'user_level',
            'content',
            'like_count',
            'reply_count',
            'ctime_text',
            'ip_location',
        ]

