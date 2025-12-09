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
    # 匹配BV号格式：BV + 10位字符
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
    # 匹配AV号格式：av + 数字
    av_pattern = r'[Aa][Vv](\d+)'
    match = re.search(av_pattern, url_or_id)
    if match:
        return int(match.group(1))
    return None


def bv_to_avid(bvid: str) -> Optional[int]:
    """
    将BV号转换为AV号（简化版本，实际需要调用API）
    注意：B站的BV到AV转换算法比较复杂，这里提供一个基础框架
    实际使用时可能需要调用B站API获取真实的AV号
    
    Args:
        bvid: BV号字符串
        
    Returns:
        AV号整数，如果转换失败则返回None
    """
    # B站的BV到AV转换算法比较复杂，涉及Base58编码
    # 这里先返回None，实际使用时通过API获取
    # 或者可以使用第三方库如 bilibili-api-python
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
    
    # 如果只有BV号，尝试获取AV号（实际需要API调用）
    if bvid and not avid:
        # 这里暂时不转换，因为需要API支持
        pass
    
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

