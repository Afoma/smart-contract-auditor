from analyzer.llm import analyze_contract
from analyzer.heuristics import run_heuristics
from analyzer.report import generate_report
from analyzer.renderer import format_report

import sys
import os
import time


def load_contract(path):
    """
    Loads a Solidity contract from disk.

    Raises:
        FileNotFoundError
        IOError
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py contracts/MyContract.sol")
        return

    contract_path = sys.argv[1]

    if not os.path.exists(contract_path):
        print(f"Error: '{contract_path}' does not exist.")
        return

    try:
        code = load_contract(contract_path)
    except Exception as e:
        print(f"Failed to read contract:\n{e}")
        return

    print("=" * 60)
    print("Running Hybrid Smart Contract Audit...")
    print("=" * 60)

    start = time.perf_counter()

    heuristic_results = run_heuristics(code)

    llm_results = analyze_contract(
        code,
        heuristic_findings=heuristic_results
    )

    report = generate_report(
        heuristic_results,
        llm_results
    )

    formatted = format_report(report)

    elapsed = time.perf_counter() - start

    print(formatted)

    print()
    print("=" * 60)
    print(f"Analysis completed in {elapsed:.3f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()