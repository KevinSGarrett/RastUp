PY_DIRS = orchestrator ProjectBlueprint/scripts/concordance

.PHONY: ci ci-setup lint type security test

ci: ci-setup lint type security test
	@echo "CI completed."

ci-setup:
	# Prefer python3 if available; fall back to python
	(command -v python3 >/dev/null 2>&1 && python3 -m ensurepip --upgrade) || true
	(command -v python  >/dev/null 2>&1 && python  -m ensurepip --upgrade) || true
	(command -v python3 >/dev/null 2>&1 && python3 -m pip install --upgrade pip) \
		|| (command -v python >/dev/null 2>&1 && python -m pip install --upgrade pip) \
		|| true
	(command -v python3 >/dev/null 2>&1 && python3 -m pip install -r tools/requirements-ci.txt) \
		|| (command -v python >/dev/null 2>&1 && python -m pip install -r tools/requirements-ci.txt)

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
