import os
import json
import time

from analyzer.heuristics import run_heuristics
from analyzer.llm import analyze_contract
from analyzer.report import generate_report


CONTRACT_DIR = "contracts"
RESULTS_DIR = "results"
LABEL_FILE = "labels.json"


def load_contract(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ensure_results_dir():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def save_report(contract_name, report):

    output_file = os.path.join(
        RESULTS_DIR,
        contract_name.replace(".sol", ".json")
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=2
        )


def analyze_single_contract(contract_file):

    path = os.path.join(
        CONTRACT_DIR,
        contract_file
    )

    code = load_contract(path)

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

    runtime = time.perf_counter() - start

    return report, runtime


def benchmark():

    ensure_results_dir()

    runtimes = []

    contracts = sorted(
        f for f in os.listdir(CONTRACT_DIR)
        if f.endswith(".sol")
    )

    print("=" * 60)
    print("SMART CONTRACT BENCHMARK")
    print("=" * 60)

    for contract in contracts:

        print(f"Analyzing {contract}...")

        report, runtime = analyze_single_contract(
            contract
        )

        runtimes.append(runtime)

        save_report(
            contract,
            report
        )

    avg_runtime = (
        sum(runtimes) / len(runtimes)
        if runtimes else 0
    )

    print()
    print("=" * 60)
    print("Benchmark Complete")
    print("=" * 60)

    print(f"Contracts: {len(contracts)}")
    print(
        f"Average Runtime: "
        f"{avg_runtime:.3f} sec"
    )


if __name__ == "__main__":
    benchmark()