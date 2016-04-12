build:
	python setup.py bdist_wheel

register:
	python setup.py register

upload:
	python setup.py rpm bdist_wheel upload

clean:
	@rm -rf .Python MANIFEST build dist venv* *.egg-info *.egg
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

venv:
	(\
	test -d venv || virtualenv venv;\
	venv/bin/pip install Click;\
	venv/bin/pip install -e .;\
	)

install:
	python setup.py install

.PHONY: build register upload clean venv install