"""
B站API调用封装模块
"""
import time
import requests
from typing import Dict, Optional, Any
from config.config import (
    COMMENT_API_URL,
    REPLY_API_URL,
    DEFAULT_HEADERS,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    MAX_RETRIES,
)


class BilibiliAPI:
    """B站API调用封装类"""
    
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        初始化API客户端
        
        Args:
            headers: 自定义请求头，如果为None则使用默认请求头
        """
        self.headers = headers or DEFAULT_HEADERS.copy()
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _request(self, url: str, params: Dict[str, Any], retry_count: int = 0) -> Optional[Dict]:
        """
        发送HTTP请求（带重试机制）
        
        Args:
            url: 请求URL
            params: 请求参数
            retry_count: 当前重试次数
            
        Returns:
            JSON响应数据，如果请求失败则返回None
        """
        try:
            time.sleep(REQUEST_DELAY)  # 控制请求频率
            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            # 检查API返回的code
            if data.get('code') != 0:
                print(f"API返回错误: code={data.get('code')}, message={data.get('message')}")
                return None
            
            return data
            
        except requests.exceptions.Timeout:
            if retry_count < MAX_RETRIES:
                print(f"请求超时，正在重试 ({retry_count + 1}/{MAX_RETRIES})")
                time.sleep(2 ** retry_count)  # 指数退避
                return self._request(url, params, retry_count + 1)
            else:
                print(f"请求超时，已达到最大重试次数")
                return None
        except requests.exceptions.RequestException as e:
            if retry_count < MAX_RETRIES:
                print(f"请求失败，正在重试 ({retry_count + 1}/{MAX_RETRIES}): {e}")
                time.sleep(2 ** retry_count)  # 指数退避
                return self._request(url, params, retry_count + 1)
            else:
                print(f"请求失败，已达到最大重试次数: {e}")
                return None
        except ValueError as e:
            # JSON解析错误
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"处理响应时出错: {e}")
            return None
    
    def get_video_info(self, bvid: str) -> Optional[Dict]:
        """
        获取视频基本信息（用于获取真实的AV号）
        
        Args:
            bvid: BV号
            
        Returns:
            视频信息字典
        """
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {"bvid": bvid}
        return self._request(url, params)
    
    def get_comments(self, oid: int, page: int = 1, mode: int = 3, type_id: int = 1, next_page: int = 0) -> Optional[Dict]:
        """
        获取视频评论列表
        
        Args:
            oid: 视频AV号（oid）
            page: 页码，从1开始（兼容旧版API）
            mode: 排序模式，3=按时间排序，2=按热度排序
            type_id: 类型ID，1=视频
            next_page: 下一页标识（cursor.next值），用于新版API分页
            
        Returns:
            评论数据字典
        """
        params = {
            "oid": oid,
            "type": type_id,
            "mode": mode,
            "pn": page,
            "ps": 20,  # 每页数量
            "next": next_page,  # 使用next参数进行分页
        }
        return self._request(COMMENT_API_URL, params)
    
    def get_replies(self, oid: int, root: int, page: int = 1, type_id: int = 1) -> Optional[Dict]:
        """
        获取评论的回复（子评论）
        
        Args:
            oid: 视频AV号
            root: 根评论ID
            page: 页码
            type_id: 类型ID，1=视频
            
        Returns:
            回复数据字典
        """
        params = {
            "oid": oid,
            "type": type_id,
            "root": root,
            "pn": page,
            "ps": 20,
        }
        return self._request(REPLY_API_URL, params)
    
    def set_cookie(self, cookie: str):
        """
        设置Cookie（用于需要登录的场景）
        
        Args:
            cookie: Cookie字符串
        """
        self.session.headers.update({"Cookie": cookie})

