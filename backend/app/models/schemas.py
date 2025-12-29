from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class InputType(str, Enum):
    URL = "url"
    TITLE = "title"

class PaperInput(BaseModel):
    input_type: InputType
    value: str
    
class PaperMetadata(BaseModel):
    title: str
    authors: List[str]
    published_date: Optional[datetime] = None
    summary: str
    pdf_url: Optional[str] = None
    entry_id: str
    source: str = "arxiv"

class AnalysisSection(BaseModel):
    motivation: str = Field(description="Research motivation")
    key_innovations: List[str] = Field(description="List of key innovations")
    methodology: str = Field(description="Methodology framework description")
    limitations: Optional[str] = Field(description="Limitations of the work", default=None)
    future_work: Optional[str] = Field(description="Future work directions", default=None)

class CodeAnalysis(BaseModel):
    has_code: bool = False
    repository_url: Optional[str] = None
    tech_stack: List[str] = []
    structure_overview: Optional[str] = None
    key_algorithms: List[str] = []

class SummaryReport(BaseModel):
    paper_id: str
    metadata: PaperMetadata
    analysis: AnalysisSection
    code_analysis: Optional[CodeAnalysis] = None
    generated_at: datetime = Field(default_factory=datetime.now)
    framework_diagram_desc: Optional[str] = Field(description="Description for generating framework diagram", default=None)

class TaskStatus(str, Enum):
    PENDING = "pending"
    SEARCHING = "searching"
    ANALYZING = "analyzing"
    CODE_ANALYZING = "code_analyzing"
    SUMMARIZING = "summarizing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    message: Optional[str] = None
    result: Optional[SummaryReport] = None
    created_at: datetime
    updated_at: datetime
