from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.models.schemas import PaperInput, TaskResponse
from app.services.workflow import workflow_manager
from app.core.config import get_settings
import uvicorn
import os

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.post("/api/analyze", response_model=TaskResponse)
async def analyze_paper(input_data: PaperInput):
    task_id = await workflow_manager.create_task(input_data)
    task = await workflow_manager.get_task_status(task_id)
    return task

@app.get("/api/status/{task_id}", response_model=TaskResponse)
async def get_status(task_id: str):
    task = await workflow_manager.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/api/history")
async def get_history():
    # In a real app, query database
    return list(workflow_manager.tasks.values())

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
