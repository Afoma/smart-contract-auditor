# Smart Contract Vulnerability Auditor (AI + Heuristics Hybrid)

A CLI-based smart contract security analysis tool that combines deterministic static heuristics with LLM-based reasoning to identify, validate, and explain vulnerabilities in Solidity contracts.

---

## Overview

This tool analyzes Solidity smart contracts and produces structured security audit reports. It is designed to improve reliability over pure LLM-based analysis by grounding model outputs in heuristic detection signals and applying post-generation validation.

The system focuses on:
- Vulnerability detection (e.g., reentrancy, missing access control)
- Explainability (simple, structured reasoning)
- Exploit feasibility modeling
- Reduction of LLM hallucinations via heuristic grounding

---

## Key Features

### Hybrid Analysis Pipeline
Combines:
- Rule-based heuristic detection (fast, deterministic signals)
- LLM-based reasoning (contextual vulnerability analysis)
- Validation layer to filter weak or non-feasible findings

### Vulnerability Detection
Currently detects:
- Potential reentrancy patterns
- Missing access control in public/external functions

### Exploit Feasibility Modeling
Each vulnerability includes:
- Preconditions required for exploitation
- Step-by-step attack scenario (when feasible)
- Expected attacker impact
- Confidence filtering for realism

### Structured Audit Output
Generates a CLI-formatted security report including:
- Severity breakdown (High / Medium / Low)
- Normalized vulnerability list
- Exploit analysis (when applicable)
- Suggested fixes

---

## Architecture
Solidity Contract
->
Heuristic Analyzer (rule-based detection)
->
LLM Reasoning Layer (grounded by heuristics)
->
Validation Layer (filters weak or unrealistic findings)
->
Report Generator (normalization + scoring)
->
CLI Renderer (human-readable audit output)


---

## Design Goals

- **Grounded LLM reasoning**: Model outputs are constrained using heuristic signals
- **Reduced hallucinations**: Vulnerabilities without realistic exploit paths are downgraded
- **Security-first design**: Focus on exploitability, not just detection
- **Explainability**: Every issue includes reasoning and remediation guidance

---

## Tech Stack

- Python 3.10+
- OpenAI API (LLM reasoning layer)
- Regex-based heuristic analysis
- CLI-based execution (no frontend dependencies)

---

## Installation

*** bash


git clone https://github.com/your-username/smart-contract-auditor.git
cd smart-contract-auditor
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

Create a .env file:

OPENAI_API_KEY=your_api_key

Usage

Run analysis on a Solidity file:

Example Output
SMART CONTRACT SECURITY AUDIT REPORT
=====================================

SUMMARY
- High: 1
- Medium: 2
- Low: 1
- Total: 4

ISSUE 1: Potential Reentrancy (HIGH)
Location: withdraw()

Explanation:
External call may allow reentrancy before state update.

Exploit Analysis:
Preconditions:
- Attacker can deploy a malicious contract
- Contract holds sufficient balance

Attack Steps:
- Attacker calls withdraw()
- Fallback function re-enters contract
- Balance is drained before state update

Impact:
Full drainage of contract funds

Fix:
Use checks-effects-interactions pattern or ReentrancyGuard
Limitations
Heuristic coverage is intentionally minimal and pattern-based
LLM may still produce uncertain or incomplete exploit reasoning
No full AST parsing or symbolic execution is currently implemented
Designed for educational and research purposes, not production auditing
Motivation

Smart contract auditing tools often suffer from a tradeoff between:

static analyzers (precise but shallow)
LLM-based tools (flexible but unreliable)

This project explores a hybrid approach where:

heuristics provide grounding signals
LLMs provide reasoning and explanation
validation logic enforces exploit realism
Future Improvements
AST-based Solidity parsing (e.g. Slither-style analysis)
Function-level slicing for improved context windows
Exploit simulation scoring system
False-positive reduction via confidence scoring
Integration with CI pipelines for automated auditing
Disclaimer

This tool is intended for educational and research purposes only. It is not a replacement for professional security audits.

Author

Built as a portfolio project focused on AI-assisted security analysis and hybrid reasoning systems for smart contract vulnerability detection.

python main.py contracts/unsafe_withdraw.sol
