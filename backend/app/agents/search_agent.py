import arxiv
import logging
from typing import Optional
from app.agents.base import BaseAgent
from app.models.schemas import PaperInput, PaperMetadata, InputType
from datetime import datetime

logger = logging.getLogger(__name__)

class PaperSearchAgent(BaseAgent):
    async def run(self, input_data: PaperInput) -> PaperMetadata:
        try:
            client = arxiv.Client()
            search = None

            if input_data.input_type == InputType.URL:
                # Extract ID from URL (naive implementation)
                # Example: https://arxiv.org/abs/2310.12345
                paper_id = input_data.value.split("/")[-1].replace(".pdf", "")
                search = arxiv.Search(id_list=[paper_id])
            else:
                # Search by title
                search = arxiv.Search(
                    query=f"ti:{input_data.value}",
                    max_results=1,
                    sort_by=arxiv.SortCriterion.Relevance
                )

            results = list(client.results(search))
            
            if not results:
                raise Exception("No paper found")

            paper = results[0]
            
            # Download PDF if needed later, for now just metadata
            # paper.download_pdf(dirpath="./uploads", filename=f"{paper.get_short_id()}.pdf")

            metadata = PaperMetadata(
                title=paper.title,
                authors=[a.name for a in paper.authors],
                published_date=paper.published,
                summary=paper.summary,
                pdf_url=paper.pdf_url,
                entry_id=paper.entry_id,
                source="arxiv"
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error in PaperSearchAgent: {str(e)}")
            raise e
