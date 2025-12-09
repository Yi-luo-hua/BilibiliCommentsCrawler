"""
数据处理和清洗模块
"""
from typing import List, Dict, Optional


class DataProcessor:
    """数据处理器类"""
    
    @staticmethod
    def clean_comments(comments: List[Dict]) -> List[Dict]:
        """
        清洗评论数据
        
        Args:
            comments: 原始评论列表
            
        Returns:
            清洗后的评论列表
        """
        cleaned = []
        for comment in comments:
            # 移除空评论
            if not comment.get('content', '').strip():
                continue
            
            # 清理内容中的特殊字符
            content = comment.get('content', '')
            # 移除多余的空白字符
            content = ' '.join(content.split())
            comment['content'] = content
            
            # 确保所有必需字段都存在
            comment.setdefault('comment_id', 0)
            comment.setdefault('root_id', 0)
            comment.setdefault('parent_id', 0)
            comment.setdefault('is_reply', False)
            comment.setdefault('user_id', 0)
            comment.setdefault('username', '')
            comment.setdefault('user_level', 0)
            comment.setdefault('like_count', 0)
            comment.setdefault('reply_count', 0)
            comment.setdefault('ctime', 0)
            comment.setdefault('ctime_text', '')
            comment.setdefault('ip_location', '')
            
            cleaned.append(comment)
        
        return cleaned
    
    @staticmethod
    def flatten_comments(comments: List[Dict]) -> List[Dict]:
        """
        扁平化评论数据（主评论和子评论在同一层级）
        
        Args:
            comments: 评论列表（可能包含主评论和子评论）
            
        Returns:
            扁平化后的评论列表
        """
        # 数据已经是扁平化的（在爬取时已经处理）
        # 这里主要是确保数据结构一致
        flattened = []
        for comment in comments:
            flattened.append(comment.copy())
        
        return flattened
    
    @staticmethod
    def validate_comment(comment: Dict) -> bool:
        """
        验证评论数据是否有效
        
        Args:
            comment: 评论字典
            
        Returns:
            如果评论有效返回True，否则返回False
        """
        # 检查必需字段
        required_fields = ['comment_id', 'content', 'user_id', 'username']
        for field in required_fields:
            if field not in comment:
                return False
        
        # 检查内容不为空
        if not comment.get('content', '').strip():
            return False
        
        return True
    
    @staticmethod
    def filter_comments(comments: List[Dict], filters: Optional[Dict] = None) -> List[Dict]:
        """
        过滤评论
        
        Args:
            comments: 评论列表
            filters: 过滤条件字典，例如：
                {
                    'min_likes': 10,  # 最小点赞数
                    'min_level': 3,   # 最小用户等级
                    'keyword': '关键词',  # 内容关键词
                }
        
        Returns:
            过滤后的评论列表
        """
        if not filters:
            return comments
        
        filtered = []
        for comment in comments:
            # 按点赞数过滤
            if 'min_likes' in filters:
                if comment.get('like_count', 0) < filters['min_likes']:
                    continue
            
            # 按用户等级过滤
            if 'min_level' in filters:
                if comment.get('user_level', 0) < filters['min_level']:
                    continue
            
            # 按关键词过滤
            if 'keyword' in filters:
                keyword = filters['keyword'].lower()
                if keyword not in comment.get('content', '').lower():
                    continue
            
            filtered.append(comment)
        
        return filtered
    
    @staticmethod
    def get_statistics(comments: List[Dict]) -> Dict:
        """
        获取评论统计信息
        
        Args:
            comments: 评论列表
            
        Returns:
            统计信息字典
        """
        if not comments:
            return {
                'total': 0,
                'main_comments': 0,
                'replies': 0,
                'total_likes': 0,
                'avg_likes': 0,
                'total_replies': 0,
            }
        
        main_comments = [c for c in comments if not c.get('is_reply', False)]
        replies = [c for c in comments if c.get('is_reply', False)]
        
        total_likes = sum(c.get('like_count', 0) for c in comments)
        total_replies = sum(c.get('reply_count', 0) for c in main_comments)
        
        return {
            'total': len(comments),
            'main_comments': len(main_comments),
            'replies': len(replies),
            'total_likes': total_likes,
            'avg_likes': round(total_likes / len(comments), 2) if comments else 0,
            'total_replies': total_replies,
        }

