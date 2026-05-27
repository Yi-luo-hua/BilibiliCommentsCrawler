# Bilibili Crawler

Bilibili Crawler 是一个 Windows 优先的 B 站评论 / 动态爬取桌面工具。v2.00 起项目迁移为 **Tauri + React + TypeScript** 桌面壳，Python 爬虫逻辑作为本地 sidecar 后端运行，通过本地进程通信完成爬取、扫码登录和 CSV 导出。

> 旧版 Python GUI / 单 exe 代码已保留在 `legacy-python-gui` 分支，主分支后续以安装包桌面应用为主。

## 功能

- 评论爬取：支持视频 BV/AV、动态、专栏链接。
- 子评论爬取：支持主评论和回复，并发抓取回复列表。
- 动态爬取：支持用户空间动态和关注页动态流。
- 扫码登录：关注页动态流可通过 B 站 App 扫码登录。
- 筛选与导出：支持关键词、时间范围、最大页数，导出 CSV。
- 现代桌面 UI：PCL / MAA 风格侧边导航、玻璃面板、运行日志、进度条。
- 自定义背景：支持选择本地背景图、透明度、模糊和恢复默认。
- 本地运行：前端不直接请求网络，爬虫任务由 Python sidecar 后台线程执行。

## 下载使用

前往 [Releases](https://github.com/Yi-luo-hua/BCC/releases) 下载最新安装包：

- `BilibiliCrawler-Setup-2.0.0-x64.exe`

安装后从开始菜单或桌面快捷方式启动即可。首版安装包面向 Windows x64，默认当前用户安装，不需要额外安装 Python 环境。

## 使用方式

### 评论爬取

1. 进入“评论爬取”页面。
2. 输入视频 BV/AV、动态链接、专栏 CV 号或链接。
3. 设置最大页数、排序方式和是否包含子评论。
4. 点击“开始任务”，等待日志和进度完成。
5. 点击“导出 CSV”保存结果。

### 动态爬取

1. 进入“动态爬取”页面。
2. 输入用户 UID 或 `space.bilibili.com/xxx` 链接。
3. 留空目标时会尝试爬关注页动态流，关注页动态流需要扫码登录。
4. 可选设置关键词、时间范围和最大页数。
5. 点击“开始任务”，完成后导出 CSV。

### 界面设置

1. 进入“界面设置”页面。
2. 选择浅色 / 暗色主题。
3. 选择背景图后，应用会复制到安装目录下的 `user-data/backgrounds/`。
4. 调整背景透明度和模糊效果；恢复默认会清空自定义背景。

## 导出字段

评论 CSV 默认字段：

- 评论 ID
- 根评论 ID
- 用户名
- 用户等级
- 评论内容
- 点赞数
- 回复数
- 发布时间
- IP 归属地

动态 CSV 默认字段：

- 动态 ID
- 用户名
- 类型
- 内容
- 发布时间
- 点赞数
- 评论数
- 转发数

## 源码开发

### 环境要求

- Windows 10/11 x64
- Python 3.10+
- Node.js 20+
- pnpm 10.28.0+
- Rust stable MSVC toolchain

### 安装依赖

```powershell
pip install -r requirements.txt
corepack prepare pnpm@10.28.0 --activate
corepack pnpm --dir desktop install
```

### 开发运行

```powershell
corepack pnpm --dir desktop tauri dev
```

### 构建安装包

```powershell
scripts\build_installer.ps1
```

产物位于：

```text
desktop\src-tauri\target\release\bundle\nsis\
```

## 项目结构

```text
assets/                         应用 logo 与图标资源
backend/sidecar.py              Python sidecar 入口
desktop/                        Tauri + React 桌面前端
desktop/src/                    React UI 源码
desktop/src-tauri/              Tauri Rust 壳与打包配置
scripts/build_backend.ps1       构建 Python sidecar
scripts/build_installer.ps1     构建 NSIS 安装包
src/api/                        B 站 API 封装
src/crawler/                    评论 / 动态爬虫
src/exporter/                   CSV 导出
src/processor/                  数据处理
```

## v2.00 更新

- 主架构迁移到 Tauri 2 + React 19 + TypeScript + Vite + Tailwind。
- Python 爬虫逻辑改为 sidecar 后台进程，前端通过 JSON 请求 / 事件通信。
- 发布形式从单 exe 改为 NSIS 安装包。
- 新增 PCL / MAA 风格桌面 UI、玻璃面板、自定义背景、运行日志和进度条。
- 动态图文内容支持多图链接导出。
- 修复扫码登录 cookie 提取、限流重试、CSV 空数据导出等问题。

## 免责声明

本项目仅供学习和研究使用。请遵守 B 站相关协议和法律法规，不要高频请求或滥用接口。
