from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_response(query, answer, context):

    evaluation_prompt = f"""
You are evaluating a legal AI system.

Question:
{query}

Retrieved Context:
{context}

Generated Answer:
{answer}

Score the following from 1 to 5:

1. Context Relevance (Are retrieved chunks relevant to question?)
2. Faithfulness (Is answer grounded only in context?)
3. Answer Relevance (Does answer properly address the question?)

Respond ONLY in this JSON format:
{{
  "context_relevance": score,
  "faithfulness": score,
  "answer_relevance": score
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": evaluation_prompt}],
        temperature=0
    )

    return response.choices[0].message.content