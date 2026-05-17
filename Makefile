PYTHON      = python3
PIP         = pip
MAIN_FILE   = a_maze_ing.py
CONFIG_FILE = config.txt
PACKAGE_DIR = mazegen

install:
	$(PIP) install flake8 mypy build

run:
	$(PYTHON) $(MAIN_FILE) $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb $(MAIN_FILE) $(CONFIG_FILE)

lint:
	flake8 .
	-mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	rm -rf __pycache__
	rm -rf $(PACKAGE_DIR)/__pycache__
	rm -rf build dist *.egg-info
	rm -rf .mypy_cache .pytest_cache

.PHONY: all install run debug lint lint-strict clean