# Step-By-Step Plan

## Phase 1: Select the mission threads

1. Pick realistic disaster-response scenarios.
2. Define the main phases and decision points.
3. List which subsystems participate in each phase.

## Phase 2: Structure the scenario data

1. Store phases in machine-readable form.
2. Capture duration, active systems, and objectives.
3. Make handoffs explicit between phases.

## Phase 3: Implement the simulator

1. Validate scenario integrity.
2. Calculate total duration and subsystem participation.
3. Export reviewer-facing tables and dashboards.

## Phase 4: Debug and verify

1. Add tests for negative duration and missing systems.
2. Check that totals match hand calculations.
3. Fix formatting or logic gaps.

## Phase 5: Publish professionally

1. Write a portfolio-ready README.
2. Commit generated outputs.
3. Push the repo publicly and keep CI green.

## To-Do

- [x] define the scenario schema
- [x] build an operational dataset
- [x] implement the simulator and exporters
- [x] add regression tests
- [ ] publish the repository
