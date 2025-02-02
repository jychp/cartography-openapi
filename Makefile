check-%:
	@hash $(*) > /dev/null 2>&1 || (echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

test: test_lint

test_lint: test_lint_python

test_lint_python: check-poetry
	poetry run pre-commit run --all-files --show-diff-on-failure
