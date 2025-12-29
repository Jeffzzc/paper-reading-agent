import re
from app.agents.base import BaseAgent
from app.models.schemas import PaperMetadata, CodeAnalysis
import logging

logger = logging.getLogger(__name__)

class CodeAnalysisAgent(BaseAgent):
    async def run(self, metadata: PaperMetadata) -> CodeAnalysis:
        try:
            # Simple heuristic to find github links in summary
            # In a full system, we would scan the PDF full text
            github_pattern = r"https?://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+"
            matches = re.findall(github_pattern, metadata.summary)
            
            has_code = len(matches) > 0
            repo_url = matches[0] if has_code else None
            
            # Simulate analysis (real implementation would clone repo and use LLM to analyze code)
            if has_code:
                return CodeAnalysis(
                    has_code=True,
                    repository_url=repo_url,
                    tech_stack=["Python", "PyTorch"], # Mock
                    structure_overview="The repository contains a standard PyTorch project structure.",
                    key_algorithms=["Transformer implementation", "Custom Loss Function"]
                )
            else:
                return CodeAnalysis(has_code=False)
                
        except Exception as e:
            logger.error(f"Error in CodeAnalysisAgent: {str(e)}")
            return CodeAnalysis(has_code=False)
