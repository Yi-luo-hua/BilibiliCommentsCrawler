"""
CSV导出功能模块
"""
import logging
import pandas as pd
from typing import List, Dict, Optional
from config.config import CSV_ENCODING

logger = logging.getLogger(__name__)


class CSVExporter:
    """CSV导出器类"""

    # 列名映射：英文 → 中文
    COLUMN_MAPPING = {
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

    # 默认导出的列
    DEFAULT_COLUMNS = [
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

    @classmethod
    def export(
        cls,
        comments: List[Dict],
        filepath: str,
        columns: Optional[List[str]] = None,
        index: bool = False,
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
            logger.warning("没有数据可导出")
            return False

        try:
            df = pd.DataFrame(comments)

            if columns:
                available_columns = [col for col in columns if col in df.columns]
                if not available_columns:
                    logger.warning("指定的列都不存在，将导出所有列")
                    available_columns = df.columns.tolist()
                df = df[available_columns]

            df = df.rename(columns=cls.COLUMN_MAPPING)
            df.to_csv(filepath, index=index, encoding=CSV_ENCODING)
            logger.info(f"成功导出 {len(comments)} 条评论到: {filepath}")
            return True

        except Exception as e:
            logger.error(f"导出CSV时出错: {e}")
            return False
