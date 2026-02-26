from agents.base_agent import BaseAgent
from models.schemas import AgentResult, RetentionLLMResponse
from utils.llm import generate


class RetentionAgent(BaseAgent):

    async def execute(self, input_data, memory):
        script = memory.read("final_script")["script"]
        first_frame = script[0]["text"]

        prompt = f"""
Improve this hook to maximize 3-second retention:

Hook:
{first_frame}

Make it more curiosity-driven.
Return only improved hook.
"""

        result = await generate(prompt, RetentionLLMResponse)

        script[0]["text"] = result.output.improved_hook
        memory.write("final_script", {"script": script})

        return AgentResult(
            output={"improved_hook": result.output.improved_hook},
            confidence=result.confidence,
            reasoning=result.reasoning
        )