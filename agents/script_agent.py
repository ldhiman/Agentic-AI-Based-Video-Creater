from agents.base_agent import BaseAgent
from models.schemas import ScriptLLMResponse
from utils.llm import generate

class ScriptAgent(BaseAgent):
    async def execute(self, input_data, memory):
        topic = input_data["planner"]["output"]["topic"]
        research = input_data["research"]["output"]
        key_points = research["key_points"]
        audience_angle = research["audience_angle"]
        compliance_notes = research["compliance_notes"]

        variation = self.name  # script_a or script_b

        prompt = f"""
Create a YouTube Short structured into frames.

Topic: {topic}

Key Points:
{key_points}

Target Audience:
{audience_angle}

Compliance Notes:
{compliance_notes}

Requirements:
- 5–7 frames
- Each frame: text, image_prompt, duration (2–5 seconds)
- Strong hook in first frame
- Avoid medical claims

Each frame must include:
- text: narration text
- image_prompt: detailed visual description for image generation
- duration: integer seconds (2–5)

Total video length should be under 30 seconds.

Variation ID: {variation}

Each script must:
- Image must be 3D pixal styled
- Use a different storytelling style
- Different tone (energetic, calm, minimalist, dramatic)
- Different hook strategy (question, bold claim, challenge, statistic)
- Avoid repeating structure used in other scripts
"""

        raw = await generate(prompt, ScriptLLMResponse)
        return raw