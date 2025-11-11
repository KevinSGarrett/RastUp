PY_DIRS = orchestrator ProjectBlueprint/scripts/concordance

.PHONY: ci ci-setup lint type security test

ci: ci-setup lint type security test
	@echo "CI completed."

ci-setup:
	python -m pip install --upgrade pip
	pip install -r tools/requirements-ci.txt

lint:
	ruff check $(PY_DIRS)
	black --check $(PY_DIRS)

type:
	mypy $(PY_DIRS)

security:
	# Bandit returns non-zero for findings; keep it informational locally
	-bandit -q -r orchestrator

test:
	@if [ -d tests ]; then pytest -q; else echo "No tests/ directory"; fi
