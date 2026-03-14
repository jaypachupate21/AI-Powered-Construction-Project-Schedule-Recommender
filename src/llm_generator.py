import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def generate_schedule(prompt):
    if not api_key or not endpoint or not deployment:
        return [
            {
                "phase": "Planning",
                "task": "Design Finalization",
                "duration_days": 14,
                "predecessor": None,
                "reasoning": "Fallback schedule because Azure configuration is missing."
            }
        ]

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version
    )

    response = client.chat.completions.create(
        model=deployment,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a construction scheduling expert. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown code fences if present
    if content.startswith("```"):
        lines = content.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines).strip()

    try:
        return json.loads(content)
    except Exception:
        start = content.find("[")
        end = content.rfind("]")
        if start != -1 and end != -1:
            return json.loads(content[start:end + 1])
        raise ValueError(f"Model response was not valid JSON. Raw output:\n{content}")