.PHONY: create_venv and run tests

create-venv:
	python3 -m venv .venv

install-reqs:
	. .venv/bin/activate && python3 -m pip install -r requirements.txt

run-tests:
	. .venv/bin/activate && python3 -m unittest
