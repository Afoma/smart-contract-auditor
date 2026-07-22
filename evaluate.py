import os
import json

RESULTS_DIR = "results"
LABEL_FILE = "labels.json"


def load_labels():

    with open(
        LABEL_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def load_report(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def extract_findings(report):

    issues = report.get(
        "issues",
        []
    )

    return set(
        issue["name"]
        for issue in issues
    )


def evaluate():

    labels = load_labels()

    tp = 0
    fp = 0
    fn = 0

    contracts = 0

    for filename in os.listdir(RESULTS_DIR):

        if not filename.endswith(".json"):
            continue

        contracts += 1

        contract_name = filename.replace(
            ".json",
            ""
        )

        report = load_report(
            os.path.join(
                RESULTS_DIR,
                filename
            )
        )

        predicted = extract_findings(
            report
        )

        expected = set(
            labels.get(
                contract_name,
                []
            )
        )

        tp += len(
            predicted & expected
        )

        fp += len(
            predicted - expected
        )

        fn += len(
            expected - predicted
        )

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0
    )

    f1 = (
        2 * precision * recall
        / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    print("=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)

    print(f"Contracts Tested: {contracts}")
    print()

    print(f"True Positives : {tp}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")

    print()

    print(
        f"Precision: "
        f"{precision * 100:.2f}%"
    )

    print(
        f"Recall: "
        f"{recall * 100:.2f}%"
    )

    print(
        f"F1 Score: "
        f"{f1 * 100:.2f}%"
    )

    print("=" * 60)


if __name__ == "__main__":
    evaluate()