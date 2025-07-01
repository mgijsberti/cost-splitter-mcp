# justfile for cost-splitter-mcp project

lint:
	uv run pylint main.py test_main.py test_integration_stdio.py

test:
	sh run_all_tests.sh

ci: lint test 