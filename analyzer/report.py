def normalize_issue(issue):

    return {
        "name": issue.get("name", "Unknown"),
        "severity": issue.get("severity", "low").lower(),
        "explanation": issue.get("explanation", ""),
        "location": issue.get("location", "Not specified"),
        "fix": issue.get("fix", ""),
        "source": issue.get("source", "unknown"),
        "exploit": issue.get(
            "exploit",
            {
                "possible": False,
                "preconditions": [],
                "steps": [],
                "impact": "",
                "notes": ""
            }
        )
    }


# --------------------------------------------------
# Deduplicate findings
# --------------------------------------------------

def deduplicate_issues(issues):

    seen = set()
    unique = []

    for issue in issues:

        key = (
            issue["name"].lower(),
            issue["location"].lower()
        )

        if key not in seen:

            seen.add(key)
            unique.append(issue)

    return unique


# --------------------------------------------------
# Validate issue quality
# --------------------------------------------------

def validate_issue(issue):

    exploit = issue.get("exploit", {})

    possible = exploit.get("possible", False)
    steps = exploit.get("steps", [])
    preconditions = exploit.get("preconditions", [])

    severity = issue["severity"]

    severity_order = {
        "low": 1,
        "medium": 2,
        "high": 3
    }

    # Only downgrade weak LLM findings.
    # Never aggressively downgrade everything.

    if issue.get("source") == "llm":

        if possible:

            if len(steps) < 2:

                if severity == "high":
                    severity = "medium"

            if len(preconditions) == 0:

                if severity == "high":
                    severity = "medium"

        else:

            if severity == "high":
                severity = "medium"

    issue["severity"] = severity

    return issue


def validate_issues(issues):

    validated = []

    for issue in issues:

        validated.append(
            validate_issue(issue)
        )

    return validated


# --------------------------------------------------
# Calculate summary statistics
# --------------------------------------------------

def calculate_summary(issues):

    summary = {
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for issue in issues:

        severity = issue["severity"]

        if severity in summary:
            summary[severity] += 1

    summary["total_issues"] = len(issues)

    return summary


# --------------------------------------------------
# Merge heuristic + LLM findings
# --------------------------------------------------

def merge_findings(
    heuristic_results,
    llm_results
):

    combined = []

    for issue in heuristic_results:

        issue["source"] = "heuristic"

        combined.append(
            normalize_issue(issue)
        )

    if isinstance(llm_results, list):

        for issue in llm_results:

            # Ignore parser failures
            if "error" in issue:
                continue

            issue["source"] = issue.get(
                "source",
                "llm"
            )

            combined.append(
                normalize_issue(issue)
            )

    return combined


# --------------------------------------------------
# Report Generation
# --------------------------------------------------

def generate_report(
    heuristic_results,
    llm_results
):

    combined = merge_findings(
        heuristic_results,
        llm_results
    )

    combined = deduplicate_issues(
        combined
    )

    combined = validate_issues(
        combined
    )

    summary = calculate_summary(
        combined
    )

    return {
        "summary": summary,
        "issues": combined
    }