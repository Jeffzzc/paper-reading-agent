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

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

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
