"""Scenario validation and rollup logic."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


REQUIRED_SCENARIO_FIELDS = {"id", "title", "objective", "phases"}


@dataclass
class SimulationResult:
    errors: List[str]
    warnings: List[str]
    summary: Dict[str, Any]
    scenario_rows: List[Dict[str, str]]
    utilization_rows: List[Dict[str, str]]


def analyze_scenarios(scenarios: Sequence[Mapping[str, Any]]) -> SimulationResult:
    """Validate scenario structure and compute rollups."""
    errors: List[str] = []
    warnings: List[str] = []
    _check_duplicate_ids(scenarios, errors)

    scenario_rows: List[Dict[str, str]] = []
    subsystem_rollup: Dict[str, Dict[str, float]] = defaultdict(lambda: {"hours": 0.0, "scenarios": 0.0})

    for scenario in scenarios:
        if not _validate_scenario(scenario, errors, warnings):
            continue
        total_hours = 0.0
        systems_seen = set()
        for phase in scenario["phases"]:
            total_hours += phase["duration_hours"]
            for system in phase["active_systems"]:
                subsystem_rollup[system]["hours"] += phase["duration_hours"]
                systems_seen.add(system)
        for system in systems_seen:
            subsystem_rollup[system]["scenarios"] += 1
        handoff_count = max(len(scenario["phases"]) - 1, 0)
        scenario_rows.append(
            {
                "id": scenario["id"],
                "title": scenario["title"],
                "objective": scenario["objective"],
                "phase_count": str(len(scenario["phases"])),
                "handoff_count": str(handoff_count),
                "duration_hours": f"{total_hours:.2f}",
                "active_system_count": str(len(systems_seen)),
            }
        )
        if total_hours > 5.5:
            warnings.append(f"{scenario['id']}: scenario duration exceeds 5.5 hours ({total_hours:.2f}).")

    utilization_rows = [
        {
            "system": system,
            "hours_active": f"{rollup['hours']:.2f}",
            "scenario_count": str(int(rollup["scenarios"])),
        }
        for system, rollup in sorted(subsystem_rollup.items())
    ]

    durations = [float(row["duration_hours"]) for row in scenario_rows]
    summary = {
        "scenario_count": len(scenario_rows),
        "total_hours": f"{sum(durations):.2f}",
        "longest_scenario_hours": f"{max(durations) if durations else 0:.2f}",
        "subsystem_count": len(utilization_rows),
        "handoff_count": sum(int(row["handoff_count"]) for row in scenario_rows),
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    return SimulationResult(errors, warnings, summary, scenario_rows, utilization_rows)


def _check_duplicate_ids(scenarios: Sequence[Mapping[str, Any]], errors: List[str]) -> None:
    seen = set()
    for scenario in scenarios:
        scenario_id = scenario.get("id")
        if scenario_id in seen:
            errors.append(f"duplicate scenario id '{scenario_id}' detected.")
        seen.add(scenario_id)


def _validate_scenario(scenario: Mapping[str, Any], errors: List[str], warnings: List[str]) -> bool:
    scenario_id = str(scenario.get("id", "<missing-id>"))
    missing = sorted(field for field in REQUIRED_SCENARIO_FIELDS if not scenario.get(field))
    if missing:
        errors.append(f"{scenario_id}: missing required fields: {', '.join(missing)}.")
        return False
    if not isinstance(scenario["phases"], list) or not scenario["phases"]:
        errors.append(f"{scenario_id}: phases must contain at least one entry.")
        return False
    for index, phase in enumerate(scenario["phases"], start=1):
        if not phase.get("name"):
            errors.append(f"{scenario_id}: phase {index} is missing a name.")
        duration = phase.get("duration_hours")
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"{scenario_id}: phase {index} duration_hours must be greater than zero.")
        if not isinstance(phase.get("active_systems"), list) or not phase["active_systems"]:
            errors.append(f"{scenario_id}: phase {index} must include active_systems.")
        if len(set(phase.get("active_systems", []))) != len(phase.get("active_systems", [])):
            warnings.append(f"{scenario_id}: phase {index} repeats the same active system.")
    return True
