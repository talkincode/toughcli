build:
	python setup.py bdist_wheel

register:
	python setup.py register

upload:
	python setup.py bdist_wheel upload

clean:
	@rm -rf .Python MANIFEST build dist venv* *.egg-info *.egg
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

venv:
	virtualenv venv --no-site-packages

install:
	python setup.py install

.PHONY: build register upload clean venv install