# Smart Contract Vulnerability Auditor 

A hybrid Solidity security analysis tool that combines deterministic static-analysis heuristics with LLM-assisted validation to identify, explain, and prioritize smart contract vulnerabilities.

The project was built to explore how traditional static analysis and AI-assisted reasoning can be combined to improve audit quality while reducing false positives and hallucinated findings.

---

## Overview

This tool analyzes Solidity smart contracts and generates structured security reports.

Unlike purely LLM-based approaches, findings are first generated using deterministic heuristics and then reviewed by an LLM that:

- Validates heuristic findings
- Rejects weak or unsupported detections
- Adds strongly justified vulnerabilities
- Generates exploitability analysis
- Suggests remediation guidance

The result is a hybrid auditing workflow that combines the consistency of static analysis with the contextual reasoning capabilities of modern language models.

---

## Features

### Hybrid Analysis Pipeline
The analyzer combines:
- Rule-based heuristic detection
- LLM-assisted vulnerability validation
- Exploitability assessment
- Report normalization and scoring

### Vulnerability Detection
Current heuristic coverage includes:
- Reentrancy
- Missing Access Control
- tx.origin Authentication
- Delegatecall Usage
- Unchecked Low-Level Calls
- Timestamp Dependence
- Block Number Dependence
- Weak Randomness
- Selfdestruct Usage
- Inline Assembly Detection

### Exploitability Analysis
Each validated issue may include:
- Exploit feasibility
- Preconditions
- Attack steps
- Expected impact
- Remediation guidance

### Structured Reporting
Generated reports contain:
- Severity summary
- Vulnerability details
- Exploit analysis
- Recommended fixes
- Runtime statistics

### Benchmark Framework
The project includes an automated benchmarking pipeline capable of:
- Auditing multiple contracts
- Saving JSON reports
- Comparing findings against labeled ground truth
- Computing evaluation metrics

---

## Architecture
Solidity Contract
->
Heuristic Analysis Layer
->
LLM Validation Layer
->
Finding Normalization
->
Validation & Deduplication
->
Report Generation
->
CLI Output / JSON Output


---

## Project Structure

smart-contract-auditor/

|-> analyzer/
│ |-> __init__.py
│ |-> heuristics.py
│ |-> llm.py
│ |-> parser.py
│ |-> renderer.py
│ |-> report.py
│
|-> contracts/
|
|-> results/
|
|-> benchmark.py
|-> evaluate.py
|-> labels.json
|-> main.py
|
|-> README.md
|-> .env
|-> .gitignore


---

## Installation

Clone the repository:

git clone https://github.com/your-username/smart-contract-auditor.git
cd smart-contract-auditor

Create and activate a virtual environment:

python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

OPENAI_API_KEY=your_api_key


---

## Usage

Analyze a single contract:

python main.py contracts/V01_Reentrancy.sol


---

## Example Output

==================================================
SMART CONTRACT SECURITY AUDIT REPORT
==================================================

SUMMARY

High: 1
Medium: 1
Low: 0
Total: 2

ISSUE 1: Potential Reentrancy (HIGH)

Location:
withdraw()

Explanation:
External value transfer detected before state update.

Exploit Analysis:

Preconditions:
- Contract contains user balances
- Contract holds funds

Attack Steps:
- Attacker deposits funds
- Attacker initiates withdrawal
- Fallback function re-enters contract
- Funds are repeatedly withdrawn

Impact:
Potential loss of contract funds

Fix:
Use Checks-Effects-Interactions or ReentrancyGuard.


---

## Benchmarking

Run all benchmark contracts:

python benchmark.py

This generates JSON reports inside:

results/


---

## Evaluation

Compute benchmark statistics:

python evaluate.py

Example output:

============================================================
EVALUATION RESULTS
============================================================

Contracts Tested: 20

True Positives : 17
False Positives: 4
False Negatives: 2

Precision: 80.95%
Recall: 89.47%
F1 Score: 85.00%
============================================================


---

## Design Goals

### Grounded AI Reasoning

The LLM is not used as a standalone auditor.

Heuristic findings provide grounding signals that guide and constrain model reasoning.

### Reduced Hallucinations

The validation layer attempts to suppress unsupported findings and downgrade weak exploitability claims.

### Explainability

Every finding includes:

- Explanation
- Severity
- Location
- Remediation guidance
- Exploitability assessment

### Reproducibility

The benchmarking framework enables repeatable evaluation using labeled contracts and measurable metrics.


---

## Current Limitations
- Regex-based analysis rather than AST parsing
- No symbolic execution
- No data-flow analysis
- No control-flow graph generation
- No automated exploit generation
- LLM output quality depends on model capability

This tool is intended as a research and portfolio project rather than a production-grade auditing platform.


---

## Future Improvements

- Solidity AST parsing
- Function-level analysis
- Data-flow tracking
- Symbolic execution
- Confidence scoring
- CI/CD integration
- Comparative evaluation against Slither and Mythril
- Expanded benchmark datasets


---

## Motivation

Traditional smart contract security tools often fall into two categories:

- Static analyzers that are fast and deterministic but limited in contextual reasoning
- LLM-based systems that are flexible but may hallucinate findings

This project explores a hybrid approach that combines the strengths of both methods.


---

## Disclaimer

This software is intended for educational, research, and portfolio purposes only.

It should not be relied upon as a substitute for professional smart contract security audits.


---

## Author

Built as a portfolio project focused on:

- Smart Contract Security
- Static Analysis
- AI-Assisted Security Tooling
- Vulnerability Research
- Hybrid Reasoning Systems 