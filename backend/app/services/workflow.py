from datetime import datetime
import uuid
import asyncio
from typing import Dict, Optional
from app.models.schemas import PaperInput, TaskStatus, TaskResponse, SummaryReport
from app.agents.search_agent import PaperSearchAgent
from app.agents.analysis_agent import PaperAnalysisAgent
from app.agents.code_agent import CodeAnalysisAgent
from app.agents.summary_agent import SummaryAgent
import logging

logger = logging.getLogger(__name__)

class WorkflowManager:
    def __init__(self):
        self.tasks: Dict[str, TaskResponse] = {}
        self.search_agent = PaperSearchAgent()
        self.analysis_agent = PaperAnalysisAgent()
        self.code_agent = CodeAnalysisAgent()
        self.summary_agent = SummaryAgent()

    async def create_task(self, input_data: PaperInput) -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = TaskResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
            message="Task created",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Start background processing
        asyncio.create_task(self._process_task(task_id, input_data))
        
        return task_id

    async def get_task_status(self, task_id: str) -> Optional[TaskResponse]:
        return self.tasks.get(task_id)

    async def _process_task(self, task_id: str, input_data: PaperInput):
        try:
            task = self.tasks[task_id]
            
            # 1. Search
            task.status = TaskStatus.SEARCHING
            task.message = "Searching for paper..."
            metadata = await self.search_agent.run(input_data)
            
            # 2. Analysis
            task.status = TaskStatus.ANALYZING
            task.message = "Analyzing paper content..."
            analysis = await self.analysis_agent.run(metadata)
            
            # 3. Code Analysis
            task.status = TaskStatus.CODE_ANALYZING
            task.message = "Checking for code..."
            code_analysis = await self.code_agent.run(metadata)
            
            # 4. Summary
            task.status = TaskStatus.SUMMARIZING
            task.message = "Generating report..."
            report = await self.summary_agent.run(metadata, analysis, code_analysis)
            
            # Done
            task.result = report
            task.status = TaskStatus.COMPLETED
            task.message = "Processing complete"
            
        except Exception as e:
            logger.error(f"Task {task_id} failed: {str(e)}")
            task = self.tasks[task_id]
            task.status = TaskStatus.FAILED
            task.message = f"Error: {str(e)}"

# Singleton instance
workflow_manager = WorkflowManager()
