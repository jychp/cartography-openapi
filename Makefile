CURRENT_VERSION := $(shell sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml)
NEXT_PATCH_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. -v OFS=. '{ $$3+=1; print $$1, $$2, $$3 }')
NEXT_MINOR_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. -v OFS=. '{ $$2+=1; print $$1, $$2, 0 }')
NEXT_MAJOR_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. -v OFS=. '{ $$1+=1; print $$1, 0, 0 }')

check-%:
	@hash $(*) > /dev/null 2>&1 || (echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

test: test_lint

test_lint: test_lint_python

test_lint_python: check-poetry
	poetry run pre-commit run --all-files --show-diff-on-failure

release-patch:
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "Next version: $(NEXT_PATCH_VERSION)"
	@sed -i "s/^version = \".*\"/version = \"$(NEXT_PATCH_VERSION)\"/" pyproject.toml
	git checkout main
	git tag v$(NEXT_PATCH_VERSION)
	git push origin v$(NEXT_PATCH_VERSION)

release-minor:
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "Next version: $(NEXT_MINOR_VERSION)"
	@sed -i "s/^version = \".*\"/version = \"$(NEXT_MINOR_VERSION)\"/" pyproject.toml
	git checkout main
	git tag v$(NEXT_MINOR_VERSION)
	git push origin v$(NEXT_MINOR_VERSION)

release-major:
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "Next version: $(NEXT_MAJOR_VERSION)"
	@sed -i "s/^version = \".*\"/version = \"$(NEXT_MAJOR_VERSION)\"/" pyproject.toml
	git checkout main
	git tag v$(NEXT_MAJOR_VERSION)
	git push origin v$(NEXT_MAJOR_VERSION)
