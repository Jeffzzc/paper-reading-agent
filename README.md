# Paper Reading Agent System

一个自动阅读计算机方向论文的智能体框架系统，集成论文搜索、分析、代码检测与总结功能。

## 系统架构

- **后端**: Python (FastAPI)
- **AI**: LangChain + OpenAI GPT-4
- **前端**: Vue.js 3 + Tailwind CSS (静态文件服务)
- **数据库**: MongoDB (可选，默认支持)

## 功能模块

1.  **Paper Search Agent**: 集成 arXiv API，支持 URL 和标题搜索。
2.  **Paper Analysis Agent**: 使用 LLM 提取动机、创新点、方法论。
3.  **Code Analysis Agent**: 检测并分析关联代码仓库。
4.  **Summary Agent**: 生成结构化报告。

## 快速开始

### 1. 环境准备

确保已安装 Python 3.10+。

### 2. 快速启动 (Windows)

直接双击运行根目录下的 `run_server.bat` 脚本。
该脚本会自动：
1. 创建虚拟环境 (`backend/venv`)
2. 安装所需依赖
3. 启动后端服务

### 3. 手动安装与运行

如果你偏好手动操作：

```bash
cd backend
# 创建虚拟环境
python -m venv venv
# 激活虚拟环境
.\venv\Scripts\activate
# 安装依赖
pip install -r requirements.txt
# 运行
python -m app.main
```

### 4. 配置环境变量

复制 `backend/.env` 并填入你的 OpenAI API Key。

```ini
OPENAI_API_KEY="sk-..."
```

### 4. 运行系统

```bash
cd backend
python -m app.main
```

系统将在 `http://localhost:8000` 启动。
直接访问该地址即可使用 Web 界面。

## Docker 部署

```bash
cd backend
docker build -t paper-reading-agent .
docker run -p 8000:8000 paper-reading-agent
```

## 目录结构

```
backend/
├── app/
│   ├── agents/          # 智能体实现
│   ├── models/          # 数据模型
│   ├── services/        # 业务逻辑与工作流
│   ├── core/            # 配置
│   └── main.py          # API 入口
├── static/              # 前端静态资源
├── Dockerfile
└── requirements.txt
```
