# Ops Concept Simulator

`Ops Concept Simulator` is a systems engineering repository for concept-of-operations analysis. It stores disaster-response mission threads as structured timelines, validates the scenario logic, and exports reviewer-facing operational summaries.

This repo is useful when you want your portfolio to show not only engineering artifacts, but also how the system is expected to operate in time.

## What This Repo Demonstrates

- concept-of-operations thinking
- scenario decomposition and timing analysis
- subsystem participation across mission phases
- automation, tests, and reproducible exports

## Repository Map

```text
.
|-- data/                         # Scenario inputs
|-- docs/                         # Build plan and ConOps notes
|-- reports/                      # Generated summaries and dashboards
|-- src/ops_concept_simulator/    # Simulation, validation, export, and CLI logic
|-- tests/                        # Regression tests
|-- .github/workflows/            # CI pipeline
|-- Makefile                      # Common commands
`-- README.md
```

## Quick Start

```bash
make test
make simulate
```

Or run the CLI directly:

```bash
PYTHONPATH=src python3 -m ops_concept_simulator.cli simulate --data-file data/scenarios.json --export-dir reports
```

## Generated Outputs

- `reports/conops-summary.md`
- `reports/scenario-catalog.csv`
- `reports/subsystem-utilization.csv`
- `reports/conops-dashboard.html`

## Documentation

- [docs/README.md](docs/README.md)
- [docs/project_plan.md](docs/project_plan.md)
- [docs/conops_notes.md](docs/conops_notes.md)

## Why This Matters For A Recruiter

A systems engineer is expected to reason about time, coordination, mission threads, and operational handoffs. This repo makes that visible through structured scenario logic instead of vague prose.
