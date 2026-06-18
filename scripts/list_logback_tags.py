from pathlib import Path
import re
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGBACK_REPO = PROJECT_ROOT / "versions" / "logback"


def version_key(tag):
    match = re.fullmatch(r"v_1\.5\.(\d+)", tag)
    if not match:
        return None
    return int(match.group(1))


def main():
    if not LOGBACK_REPO.exists():
        print("Logback repository was not found at versions/logback.")
        return

    result = subprocess.run(
        ["git", "tag", "--list"],
        cwd=LOGBACK_REPO,
        text=True,
        capture_output=True,
        check=True,
    )

    tags = result.stdout.splitlines()
    stable_15_tags = [tag for tag in tags if version_key(tag) is not None]
    selected = sorted(stable_15_tags, key=version_key)[-10:]

    print("Stable Logback 1.5.x tags:")
    for tag in sorted(stable_15_tags, key=version_key):
        print(tag)

    print("\nSelected 10 versions for this project:")
    for tag in selected:
        print(tag)


if __name__ == "__main__":
    main()
