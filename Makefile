.PHONY: check
check:
	poetry build
	twine check dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: release
release:
	make check
	twine upload dist/*

.PHONY: push
push:
	git push origin master --tags


.PHONY: patch
patch:
	echo "Making a patch release"
	poetry run bump2version patch


.PHONY: minor
minor:
	echo "Making a minor release"
	poetry run bump2version minor


.PHONY: major
major:
	echo "Making a MAJOR release"
	poetry run bump2version major
