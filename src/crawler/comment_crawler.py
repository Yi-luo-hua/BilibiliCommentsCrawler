"""
评论爬取核心逻辑模块
"""
from typing import List, Dict, Optional, Callable
from src.api.bilibili_api import BilibiliAPI
from utils.helpers import parse_video_id, validate_bvid


class CommentCrawler:
    """评论爬虫类"""
    
    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        """
        初始化爬虫
        
        Args:
            progress_callback: 进度回调函数，接收日志消息
        """
        self.api = BilibiliAPI()
        self.progress_callback = progress_callback or (lambda x: None)
        self._stop_flag = False
    
    def _log(self, message: str):
        """输出日志"""
        self.progress_callback(message)
        print(message)
    
    def stop(self):
        """停止爬取"""
        self._stop_flag = True
        self._log("正在停止爬取...")
    
    def get_video_oid(self, url_or_id: str) -> Optional[int]:
        """
        获取视频的OID（AV号）
        
        Args:
            url_or_id: 视频URL、BV号或AV号
            
        Returns:
            视频OID（AV号），如果获取失败则返回None
        """
        bvid, avid = parse_video_id(url_or_id)
        
        # 如果已经有AV号，直接返回
        if avid:
            return avid
        
        # 如果有BV号，通过API获取AV号
        if bvid and validate_bvid(bvid):
            self._log(f"正在获取视频信息: {bvid}")
            video_info = self.api.get_video_info(bvid)
            if video_info and video_info.get('data'):
                oid = video_info['data'].get('aid')
                if oid:
                    self._log(f"成功获取视频OID: {oid}")
                    return oid
        
        # 尝试从URL中提取AV号
        if not avid:
            self._log("无法获取视频OID，请检查输入的视频ID或URL")
        
        return avid
    
    def crawl_comments(
        self,
        url_or_id: str,
        include_replies: bool = True,
        max_pages: int = 1000,
        mode: int = 3
    ) -> List[Dict]:
        """
        爬取视频评论
        
        Args:
            url_or_id: 视频URL、BV号或AV号
            include_replies: 是否包含子评论（回复）
            max_pages: 最大爬取页数
            mode: 排序模式，3=按时间，2=按热度
            
        Returns:
            评论列表
        """
        self._stop_flag = False
        all_comments = []
        
        # 获取视频OID
        oid = self.get_video_oid(url_or_id)
        if not oid:
            self._log("错误: 无法获取视频OID")
            return all_comments
        
        self._log(f"开始爬取评论，视频OID: {oid}")
        
        page = 1
        next_page = 0  # cursor.next值，用于分页
        total_replies = 0
        seen_comment_ids = set()  # 用于去重，避免重复爬取
        
        while page <= max_pages and not self._stop_flag:
            self._log(f"正在爬取第 {page} 页评论...")
            
            # 获取评论列表
            comment_data = self.api.get_comments(oid, page=page, mode=mode, next_page=next_page)
            
            if not comment_data or not comment_data.get('data'):
                self._log(f"第 {page} 页没有更多评论")
                break
            
            replies = comment_data['data'].get('replies', [])
            if not replies:
                self._log(f"第 {page} 页评论为空")
                break
            
            # 去重检查：如果这页的评论ID都在seen集合中，说明已经爬取过了
            current_page_ids = {reply.get('rpid') for reply in replies if reply.get('rpid')}
            if current_page_ids.issubset(seen_comment_ids):
                self._log("检测到重复数据，已到达最后一页")
                break
            
            seen_comment_ids.update(current_page_ids)
            self._log(f"第 {page} 页获取到 {len(replies)} 条评论")
            
            # 处理每条评论
            for reply in replies:
                if self._stop_flag:
                    break
                
                # 处理主评论
                comment = self._process_comment(reply, oid, is_reply=False)
                all_comments.append(comment)
                
                # 如果包含子评论，获取回复
                if include_replies:
                    rcount = reply.get('rcount', 0)
                    if rcount > 0:
                        self._log(f"  评论 {reply.get('rpid')} 有 {rcount} 条回复，正在获取...")
                        sub_comments = self._crawl_replies(oid, reply.get('rpid'))
                        all_comments.extend(sub_comments)
                        total_replies += len(sub_comments)
            
            # 检查是否还有更多页（使用cursor机制）
            cursor = comment_data['data'].get('cursor', {})
            is_end = cursor.get('is_end', True) if cursor else True
            next_page = cursor.get('next', 0) if cursor else 0
            
            if not is_end and len(replies) > 0 and next_page > 0:
                page += 1
            else:
                self._log("已到达最后一页")
                break
        
        self._log(f"爬取完成！共获取 {len(all_comments)} 条评论（主评论: {len(all_comments) - total_replies}, 回复: {total_replies}）")
        return all_comments
    
    def _crawl_replies(self, oid: int, root: int) -> List[Dict]:
        """
        爬取评论的回复
        
        Args:
            oid: 视频OID
            root: 根评论ID
            
        Returns:
            回复列表
        """
        replies = []
        page = 1
        
        while not self._stop_flag:
            reply_data = self.api.get_replies(oid, root, page=page)
            
            if not reply_data or not reply_data.get('data'):
                break
            
            reply_list = reply_data['data'].get('replies', [])
            if not reply_list:
                break
            
            for reply in reply_list:
                comment = self._process_comment(reply, oid, is_reply=True, root_id=root)
                replies.append(comment)
            
            # 检查是否还有更多页
            cursor = reply_data['data'].get('cursor', {})
            # 兼容新旧API格式
            is_end = cursor.get('is_end', True) if cursor else True
            if is_end:
                break
            
            page += 1
        
        return replies
    
    def _process_comment(self, reply: Dict, oid: int, is_reply: bool = False, root_id: Optional[int] = None) -> Dict:
        """
        处理单条评论数据
        
        Args:
            reply: 原始评论数据
            oid: 视频OID
            is_reply: 是否为回复
            root_id: 根评论ID（如果是回复）
            
        Returns:
            处理后的评论字典
        """
        member = reply.get('member', {})
        content = reply.get('content', {})
        
        comment = {
            'comment_id': reply.get('rpid'),  # 评论ID
            'root_id': root_id or reply.get('rpid'),  # 根评论ID
            'parent_id': reply.get('parent'),  # 父评论ID
            'is_reply': is_reply,  # 是否为回复
            'video_oid': oid,  # 视频OID
            
            # 用户信息
            'user_id': member.get('mid'),  # 用户ID
            'username': member.get('uname', ''),  # 用户名
            'user_level': member.get('level_info', {}).get('current_level', 0),  # 用户等级
            
            # 评论内容
            'content': content.get('message', ''),  # 评论内容
            
            # 统计信息
            'like_count': reply.get('like', 0),  # 点赞数
            'reply_count': reply.get('rcount', 0),  # 回复数
            
            # 时间信息
            'ctime': reply.get('ctime', 0),  # 创建时间戳
            'ctime_text': self._timestamp_to_str(reply.get('ctime', 0)),  # 格式化时间
            
            # 其他信息
            'ip_location': reply.get('reply_control', {}).get('location', ''),  # IP归属地
        }
        
        return comment
    
    @staticmethod
    def _timestamp_to_str(timestamp: int) -> str:
        """
        将时间戳转换为可读字符串
        
        Args:
            timestamp: Unix时间戳
            
        Returns:
            格式化后的时间字符串
        """
        from datetime import datetime
        if timestamp:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return ''

