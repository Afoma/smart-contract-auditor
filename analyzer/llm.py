import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_contract(code):
    prompt = f"""
You are a smart contract security auditor.

Analyze the Solidity contract and return ONLY valid JSON.

Format:
[
  {{
    "name": "Vulnerability name",
    "severity": "low | medium | high",
    "explanation": "Simple explanation",
    "location": "Code snippet or function",
    "fix": "Suggested fix"
  }}
]

Rules:
- Be concise but precise
- Only include real issues
- If no issues, return []

Contract:
{code}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise and critical smart contract auditor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by model",
            "raw": raw
        }