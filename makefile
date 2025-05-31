# Configuration
VENV_DIR := .venv
PYTHON := python3
REQUIREMENTS := requirements.txt
TOP_LEVEL_PACKAGES := cryptography google-api-python-client google-auth google-auth-oauthlib pyyaml

.PHONY: all setup activate clean freeze

all: setup

setup:
	@echo "🔧 Creating virtual environment in $(VENV_DIR) if it doesn't exist..."
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	@echo "🚀 Upgrading pip, setuptools, and wheel..."
	. $(VENV_DIR)/bin/activate && \
	pip install --upgrade pip setuptools wheel
ifeq ("$(wildcard $(REQUIREMENTS))","")
	@echo "📦 Installing top-level packages: $(TOP_LEVEL_PACKAGES)"
	. $(VENV_DIR)/bin/activate && \
	pip install $(TOP_LEVEL_PACKAGES)
	@echo "📝 Writing top-level-only requirements.txt"
	@echo "# Top-level dev dependencies" > $(REQUIREMENTS)
	@for pkg in $(TOP_LEVEL_PACKAGES); do echo $$pkg >> $(REQUIREMENTS); done
else
	@echo "📜 Installing from existing $(REQUIREMENTS)..."
	. $(VENV_DIR)/bin/activate && \
	pip install -r $(REQUIREMENTS)
endif
	@echo "✅ Setup complete."
	@echo "Run 'source $(VENV_DIR)/bin/activate' to activate the virtual environment."


activate:
	@echo "Run this to activate the virtual environment:"
	@echo "source $(VENV_DIR)/bin/activate"

freeze:
	@echo "📌 Rewriting $(REQUIREMENTS) with top-level-only packages..."
	@echo "# Top-level dev dependencies" > $(REQUIREMENTS)
	@for pkg in $(TOP_LEVEL_PACKAGES); do echo $$pkg >> $(REQUIREMENTS); done
	@echo "✅ Updated."

clean:
	@echo "🧹 Removing virtual environment..."
	@rm -rf $(VENV_DIR)
	@echo "🧹 Removing all __pycache__ directories..."
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@echo "🧹 Removing .mypy_cache directory..."
	@rm -rf .mypy_cache
	@echo "🧹 Removing log files..."
	@rm -rf *.log
	@echo "🧹 Removing requirements.txt ..."
	@rm -rf requirements.txt
	@echo "✅ Cleaned all caches and virtual environment."

test:
	@echo "Running tests..."
	@. $(VENV_DIR)/bin/activate && \
	pwl main env2yaml
	pwl main yaml2enc
#	@. $(VENV_DIR)/bin/activate && \
	pytest --maxfail=1 --disable-warnings -q
	@echo "✅ Tests completed."

