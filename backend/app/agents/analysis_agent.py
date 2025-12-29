from typing import Any
from app.agents.base import BaseAgent
from app.models.schemas import PaperMetadata, AnalysisSection
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class PaperAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY or "sk-mock-key", # Fallback for demo
            model=settings.OPENAI_MODEL,
            temperature=0
        )
        self.parser = PydanticOutputParser(pydantic_object=AnalysisSection)

    async def run(self, metadata: PaperMetadata) -> AnalysisSection:
        try:
            # In a real system, we would download the PDF and extract full text here.
            # For this demo, we will use the abstract (summary) as the source text,
            # which is often sufficient for high-level analysis.
            text_to_analyze = f"Title: {metadata.title}\n\nAbstract: {metadata.summary}"
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert computer science researcher. Analyze the following paper information and extract key insights."),
                ("user", "Analyze the following paper content:\n\n{text}\n\nProvide the output in the specified format.\n{format_instructions}")
            ])

            chain = prompt | self.llm | self.parser
            
            if not settings.OPENAI_API_KEY:
                # Mock response if no API key is present
                logger.warning("No OpenAI API Key found, returning mock analysis.")
                return AnalysisSection(
                    motivation="The paper addresses the limitation of X in existing systems.",
                    key_innovations=["Novel architecture Y", "Improved efficiency by Z%"],
                    methodology="The authors propose a transformer-based framework...",
                    limitations="Limited to static datasets.",
                    future_work="Extend to real-time processing."
                )

            result = await chain.ainvoke({
                "text": text_to_analyze,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            return result

        except Exception as e:
            logger.error(f"Error in PaperAnalysisAgent: {str(e)}")
            # Return a fallback/empty result on error to avoid crashing the workflow
            return AnalysisSection(
                motivation="Error analyzing paper",
                key_innovations=[],
                methodology="Error",
            )
