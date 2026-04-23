import re

def detect_reentrancy(code):
    findings = []

    # modern and legacy patterns
    if (
        "call.value" in code or
        ".call(" in code or
        "call{" in code or
        "send(" in code or
        "transfer(" in code
    ):
        findings.append({
            "name": "Potential Reentrancy",
            "severity": "high",
            "explanation": "External call detected which may allow reentrancy if state updates occur after the call.",
            "location": "external call (possible reentrancy point)",
            "fix": "Use checks-effects-interactions pattern or ReentrancyGuard."
        })

    return findings

def detect_unprotected_functions(code):
    findings = []

    functions = re.findall(r"function\s+(\w+)\s*\(.*?\)\s*(public|external)", code)

    for name, _ in functions:
        pattern = rf"function\s+{name}.*?(public|external)(?!.*onlyOwner)"
        if re.search(pattern, code, re.DOTALL):
            findings.append({
                "name": "Missing Access Control",
                "severity": "medium",
                "explanation": f"Function `{name}` may be publicly accessible without restriction.",
                "location": name,
                "fix": "Add access control modifier like onlyOwner or role-based auth."
            })

    return findings


def run_heuristics(code):
    results = []
    results += detect_reentrancy(code)
    results += detect_unprotected_functions(code)
    return results