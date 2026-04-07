"""CLI for the ConOps simulator."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .data import load_scenarios
from .export import export_reports
from .simulate import analyze_scenarios


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        prog="ops-concept-simulator",
        description="Validate and export concept-of-operations scenarios.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate_parser = subparsers.add_parser("simulate", help="Analyze scenario timelines and export reports.")
    simulate_parser.add_argument("--data-file", default="data/scenarios.json", help="Path to the scenario JSON file.")
    simulate_parser.add_argument("--export-dir", help="Directory where reports should be written.")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "simulate":
        result = analyze_scenarios(load_scenarios(Path(args.data_file)))
        _print_summary(result)
        if args.export_dir:
            export_reports(result, Path(args.export_dir))
            print(f"Reports exported to: {args.export_dir}")
        return 1 if result.errors else 0

    parser.error("Unknown command.")
    return 2


def _print_summary(result) -> None:
    summary = result.summary
    print("ConOps summary")
    print(f"  Scenarios: {summary['scenario_count']}")
    print(f"  Total hours simulated: {summary['total_hours']}")
    print(f"  Longest scenario hours: {summary['longest_scenario_hours']}")
    print(f"  Unique systems involved: {summary['subsystem_count']}")
    print(f"  Total handoffs: {summary['handoff_count']}")
    print(f"  Errors: {summary['error_count']}")
    print(f"  Warnings: {summary['warning_count']}")
    if result.errors:
        print("Validation errors:")
        for item in result.errors:
            print(f"  - {item}")
    if result.warnings:
        print("Validation warnings:")
        for item in result.warnings:
            print(f"  - {item}")


if __name__ == "__main__":
    raise SystemExit(run())
