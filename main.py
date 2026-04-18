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

    print("\n=== CONTRACT LOADED ===\n")
    print(code[:500])  # preview first 500 chars

if __name__ == "__main__":
    main()