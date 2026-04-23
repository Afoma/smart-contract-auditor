import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_contract(code, heuristic_findings=None):
    heuristic_context = json.dumps(heuristic_findings or [], indent=2)

    prompt = f"""
You are a strict smart contract security auditor.

You are given:
1. Solidity contract code
2. Heuristic findings from a static analyzer

Your task:
- Validate heuristic findings (keep or reject them)
- Add missing vulnerabilities ONLY if strongly justified
- Remove false positives
- Improve explanations and fixes

IMPORTANT RULES:
- Do NOT invent issues without evidence in code
- Prefer precision over completeness
- Be strict about severity classification

Return ONLY valid JSON in this format:

[
  {{
    "name": "...",
    "severity": "low | medium | high",
    "explanation": "...",
    "location": "...",
    "fix": "...",
    "exploit_scenario": ["step-by-step attack path"],
    "source": "heuristic | llm"
  }}
]

Rules for exploit_scenario:
- Only include if realistically exploitable
- Must be step-by-step attacker actions
- If not exploitable, return []

Heuristic Findings:
{heuristic_context}

Contract:
{code}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict smart contract security reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    raw = response.choices[0].message.content

    # Handle markdown-wrapped JSON
    if raw.startswith("```"):
        raw = raw.strip("```json").strip("```").strip()

    try:
        return json.loads(raw)
    except:
        return [{"error": "invalid_json", "raw": raw}]