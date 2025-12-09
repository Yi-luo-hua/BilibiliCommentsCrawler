"""
B站评论爬虫配置文件
"""
# B站评论API端点
COMMENT_API_URL = "https://api.bilibili.com/x/v2/reply/main"
REPLY_API_URL = "https://api.bilibili.com/x/v2/reply/reply"

# 请求头配置
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Origin": "https://www.bilibili.com",
}

# 请求配置
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）
REQUEST_DELAY = 0.5   # 请求间隔（秒），避免请求过快
MAX_RETRIES = 3       # 最大重试次数

# 分页配置
DEFAULT_PAGE_SIZE = 20  # 每页评论数量
MAX_PAGES = 1000        # 最大爬取页数（防止无限爬取）

# CSV导出配置
CSV_ENCODING = "utf-8-sig"  # 使用UTF-8 with BOM，Excel可以正确识别中文

