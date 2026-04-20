from analyzer.llm import analyze_contract
import sys

def load_contract(path):
    with open(path, "r") as file:
        return file.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <contract.sol>")
        return

    contract_path = sys.argv[1]
    code = load_contract(contract_path)

    print("\n=== ANALYZING CONTRACT ===\n")

    result = analyze_contract(code)

    print("\n=== ANALYSIS RESULT ===\n")
    print(result)

if __name__ == "__main__":
    main()