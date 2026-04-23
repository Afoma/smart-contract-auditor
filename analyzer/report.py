def normalize_issue(issue):
    return {
        "name": issue.get("name", "Unknown"),
        "severity": issue.get("severity", "low").lower(),
        "explanation": issue.get("explanation", ""),
        "location": issue.get("location", "Not specified"),
        "fix": issue.get("fix", ""),
        "exploit": issue.get("exploit", {
            "possible": False,
            "preconditions": [],
            "steps": [],
            "impact": "",
            "notes": ""
        })
    }


def deduplicate_issues(issues):
    seen = set()
    unique = []

    for issue in issues:
        key = (issue["name"], issue["location"])
        if key not in seen:
            seen.add(key)
            unique.append(issue)

    return unique


def validate_issues(issues):
    validated = []

    for issue in issues:
        exploit = issue.get("exploit", {})

        possible = exploit.get("possible", False)
        steps = exploit.get("steps", [])
        preconditions = exploit.get("preconditions", [])

        # If exploit not possible, downgrade heavily
        if not possible:
            issue["severity"] = "low"

        # If no real steps, downgrade
        elif len(steps) < 2:
            issue["severity"] = "medium"

        # If no preconditions, weak reasoning
        elif not preconditions:
            issue["severity"] = "medium"

        validated.append(issue)

    return validated
def calculate_summary(issues):
    summary = {"high": 0, "medium": 0, "low": 0}

    for issue in issues:
        sev = issue["severity"]
        if sev in summary:
            summary[sev] += 1

    summary["total_issues"] = len(issues)
    return summary


def generate_report(heuristic_results, llm_results):
    combined = []

    for issue in heuristic_results:
        combined.append(normalize_issue(issue))

    if isinstance(llm_results, list):
        for issue in llm_results:
            combined.append(normalize_issue(issue))

    combined = deduplicate_issues(combined)

    # apply validation step here
    combined = validate_issues(combined)

    summary = calculate_summary(combined)

    return {
        "summary": summary,
        "issues": combined
    }