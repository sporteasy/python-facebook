all: clean-pyc test

test:
	py.test tests

tox-test:
	tox

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
