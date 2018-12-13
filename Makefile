.PHONY: test
test:
	pipenv run pytest


.PHONY: release
release:
	python setup.py sdist --format=zip,bztar,gztar register upload
	python setup.py bdist_wheel register upload


.PHONY: flake8
flake8:
	pipenv run flake8 .

.PHONY: isort
isort:
	isort --check-only --diff --recursive --skip .tox


.PHONY: clean
clean:
	rm -rf *.egg-info *.egg
	rm -rf htmlcov
	rm -f .coverage
	find . -name "*.pyc" -exec rm -rf {} \;
