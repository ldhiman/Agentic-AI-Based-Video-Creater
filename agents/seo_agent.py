from agents.base_agent import BaseAgent
from models.schemas import AgentResult, SEOLLMResponse
from utils.llm import generate

class SEOAgent(BaseAgent):

    async def execute(self, input_data, memory):
        script = memory.read("final_script")["script"]

        full_text = " ".join(frame["text"] for frame in script)

        prompt = f"""
Generate SEO metadata for this YouTube Short.

Script:
{full_text}

Requirements:
- Title under 60 characters
- Description 2-3 sentences
- 5-10 hashtags
- 10-15 tags
- Optimized for CTR
Return structured JSON.
"""

        result = await generate(prompt, SEOLLMResponse)

        return AgentResult(
            output=result.output.model_dump(),
            confidence=result.confidence,
            reasoning=result.reasoning
        )