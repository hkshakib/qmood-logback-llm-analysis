from pathlib import Path
import subprocess
import sys

from checkout_logback_version import checkout_version


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGBACK_REPO = PROJECT_ROOT / "versions" / "logback"
CK_JAR = PROJECT_ROOT / "tools" / "ck.jar"
RAW_METRICS = PROJECT_ROOT / "data" / "raw_metrics"

SOURCE_FOLDERS = {
    "logback-core": LOGBACK_REPO / "logback-core" / "src" / "main" / "java",
    "logback-classic": LOGBACK_REPO / "logback-classic" / "src" / "main" / "java",
}


def run_ck(source_folder, output_folder):
    output_folder.mkdir(parents=True, exist_ok=True)

    if any(output_folder.iterdir()):
        raise RuntimeError(f"Output folder is not empty: {output_folder}")

    command = [
        "java",
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
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_ck_single_version.py v_1.5.25")
        sys.exit(1)

    tag = sys.argv[1]
    tools_folder = PROJECT_ROOT / "tools"
    tools_folder.mkdir(exist_ok=True)

    if not CK_JAR.exists():
        print("CK Tool was not found.")
        print("Please put the CK jar here: tools/ck.jar")
        sys.exit(1)

    try:
        checkout_version(tag)

        version_output = RAW_METRICS / tag
        for module_name, source_folder in SOURCE_FOLDERS.items():
            if not source_folder.exists():
                raise RuntimeError(f"Source folder was not found: {source_folder}")

            module_output = version_output / module_name
            print(f"Running CK for {module_name}")
            run_ck(source_folder, module_output)

        print(f"Raw CK output saved in: {version_output}")
    except subprocess.CalledProcessError as error:
        print("CK metric extraction did not finish successfully.")
        print(f"Command failed with exit code {error.returncode}.")
        sys.exit(1)
    except RuntimeError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
