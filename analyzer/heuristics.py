import re

def detect_reentrancy(code):
    findings = []

    # very simple heuristic: external call + state change pattern risk
    if "call.value" in code or ".call(" in code:
        if "=" in code or "balance" in code:
            findings.append({
                "name": "Potential Reentrancy",
                "severity": "high",
                "explanation": "Detected external call which may allow reentrancy if state changes occur after the call.",
                "fix": "Use checks-effects-interactions pattern or ReentrancyGuard."
            })

    return findings


def detect_unprotected_functions(code):
    findings = []

    # naive check: public functions without modifiers
    functions = re.findall(r"function\s+(\w+)\s*\(.*?\)\s*(public|external)", code)

    for name, visibility in functions:
        # crude heuristic: no onlyOwner mention nearby
        pattern = rf"function\s+{name}.*?(public|external)(?!.*onlyOwner)"
        if re.search(pattern, code, re.DOTALL):
            findings.append({
                "name": "Missing Access Control",
                "severity": "medium",
                "explanation": f"Function `{name}` may be publicly accessible without restriction.",
                "fix": "Add access control modifier like onlyOwner or role-based auth."
            })

    return findings


def run_heuristics(code):
    results = []
    results += detect_reentrancy(code)
    results += detect_unprotected_functions(code)
    return results