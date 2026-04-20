from analyzer.llm import analyze_contract
from analyzer.heuristics import run_heuristics
import sys
import json

def load_contract(path):
    with open(path, "r") as file:
        return file.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <contract.sol>")
        return

    code = load_contract(sys.argv[1])

    print("\n=== HEURISTIC ANALYSIS ===\n")
    heuristic_findings = run_heuristics(code)
    print(json.dumps(heuristic_findings, indent=2))

    print("\n=== LLM ANALYSIS ===\n")
    llm_findings = analyze_contract(code)

    print(json.dumps(llm_findings, indent=2))

if __name__ == "__main__":
    main()