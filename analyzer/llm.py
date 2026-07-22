import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def extract_json(text):
    """
    Attempts to recover JSON from model output.
    Handles markdown fences and extra text.
    """

    if not text:
        return None

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    start = text.find("[")
    end = text.rfind("]")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text


def analyze_contract(
    code,
    heuristic_findings=None
):

    heuristic_context = json.dumps(
        heuristic_findings or [],
        indent=2
    )

    prompt = f"""
You are an expert Solidity smart contract auditor.

You are given:

1. Solidity source code
2. Findings from a static analyzer

Your responsibilities:

- Validate heuristic findings
- Reject false positives
- Add missing vulnerabilities only when strongly justified
- Do NOT invent issues
- Do NOT report informational observations
- Do NOT report style concerns
- Do NOT report gas optimizations
- Only report actual security vulnerabilities

Severity rules:

high:
- loss of funds
- privilege escalation
- contract takeover

medium:
- meaningful security weakness
- exploitable under realistic conditions

low:
- limited impact
- difficult exploitation

Return ONLY valid JSON.

Schema:

[
  {{
    "name": "...",
    "severity": "low|medium|high",
    "explanation": "...",
    "location": "...",
    "fix": "...",
    "exploit": {{
      "possible": true,
      "preconditions": [],
      "steps": [],
      "impact": "...",
      "notes": "..."
    }},
    "source": "heuristic|llm"
  }}
]

If no vulnerabilities exist:

[]

Heuristic Findings:

{heuristic_context}

Contract:

{code}
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,
            messages=[
                {
                    "role": "system",
                    "content":
                    (
                        "You are a strict smart contract "
                        "security reviewer."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        raw = response.choices[0].message.content

        raw = extract_json(raw)

        if not raw:

            return [
                {
                    "error": "empty_response"
                }
            ]

        try:

            parsed = json.loads(raw)

            if isinstance(parsed, list):
                return parsed

            return [
                {
                    "error": "unexpected_format"
                }
            ]

        except json.JSONDecodeError:

            return [
                {
                    "error": "invalid_json",
                    "raw": raw
                }
            ]

    except Exception as e:

        return [
            {
                "error": "llm_failure",
                "message": str(e)
            }
        ]