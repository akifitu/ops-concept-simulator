PYTHON ?= python3

.PHONY: test simulate

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

simulate:
	PYTHONPATH=src $(PYTHON) -m ops_concept_simulator.cli simulate --data-file data/scenarios.json --export-dir reports
