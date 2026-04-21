from analyzer.llm import analyze_contract
from analyzer.heuristics import run_heuristics
from analyzer.report import generate_report
from analyzer.renderer import format_report

import sys

def load_contract(path):
    with open(path, "r") as file:
        return file.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <contract.sol>")
        return

    code = load_contract(sys.argv[1])

    heuristic_results = run_heuristics(code)

    llm_results = analyze_contract(
        code,
        heuristic_findings=heuristic_results
    )

    report = generate_report(heuristic_results, llm_results)

    formatted = format_report(report)

    print(formatted)

if __name__ == "__main__":
    main()