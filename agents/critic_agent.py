from agents.base_agent import BaseAgent
from models.schemas import AgentResult, CriticLLMResponse
from utils.llm import generate

class CriticAgent(BaseAgent):

    async def execute(self, input_data, memory):
        script_name = self.name.replace("critic_", "")

        frames = input_data[script_name]["output"]["script"]


        total_duration = sum(frame["duration"] for frame in frames)


        prompt = f"""
You are evaluating a short-form video structured into frames.

Each frame contains:
- text
- image_prompt
- duration

Evaluate:

1. Hook strength (frame 0)
2. Visual diversity across image_prompts
3. Narrative coherence
4. Engagement
5. Avoid medical claims
6. Avoid exaggeration

Total duration: {total_duration} seconds

Frames:
{frames}

Return ONLY actual problems in "issues".
If no issues found, return an empty list.
Do NOT include metric descriptions.
Do NOT restate scores.

Return structured scoring.
"""

        result = await generate(prompt, CriticLLMResponse)

        hook = result.output.hook_score
        visual = result.output.visual_diversity_score
        coherence = result.output.coherence_score

        calculated_score  = (hook + visual + coherence) / 3
        # Deterministic enforcement
        approved = (
            calculated_score  >= 0.75
            and 15 <= total_duration <= 30
        )

        

        return AgentResult(
            output={
                "score": calculated_score,
                "issues": result.output.issues,
                "approved": approved,
                "hook_score": hook,
                "visual_diversity_score": visual,
                "coherence_score": coherence,
                "total_duration": total_duration
            },
            confidence=result.confidence,
            reasoning=result.reasoning
        )