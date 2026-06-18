from pathlib import Path
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_METRICS = PROJECT_ROOT / "data" / "raw_metrics"
PROCESSED = PROJECT_ROOT / "data" / "processed"
COLUMN_REPORT = PROCESSED / "ck_column_report.csv"
MAPPING_FILE = PROCESSED / "qmood_metric_mapping.csv"

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

USEFUL_COLUMNS = [
    "cbo",
    "wmc",
    "rfc",
    "lcom",
    "dit",
    "noc",
    "loc",
    "totalMethodsQty",
    "totalFieldsQty",
    "publicMethodsQty",
    "privateMethodsQty",
    "protectedMethodsQty",
    "publicFieldsQty",
    "privateFieldsQty",
    "protectedFieldsQty",
]

MAPPING_ROWS = [
    ["Design Size", "class_count", "Count classes in the CK class CSV files."],
    ["Coupling", "avg_cbo", "Average `cbo`."],
    ["Complexity", "avg_wmc", "Average `wmc`."],
    ["Messaging", "avg_rfc", "Average `rfc`."],
    ["Cohesion", "inverse of avg_lcom", "Use the inverse direction of average `lcom`."],
    ["Inheritance", "avg_dit + avg_noc", "Use average `dit` and average `noc`."],
    ["Abstraction", "avg_dit", "Use average `dit`."],
    ["Polymorphism", "avg_noc + avg_methods", "Use average `noc` and average method count."],
    ["Encapsulation", "private method/field ratio if available", "Use private/public method and field columns."],
    ["Composition", "field-related structure if available", "Use field count columns as a simple approximation."],
]

NOTE = "This project uses a QMOOD-inspired approximation because CK Tool does not directly provide every original QMOOD design property."


def read_columns(csv_file):
    with csv_file.open(newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        return next(reader)


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)

    report_rows = []
    all_columns = set()

    for version in VERSIONS:
        for file_name in CLASS_FILES:
            csv_file = RAW_METRICS / version / file_name
            if not csv_file.exists():
                report_rows.append([version, file_name, "missing", "", "", ""])
                continue

            columns = read_columns(csv_file)
            all_columns.update(columns)
            useful_found = [column for column in USEFUL_COLUMNS if column in columns]
            useful_missing = [column for column in USEFUL_COLUMNS if column not in columns]

            report_rows.append([
                version,
                file_name,
                "found",
                "|".join(columns),
                "|".join(useful_found),
                "|".join(useful_missing),
            ])

    with COLUMN_REPORT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["version", "file", "file_status", "detected_columns", "useful_columns_found", "useful_columns_missing"])
        writer.writerows(report_rows)

    with MAPPING_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["note", NOTE])
        writer.writerow([])
        writer.writerow(["qmood_related_property", "planned_metric", "source"])
        writer.writerows(MAPPING_ROWS)

    found = [column for column in USEFUL_COLUMNS if column in all_columns]
    missing = [column for column in USEFUL_COLUMNS if column not in all_columns]

    print("Useful CK columns found:")
    for column in found:
        print(f"- {column}")

    print("\nExpected useful columns missing:")
    if missing:
        for column in missing:
            print(f"- {column}")
    else:
        print("- none")

    print(f"\nColumn report saved in: {COLUMN_REPORT}")
    print(f"QMOOD mapping saved in: {MAPPING_FILE}")


if __name__ == "__main__":
    main()
