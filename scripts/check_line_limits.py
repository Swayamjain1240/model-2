from pathlib import Path

MAX_LINES = 200
ROOT = Path(__file__).resolve().parents[1]
TARGETS = (ROOT / "app", ROOT / "tests", ROOT / "scripts", ROOT / "migrations")


def find_violations() -> list[tuple[Path, int]]:
    violations = []
    for directory in TARGETS:
        if not directory.exists():
            continue
        for path in directory.rglob("*.py"):
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            if line_count > MAX_LINES:
                violations.append((path.relative_to(ROOT), line_count))
    return violations


if __name__ == "__main__":
    failures = find_violations()
    if failures:
        for path, count in failures:
            print(f"{path}: {count} lines (limit: {MAX_LINES})")
        raise SystemExit(1)
    print(f"Line limit check passed: all Python files are <= {MAX_LINES} lines")
