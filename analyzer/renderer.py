def format_report(report):
    summary = report["summary"]
    issues = report["issues"]

    lines = []

    lines.append("=" * 50)
    lines.append("SMART CONTRACT SECURITY AUDIT REPORT")
    lines.append("=" * 50)
    lines.append("")

    lines.append("SUMMARY")
    lines.append(f"- High: {summary.get('high', 0)}")
    lines.append(f"- Medium: {summary.get('medium', 0)}")
    lines.append(f"- Low: {summary.get('low', 0)}")
    lines.append(f"- Total: {summary.get('total_issues', 0)}")
    lines.append("")

    if not issues:
        lines.append("No vulnerabilities detected.")
        return "\n".join(lines)

    for i, issue in enumerate(issues, 1):
        lines.append(f"ISSUE {i}: {issue['name']} ({issue['severity'].upper()})")
        lines.append(f"Location: {issue.get('location', 'N/A')}")
        lines.append("")
        lines.append("Explanation:")
        lines.append(issue.get("explanation", ""))
        lines.append("")
        lines.append("Fix:")
        lines.append(issue.get("fix", ""))
        lines.append("")

        # ✅ FIX: exploit block INSIDE the loop
        exploit = issue.get("exploit", {})

        if exploit.get("possible"):
            lines.append("Exploit Analysis:")

            if exploit.get("preconditions"):
                lines.append("Preconditions:")
                for p in exploit["preconditions"]:
                    lines.append(f"- {p}")

            if exploit.get("steps"):
                lines.append("Attack Steps:")
                for step in exploit["steps"]:
                    lines.append(f"- {step}")

            if exploit.get("impact"):
                lines.append(f"Impact: {exploit['impact']}")

            if exploit.get("notes"):
                lines.append(f"Notes: {exploit['notes']}")

            lines.append("")

        lines.append("-" * 50)

    return "\n".join(lines)