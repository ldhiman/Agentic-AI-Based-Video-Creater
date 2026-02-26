from agents.base_agent import BaseAgent
from models.schemas import AgentResult, ThumbnailLLMResponse    
from utils.llm import generate


class ThumbnailAgent(BaseAgent):

    async def execute(self, input_data, memory):
        topic = memory.read("planner")["output"]["topic"]

        prompt = f"""
Create a high-CTR YouTube Shorts thumbnail concept.

Topic: {topic}

Return:
- Detailed image generation prompt (vertical 9:16)
- 3-5 word bold overlay text

Style:
- High contrast
- Bright colors
- Eye-catching
- 3D pixel style
"""

        result = await generate(prompt, ThumbnailLLMResponse)

        return AgentResult(
            output=result.output.model_dump(),
            confidence=result.confidence,
            reasoning=result.reasoning
        )