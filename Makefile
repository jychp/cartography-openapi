CURRENT_VERSION := $(shell git ls-remote --tags --sort=committerdate|sort|head -1|cut -d'/' -f3)
NEXT_PATCH_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. -v OFS=. '{ $$3+=1; print $$1, $$2, $$3 }')
NEXT_MINOR_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. -v OFS=. '{ $$2+=1; print $$1, $$2, 0 }')
NEXT_MAJOR_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. -v OFS=. '{ $$1+=1; print $$1, 0, 0 }')

check-%:
	@hash $(*) > /dev/null 2>&1 || (echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

test: test_lint

test_lint: test_lint_python

test_lint_python: check-uv
	uv run pre-commit run --all-files --show-diff-on-failure

release-patch:
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "Next version: $(NEXT_PATCH_VERSION)""
	git checkout main
	git pull
	git tag $(NEXT_PATCH_VERSION)
	git push origin $(NEXT_PATCH_VERSION)

release-minor:
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "Next version: $(NEXT_MINOR_VERSION)"
	git checkout main
	git pull
	git tag $(NEXT_MINOR_VERSION)
	git push origin $(NEXT_MINOR_VERSION)

release-major:
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "Next version: $(NEXT_MAJOR_VERSION)"
	git checkout main
	git pull
	git tag $(NEXT_MAJOR_VERSION)
	git push origin $(NEXT_MAJOR_VERSION)
