import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


class WaterIntakeAgent:
    def analyze_intake(self, intake_ml):
        prompt = f"""
You are a hydration assistant.
User drank {intake_ml} ml of water today.
Provide hydration status and suggestion.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    agent = WaterIntakeAgent()
    print(agent.analyze_intake(1500))