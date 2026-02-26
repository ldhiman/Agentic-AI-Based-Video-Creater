from agents.base_agent import BaseAgent
from models.schemas import PlannerLLMResponse
from utils.llm import generate


class PlannerAgent(BaseAgent):
    async def execute(self, input_data, memory):

        prompt = """
Generate one healthy food topic suitable for a 30 second YouTube Short.
Avoid medical claims.
Keep topic concise.
Return structured JSON.
"""

        raw = await generate(prompt, PlannerLLMResponse)

        return raw