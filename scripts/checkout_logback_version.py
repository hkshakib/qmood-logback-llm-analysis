from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGBACK_REPO = PROJECT_ROOT / "versions" / "logback"


def run_git(args):
    return subprocess.run(
        ["git", *args],
        cwd=LOGBACK_REPO,
        text=True,
        capture_output=True,
        check=True,
    )


def checkout_version(tag):
    if not LOGBACK_REPO.exists():
        raise RuntimeError("Logback repository was not found at versions/logback.")

    status = run_git(["status", "--short"]).stdout.strip()
    if status:
        raise RuntimeError("Logback has local changes. Please check them before changing versions.")

    run_git(["checkout", tag])

    current = run_git(["describe", "--tags", "--exact-match"]).stdout.strip()
    print(f"Current Logback version: {current}")
    return current


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/checkout_logback_version.py v_1.5.25")
        sys.exit(1)

    try:
        checkout_version(sys.argv[1])
    except subprocess.CalledProcessError as error:
        print("Could not checkout the requested version.")
        if error.stderr:
            print(error.stderr.strip())
        sys.exit(1)
    except RuntimeError as error:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
