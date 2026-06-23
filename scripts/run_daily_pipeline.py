from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"


PIPELINE_STEPS = [
    {
        "name": "data_loader",
        "path": PROJECT_ROOT / "scripts" / "data_loader.py",
    },
    {
        "name": "download_fred_data",
        "path": PROJECT_ROOT / "scripts" / "download_fred_data.py",
    },
    {
        "name": "load_all_data",
        "path": PROJECT_ROOT / "scripts" / "load_all_data.py",
    },
    {
        "name": "run_macro_snapshot",
        "path": PROJECT_ROOT / "scripts" / "run_macro_snapshot.py",
    },
    {
        "name": "export_allocation_snapshot",
        "path": PROJECT_ROOT / "dashboard_export" / "export_allocation_snapshot.py",
    },
]


def is_weekday_trade_day() -> bool:
    """
    Simple trading-day guard.

    Current version:
    - Monday to Friday: run
    - Saturday / Sunday: skip

    Later we can upgrade this to a real NYSE calendar check.
    """
    today = datetime.now().date()
    return today.weekday() < 5


def write_log(log_file: Path, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    with log_file.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_step(step: dict, log_file: Path) -> None:
    name = step["name"]
    script_path = step["path"]

    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    command = [sys.executable, str(script_path)]

    write_log(log_file, f"START step: {name}")
    write_log(log_file, f"COMMAND: {' '.join(command)}")

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.stdout:
        write_log(log_file, f"STDOUT for {name}:\n{result.stdout}")

    if result.stderr:
        write_log(log_file, f"STDERR for {name}:\n{result.stderr}")

    if result.returncode != 0:
        write_log(log_file, f"FAILED step: {name}, returncode={result.returncode}")
        raise RuntimeError(f"Pipeline failed at step: {name}")

    write_log(log_file, f"FINISH step: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run even if today is weekend or trading-day guard says skip.",
    )
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"daily_pipeline_{today_str}.log"

    write_log(log_file, "Daily pipeline started.")
    write_log(log_file, f"Project root: {PROJECT_ROOT}")
    write_log(log_file, f"Python executable: {sys.executable}")

    if not args.force and not is_weekday_trade_day():
        write_log(log_file, "Today is not a weekday trading day. Pipeline skipped.")
        return

    for step in PIPELINE_STEPS:
        run_step(step, log_file)

    write_log(log_file, "Daily pipeline completed successfully.")


if __name__ == "__main__":
    main()