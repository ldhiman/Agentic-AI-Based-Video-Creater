from agents.base_agent import BaseAgent
from models.schemas import AgentResult
from utils.llm import generate
from models.schemas import ResearchLLMResponse

class ResearchAgent(BaseAgent):

    async def execute(self, input_data, memory):

        topic = input_data["planner"]["output"]["topic"]

        prompt = f"""
Research the topic: {topic}

Provide:
- 5 concise key factual points
- A suggested audience angle (e.g., busy students, gym-goers, etc.)
- Compliance notes (avoid medical claims, exaggeration, etc.)

Keep concise.
"""

        result = await generate(prompt, ResearchLLMResponse)

        return AgentResult(
            output=result.output.model_dump(),
            confidence=result.confidence,
            reasoning=result.reasoning
        )