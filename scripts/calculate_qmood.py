from pathlib import Path
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_METRICS = PROJECT_ROOT / "data" / "raw_metrics"
PROCESSED = PROJECT_ROOT / "data" / "processed"
COMBINED_METRICS = PROCESSED / "logback_combined_metrics.csv"
QMOOD_SCORES = PROCESSED / "logback_qmood_scores.csv"

VERSIONS = [
    "v_1.5.25",
    "v_1.5.26",
    "v_1.5.27",
    "v_1.5.28",
    "v_1.5.29",
    "v_1.5.30",
    "v_1.5.31",
    "v_1.5.32",
    "v_1.5.33",
    "v_1.5.34",
]

CLASS_FILES = [
    "logback-coreclass.csv",
    "logback-classicclass.csv",
]

REQUIRED_COLUMNS = [
    "cbo",
    "wmc",
    "rfc",
    "lcom",
    "dit",
    "noc",
    "loc",
    "totalMethodsQty",
    "totalFieldsQty",
]


def read_rows(csv_file):
    with csv_file.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def as_float(row, column):
    value = row.get(column, "")
    if value == "":
        return 0.0
    return float(value)


def average(rows, column):
    if not rows:
        return 0.0
    return sum(as_float(row, column) for row in rows) / len(rows)


def total(rows, column):
    return sum(as_float(row, column) for row in rows)


def round_value(value):
    return round(value, 6)


def normalize(value, minimum, maximum):
    if maximum == minimum:
        return 1.0
    return (value - minimum) / (maximum - minimum)


def average_values(*values):
    return sum(values) / len(values)


def load_version_rows(version):
    rows = []
    for file_name in CLASS_FILES:
        csv_file = RAW_METRICS / version / file_name
        if not csv_file.exists():
            raise FileNotFoundError(f"Missing input file: {csv_file}")

        file_rows = read_rows(csv_file)
        if file_rows:
            missing = [column for column in REQUIRED_COLUMNS if column not in file_rows[0]]
            if missing:
                raise ValueError(f"Missing columns in {csv_file}: {', '.join(missing)}")
        rows.extend(file_rows)
    return rows


def calculate_combined_metrics():
    combined = []
    for version in VERSIONS:
        rows = load_version_rows(version)
        combined.append({
            "version": version,
            "class_count": len(rows),
            "avg_cbo": round_value(average(rows, "cbo")),
            "avg_wmc": round_value(average(rows, "wmc")),
            "avg_rfc": round_value(average(rows, "rfc")),
            "avg_lcom": round_value(average(rows, "lcom")),
            "avg_dit": round_value(average(rows, "dit")),
            "avg_noc": round_value(average(rows, "noc")),
            "avg_loc": round_value(average(rows, "loc")),
            "avg_methods": round_value(average(rows, "totalMethodsQty")),
            "avg_fields": round_value(average(rows, "totalFieldsQty")),
            "total_loc": int(total(rows, "loc")),
            "total_methods": int(total(rows, "totalMethodsQty")),
            "total_fields": int(total(rows, "totalFieldsQty")),
        })
    return combined


def metric_range(rows, column):
    values = [row[column] for row in rows]
    return min(values), max(values)


def calculate_scores(combined):
    ranges = {
        column: metric_range(combined, column)
        for column in [
            "class_count",
            "avg_cbo",
            "avg_wmc",
            "avg_rfc",
            "avg_lcom",
            "avg_dit",
            "avg_noc",
            "avg_methods",
            "avg_fields",
        ]
    }

    scores = []
    for row in combined:
        design_size_score = normalize(row["class_count"], *ranges["class_count"])
        inverse_coupling_score = 1 - normalize(row["avg_cbo"], *ranges["avg_cbo"])
        inverse_complexity_score = 1 - normalize(row["avg_wmc"], *ranges["avg_wmc"])
        messaging_score = normalize(row["avg_rfc"], *ranges["avg_rfc"])
        cohesion_score = 1 - normalize(row["avg_lcom"], *ranges["avg_lcom"])
        abstraction_score = normalize(row["avg_dit"], *ranges["avg_dit"])
        inheritance_score = average_values(
            normalize(row["avg_dit"], *ranges["avg_dit"]),
            normalize(row["avg_noc"], *ranges["avg_noc"]),
        )
        polymorphism_score = average_values(
            normalize(row["avg_noc"], *ranges["avg_noc"]),
            normalize(row["avg_methods"], *ranges["avg_methods"]),
        )

        reusability = average_values(cohesion_score, messaging_score, design_size_score, inverse_coupling_score)
        flexibility = average_values(inverse_coupling_score, abstraction_score, polymorphism_score, inverse_complexity_score)
        understandability = average_values(inverse_complexity_score, inverse_coupling_score, cohesion_score)
        functionality = average_values(messaging_score, design_size_score, polymorphism_score)
        extendibility = average_values(abstraction_score, inheritance_score, inverse_coupling_score, inverse_complexity_score)
        effectiveness = average_values(cohesion_score, messaging_score, inverse_complexity_score)
        overall_quality_score = average_values(
            reusability,
            flexibility,
            understandability,
            functionality,
            extendibility,
            effectiveness,
        )

        scores.append({
            "version": row["version"],
            "reusability": round_value(reusability),
            "flexibility": round_value(flexibility),
            "understandability": round_value(understandability),
            "functionality": round_value(functionality),
            "extendibility": round_value(extendibility),
            "effectiveness": round_value(effectiveness),
            "overall_quality_score": round_value(overall_quality_score),
        })
    return scores


def write_csv(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)

    combined = calculate_combined_metrics()
    scores = calculate_scores(combined)

    combined_columns = [
        "version",
        "class_count",
        "avg_cbo",
        "avg_wmc",
        "avg_rfc",
        "avg_lcom",
        "avg_dit",
        "avg_noc",
        "avg_loc",
        "avg_methods",
        "avg_fields",
        "total_loc",
        "total_methods",
        "total_fields",
    ]
    score_columns = [
        "version",
        "reusability",
        "flexibility",
        "understandability",
        "functionality",
        "extendibility",
        "effectiveness",
        "overall_quality_score",
    ]

    write_csv(COMBINED_METRICS, combined, combined_columns)
    write_csv(QMOOD_SCORES, scores, score_columns)

    print(f"Combined metrics saved in: {COMBINED_METRICS}")
    print(f"QMOOD-inspired scores saved in: {QMOOD_SCORES}")
    print(f"Versions processed: {len(combined)}")


if __name__ == "__main__":
    main()
