from app.agents.base import BaseAgent
from app.models.schemas import PaperMetadata, AnalysisSection, CodeAnalysis, SummaryReport
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SummaryAgent(BaseAgent):
    async def run(self, metadata: PaperMetadata, analysis: AnalysisSection, code_analysis: CodeAnalysis) -> SummaryReport:
        try:
            # In a complex system, this agent might re-write or format the content using an LLM
            # based on user preferences (e.g., "explain like I'm 5").
            # Here we aggregate the structured data.
            
            # Generate a description for a framework diagram based on methodology
            diagram_desc = f"A flowchart showing the process: {analysis.methodology[:200]}..."
            
            report = SummaryReport(
                paper_id=metadata.entry_id,
                metadata=metadata,
                analysis=analysis,
                code_analysis=code_analysis,
                generated_at=datetime.now(),
                framework_diagram_desc=diagram_desc
            )
            
            return report
            
        except Exception as e:
            logger.error(f"Error in SummaryAgent: {str(e)}")
            raise e
