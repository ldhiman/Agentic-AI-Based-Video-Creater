from typing import Type
from pydantic import BaseModel
from ollama import chat


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"

async def generate(prompt: str, schema: Type[BaseModel]) -> BaseModel:
    strict_prompt = f"""
Return confidence strictly as a decimal between 0.0 and 1.0.
No markdown.
No extra text.

{prompt}
"""

    response = chat(
        model=MODEL,
        messages=[{
            'role': 'user',
            'content': strict_prompt,
        }],
        format=schema.model_json_schema(),
        options={'temperature': 0},
        )

    # print(response)

    try:
        return schema.model_validate_json(response["message"]["content"])
    except Exception as e:
        raise ValueError(f"Schema validation failed: {e}") from e