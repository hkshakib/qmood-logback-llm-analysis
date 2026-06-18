from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"
GRAPHS = PROJECT_ROOT / "graphs"

COMBINED_METRICS = PROCESSED / "logback_combined_metrics.csv"
QMOOD_SCORES = PROCESSED / "logback_qmood_scores.csv"


def save_line_chart(data, columns, title, ylabel, output_file):
    plt.figure(figsize=(10, 5))
    for column in columns:
        plt.plot(data["version"], data[column], marker="o", linewidth=2, label=column)

    plt.title(title)
    plt.xlabel("Logback version")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    if len(columns) > 1:
        plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()


def save_bar_chart(data, column, title, ylabel, output_file):
    plt.figure(figsize=(10, 5))
    plt.bar(data["version"], data[column], color="#4f81bd")
    plt.title(title)
    plt.xlabel("Logback version")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()


def main():
    GRAPHS.mkdir(parents=True, exist_ok=True)

    combined = pd.read_csv(COMBINED_METRICS)
    scores = pd.read_csv(QMOOD_SCORES)

    save_line_chart(
        scores,
        ["overall_quality_score"],
        "Overall QMOOD-Inspired Quality Score by Version",
        "Score",
        GRAPHS / "overall_quality_score_by_version.png",
    )

    save_line_chart(
        scores,
        ["reusability", "flexibility", "understandability", "functionality", "extendibility", "effectiveness"],
        "QMOOD-Inspired Quality Attributes by Version",
        "Score",
        GRAPHS / "qmood_quality_attributes_by_version.png",
    )

    save_line_chart(
        combined,
        ["avg_cbo", "avg_wmc", "avg_lcom"],
        "Metric Trends: CBO, WMC, and LCOM",
        "Average metric value",
        GRAPHS / "metric_trends_cbo_wmc_lcom.png",
    )

    save_bar_chart(
        combined,
        "class_count",
        "Class Count by Version",
        "Class count",
        GRAPHS / "class_count_by_version.png",
    )

    print("Graphs saved in:")
    for graph in sorted(GRAPHS.glob("*.png")):
        print(f"- {graph}")


if __name__ == "__main__":
    main()
