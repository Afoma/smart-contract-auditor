import re


def make_finding(
    name,
    severity,
    explanation,
    location,
    fix
):
    return {
        "name": name,
        "severity": severity,
        "explanation": explanation,
        "location": location,
        "fix": fix
    }


# --------------------------------------------------
# Reentrancy
# --------------------------------------------------

def detect_reentrancy(code):
    findings = []

    patterns = [
        r"\.call\s*\{",
        r"\.call\s*\(",
        r"\.send\s*\(",
        r"\.transfer\s*\("
    ]

    for pattern in patterns:
        if re.search(pattern, code):
            findings.append(
                make_finding(
                    "Potential Reentrancy",
                    "high",
                    "External value transfer detected. Review ordering of state updates and external calls.",
                    "External call",
                    "Apply Checks-Effects-Interactions or ReentrancyGuard."
                )
            )
            break

    return findings


# --------------------------------------------------
# Missing Access Control
# --------------------------------------------------

def detect_unprotected_functions(code):
    findings = []

    function_pattern = re.finditer(
        r"function\s+(\w+)\s*\([^)]*\)\s*([^{;]*)",
        code,
        re.MULTILINE
    )

    sensitive_keywords = [
        "withdraw",
        "mint",
        "burn",
        "pause",
        "unpause",
        "upgrade",
        "set",
        "transferownership",
        "emergency"
    ]

    for match in function_pattern:

        name = match.group(1)
        declaration = match.group(2).lower()

        if "internal" in declaration or "private" in declaration:
            continue

        sensitive = any(
            keyword in name.lower()
            for keyword in sensitive_keywords
        )

        has_auth = (
            "onlyowner" in declaration or
            "role" in declaration or
            "auth" in declaration
        )

        if sensitive and not has_auth:

            findings.append(
                make_finding(
                    "Missing Access Control",
                    "medium",
                    f"Sensitive function '{name}' appears callable without authorization.",
                    name,
                    "Protect sensitive functions with onlyOwner or role-based access control."
                )
            )

    return findings


# --------------------------------------------------
# tx.origin
# --------------------------------------------------

def detect_tx_origin(code):

    findings = []

    if "tx.origin" in code:

        findings.append(
            make_finding(
                "tx.origin Authentication",
                "high",
                "Authentication logic appears to rely on tx.origin.",
                "tx.origin",
                "Use msg.sender for authorization checks."
            )
        )

    return findings


# --------------------------------------------------
# Delegatecall
# --------------------------------------------------

def detect_delegatecall(code):

    findings = []

    if "delegatecall" in code:

        findings.append(
            make_finding(
                "Delegatecall Usage",
                "high",
                "delegatecall can execute code in the current contract context.",
                "delegatecall",
                "Restrict delegatecall targets and validate implementation contracts."
            )
        )

    return findings


# --------------------------------------------------
# Unchecked Low-Level Call
# --------------------------------------------------

def detect_unchecked_call(code):

    findings = []

    matches = re.finditer(
        r"\.call\s*\{?.*?\}?\(",
        code,
        re.DOTALL
    )

    for _ in matches:

        findings.append(
            make_finding(
                "Unchecked Low-Level Call",
                "medium",
                "Low-level call detected. Verify success return values are checked.",
                "call()",
                "Capture and validate the boolean success value."
            )
        )

        break

    return findings


# --------------------------------------------------
# Timestamp Dependence
# --------------------------------------------------

def detect_timestamp_dependence(code):

    findings = []

    if "block.timestamp" in code:

        findings.append(
            make_finding(
                "Timestamp Dependence",
                "medium",
                "Contract logic depends on block.timestamp.",
                "block.timestamp",
                "Avoid relying on timestamps for critical security decisions."
            )
        )

    return findings


# --------------------------------------------------
# Block Number Dependence
# --------------------------------------------------

def detect_block_number_dependence(code):

    findings = []

    if "block.number" in code:

        findings.append(
            make_finding(
                "Block Number Dependence",
                "low",
                "Contract logic depends on block.number.",
                "block.number",
                "Avoid using block.number for randomness or security-sensitive logic."
            )
        )

    return findings


# --------------------------------------------------
# Selfdestruct
# --------------------------------------------------

def detect_selfdestruct(code):

    findings = []

    if "selfdestruct" in code:

        findings.append(
            make_finding(
                "Selfdestruct Usage",
                "high",
                "Contract contains selfdestruct functionality.",
                "selfdestruct",
                "Restrict destruction logic and carefully review authorization."
            )
        )

    return findings


# --------------------------------------------------
# Weak Randomness
# --------------------------------------------------

def detect_weak_randomness(code):

    findings = []

    weak_sources = [
        "block.timestamp",
        "blockhash",
        "block.number"
    ]

    count = sum(
        source in code
        for source in weak_sources
    )

    if count >= 2:

        findings.append(
            make_finding(
                "Weak Randomness",
                "medium",
                "Randomness appears derived from predictable blockchain properties.",
                "Randomness logic",
                "Use Chainlink VRF or another verifiable randomness source."
            )
        )

    return findings


# --------------------------------------------------
# Inline Assembly
# --------------------------------------------------

def detect_inline_assembly(code):

    findings = []

    if re.search(r"\bassembly\b", code):

        findings.append(
            make_finding(
                "Inline Assembly",
                "medium",
                "Inline assembly detected.",
                "assembly",
                "Review assembly blocks carefully for memory and storage safety."
            )
        )

    return findings


# --------------------------------------------------
# Central Dispatcher
# --------------------------------------------------

def run_heuristics(code):

    results = []

    detectors = [
        detect_reentrancy,
        detect_unprotected_functions,
        detect_tx_origin,
        detect_delegatecall,
        detect_unchecked_call,
        detect_timestamp_dependence,
        detect_block_number_dependence,
        detect_selfdestruct,
        detect_weak_randomness,
        detect_inline_assembly
    ]

    for detector in detectors:

        try:
            results.extend(detector(code))
        except Exception:
            pass

    return results