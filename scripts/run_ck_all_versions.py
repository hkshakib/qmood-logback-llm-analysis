from pathlib import Path
import csv
import shutil
import subprocess

from checkout_logback_version import checkout_version


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGBACK_REPO = PROJECT_ROOT / "versions" / "logback"
CK_JAR = PROJECT_ROOT / "tools" / "ck.jar"
RAW_METRICS = PROJECT_ROOT / "data" / "raw_metrics"
LOG_FILE = RAW_METRICS / "extraction_log.csv"

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

MODULES = {
    "logback-core": LOGBACK_REPO / "logback-core" / "src" / "main" / "java",
    "logback-classic": LOGBACK_REPO / "logback-classic" / "src" / "main" / "java",
}

EXPECTED_SUFFIXES = ["class.csv", "field.csv", "method.csv", "variable.csv"]


def find_java():
    java = shutil.which("java")
    if java:
        return java

    possible_paths = [
        Path("C:/Program Files/Eclipse Adoptium/jre-17.0.19.10-hotspot/bin/java.exe"),
        Path("C:/Program Files/Java"),
        Path("C:/Program Files/Eclipse Adoptium"),
    ]

    for path in possible_paths:
        if path.is_file():
            return str(path)
        if path.is_dir():
            matches = list(path.rglob("java.exe"))
            if matches:
                return str(matches[0])

    return None


def expected_files(version_folder):
    files = []
    for module_name in MODULES:
        for suffix in EXPECTED_SUFFIXES:
            files.append(version_folder / f"{module_name}{suffix}")
    return files


def output_is_complete(version_folder):
    return all(path.exists() and path.stat().st_size > 0 for path in expected_files(version_folder))


def write_version_readme(version, version_folder):
    text = f"""# Raw CK Metrics for {version}

Version analyzed: `{version}`

Folders analyzed:
- `versions/logback/logback-core/src/main/java`
- `versions/logback/logback-classic/src/main/java`

Folders excluded:
- tests
- examples
- target folders
- generated files
- documentation
- logback-access

Tool used: CK Tool

No QMOOD calculation was done yet.
"""
    (version_folder / "README.md").write_text(text, encoding="utf-8")


def run_ck(java_cmd, source_folder, output_folder):
    output_folder.mkdir(parents=True, exist_ok=True)
    command = [
        java_cmd,
        "-jar",
        str(CK_JAR),
        str(source_folder),
        "false",
        "0",
        "true",
        str(output_folder),
    ]
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def main():
    if not CK_JAR.exists():
        print("CK Tool was not found. Please put it at tools/ck.jar.")
        return

    java_cmd = find_java()
    if not java_cmd:
        print("Java was not found. Please install Java or add it to PATH.")
        return

    rows = []

    for version in VERSIONS:
        version_folder = RAW_METRICS / version
        output_folder = version_folder.relative_to(PROJECT_ROOT).as_posix()

        if output_is_complete(version_folder):
            write_version_readme(version, version_folder)
            rows.append([version, "success", "success", "success", output_folder, "already completed"])
            print(f"{version}: already completed")
            continue

        checkout_status = "failed"
        ck_core_status = "not started"
        ck_classic_status = "not started"
        notes = "ok"

        try:
            checkout_version(version)
            checkout_status = "success"

            run_ck(java_cmd, MODULES["logback-core"], version_folder / "logback-core")
            ck_core_status = "success"

            run_ck(java_cmd, MODULES["logback-classic"], version_folder / "logback-classic")
            ck_classic_status = "success"

            if output_is_complete(version_folder):
                write_version_readme(version, version_folder)
            else:
                notes = "CK ran, but expected CSV files are missing"
        except Exception as error:
            notes = str(error).replace("\n", " ")
            print(f"{version}: failed - {notes}")

        rows.append([version, checkout_status, ck_core_status, ck_classic_status, output_folder, notes])

    with LOG_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["version", "checkout_status", "ck_core_status", "ck_classic_status", "output_folder", "notes"])
        writer.writerows(rows)

    print(f"Extraction log saved in: {LOG_FILE}")


if __name__ == "__main__":
    main()
