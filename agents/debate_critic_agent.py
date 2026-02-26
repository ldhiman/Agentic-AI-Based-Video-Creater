from agents.base_agent import BaseAgent
from models.schemas import DebateLLMResponse, AgentResult
from utils.llm import generate


class DebateCriticAgent(BaseAgent):

    async def execute(self, input_data, memory):

        # Collect all script names dynamically
        script_names = [
            name.replace("critic_", "")
            for name in input_data.keys()
            if name.startswith("critic_script_")
        ]

        approved_scripts = []

        for script_name in script_names:
            critic_name = f"critic_{script_name}"
            approved = input_data[critic_name]["output"]["approved"]

            if approved:
                script_text = input_data[script_name]["output"]["script"]
                approved_scripts.append((script_name, script_text))

        # If none approved → regenerate logic handled upstream
        if not approved_scripts:
            return AgentResult(
                output={"winner": None},
                confidence=0.1,
                reasoning="No approved scripts"
            )

        # If only one approved → auto select
        if len(approved_scripts) == 1:
            winner_name, script = approved_scripts[0]
            memory.write("final_script", {"script": script})
            return AgentResult(
                output={"winner": winner_name},
                confidence=0.9,
                reasoning="Only one script approved"
            )

        # If multiple approved → compare all
        comparison_text = "\n\n".join(
            [f"{name}:\n{text}" for name, text in approved_scripts]
        )

        prompt = f"""
You are a content evaluator.

Compare the following scripts and choose the best one.

Criteria:
- Engagement
- Clarity
- Retention
- Compliance

Return:
- winner: script name exactly as given
- reason

Score each script between 0.0 and 1.0.

Scripts:
{comparison_text}
"""

        result = await generate(prompt, DebateLLMResponse)

        winner = result.output.winner

        selected_script = dict(approved_scripts)[winner]
        memory.write("final_script", {"script": selected_script})

        return result