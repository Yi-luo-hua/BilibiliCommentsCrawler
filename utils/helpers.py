"""
工具函数模块
"""
import re
from typing import Optional, Tuple


def extract_bvid(url_or_id: str) -> Optional[str]:
    """
    从URL或字符串中提取BV号

    Args:
        url_or_id: 视频URL或BV号字符串

    Returns:
        BV号字符串，如果无法提取则返回None
    """
    bv_pattern = r'[Bb][Vv]([A-Za-z0-9]{10})'
    match = re.search(bv_pattern, url_or_id)
    if match:
        return f"BV{match.group(1)}"
    return None


def extract_avid(url_or_id: str) -> Optional[int]:
    """
    从URL或字符串中提取AV号

    Args:
        url_or_id: 视频URL或AV号字符串

    Returns:
        AV号整数，如果无法提取则返回None
    """
    av_pattern = r'[Aa][Vv](\d+)'
    match = re.search(av_pattern, url_or_id)
    if match:
        return int(match.group(1))
    return None


def parse_video_id(url_or_id: str) -> Tuple[Optional[str], Optional[int]]:
    """
    解析视频ID，返回BV号和AV号

    Args:
        url_or_id: 视频URL、BV号或AV号

    Returns:
        (BV号, AV号) 元组
    """
    bvid = extract_bvid(url_or_id)
    avid = extract_avid(url_or_id)
    return bvid, avid


def validate_bvid(bvid: str) -> bool:
    """
    验证BV号格式是否正确

    Args:
        bvid: BV号字符串

    Returns:
        如果格式正确返回True，否则返回False
    """
    if not bvid:
        return False
    pattern = r'^[Bb][Vv][A-Za-z0-9]{10}$'
    return bool(re.match(pattern, bvid))
