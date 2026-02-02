# Name of the main execution script
NAME = a_maze_ing.py

# Python interpreter
PYTHON = python3

# Formatting and Type Checking tools
FLAKE8 = flake8
MYPY = mypy

# Default rule
all: run

# Install project dependencies
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install flake8 mypy build setuptools wheel

# Execute the main script
run:
	$(PYTHON) $(NAME) config.txt

# Run the script in debug mode using pdb
debug:
	$(PYTHON) -m pdb $(NAME) config.txt

# Linting as per 42 requirements
# We check the main script and the package folder
lint:
	@$(FLAKE8) .
	@$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

# Build the reusable package (.whl) strictly using pyproject.toml configuration
package: clean
	@echo "📦 Building package using pyproject.toml (Setuptools Direct Mode)..."
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install setuptools wheel
	@$(PYTHON) -c "from setuptools import build_meta; import setuptools; setuptools.setup()" bdist_wheel
	@cp dist/*.whl .
	@echo "✅ Success: Package built from pyproject.toml!"

# Clean temporary files
clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@rm -f *.whl
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "🧹 Directory cleaned."

.PHONY: install run debug lint package clean