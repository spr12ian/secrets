# Customize these
GOOGLE_SERVICE_ACCOUNT_KEY_FILE ?= service-account.json
GOOGLE_PROJECT_ID ?= your-project-id

# Configuration
VENV_DIR := .venv
PYTHON := python3
REQUIREMENTS := requirements.txt
TOP_LEVEL_PACKAGES := cryptography google-api-python-client google-auth google-auth-oauthlib mypy pyyaml types-PyYAML

.PHONY: activate all auth clean cloud2enc enc2cloud enc2yaml env2yaml freeze gcloud info install-gcloud set-project setup test yaml2enc yaml2env

.DEFAULT_GOAL := all

activate:
	@echo "Run this to activate the virtual environment:"
	@echo "source $(VENV_DIR)/bin/activate"

all: setup test

auth:
	@echo "🔐 Authenticating with service account..."
	@if echo '$(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)' | grep -q '^{'; then \
		echo "📝 Writing inline JSON to .gsa-tmp.json"; \
		printf '%s\n' '$(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)' > .gsa-tmp.json; \
		gcloud auth activate-service-account --key-file=.gsa-tmp.json; \
		rm .gsa-tmp.json; \
	else \
		if [ ! -f "$(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)" ]; then \
			echo "❌ File not found: $(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)"; \
			exit 1; \
		fi; \
		echo "📁 Using service account file: $(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)"; \
		gcloud auth activate-service-account --key-file="$(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)"; \
	fi

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

cloud2enc:
	@$(VENV_DIR)/bin/python -m main cloud2enc

enc2cloud:
	@$(VENV_DIR)/bin/python -m main enc2cloud

enc2yaml:
	@$(VENV_DIR)/bin/python -m main enc2yaml

env2yaml:
	@$(VENV_DIR)/bin/python -m main env2yaml

freeze:
	@echo "📌 Rewriting $(REQUIREMENTS) with top-level-only packages..."
	@echo "# Top-level dev dependencies" > $(REQUIREMENTS)
	@for pkg in $(TOP_LEVEL_PACKAGES); do echo $$pkg >> $(REQUIREMENTS); done
	@echo "✅ Updated."

gcloud: install-gcloud auth set-project info

# Show current configuration
info:
	@echo "GOOGLE_PROJECT_ID=$(GOOGLE_PROJECT_ID)"
	@echo "GOOGLE_SERVICE_ACCOUNT_KEY_FILE:"
	@if echo '$(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)' | grep -q '^{'; then \
		echo '$(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)' | jq .; \
	else \
		cat "$(GOOGLE_SERVICE_ACCOUNT_KEY_FILE)" | jq .; \
	fi
	@gcloud config list

# Install the Google Cloud SDK
install-gcloud:
	@echo "Installing Google Cloud SDK..."
	sudo apt-get update -y && \
	sudo apt-get install -y apt-transport-https ca-certificates gnupg curl && \
	echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
		| sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list && \
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
		| sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
	sudo apt-get update -y && \
	sudo apt-get install -y google-cloud-sdk

# Set active project
set-project:
	@echo "Setting project to: $(GOOGLE_PROJECT_ID)"
	gcloud config set project $(GOOGLE_PROJECT_ID)

setup:
	@echo "🔧 Creating virtual environment in $(VENV_DIR) if it doesn't exist..."
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	@echo "🚀 Upgrading pip, setuptools, and wheel..."
	$(VENV_DIR)/bin/python -m pip install --upgrade pip setuptools wheel
ifeq ("$(wildcard $(REQUIREMENTS))","")
	@echo "📦 Installing top-level packages: $(TOP_LEVEL_PACKAGES)"
	$(VENV_DIR)/bin/python -m pip install $(TOP_LEVEL_PACKAGES)
	@echo "📝 Writing top-level-only requirements.txt"
	@echo "# Top-level dev dependencies" > $(REQUIREMENTS)
	@for pkg in $(TOP_LEVEL_PACKAGES); do echo $$pkg >> $(REQUIREMENTS); done
else
	@echo "📜 Installing from existing $(REQUIREMENTS)..."
	$(VENV_DIR)/bin/python -m pip install -r $(REQUIREMENTS)
endif
	@echo "✅ Setup complete."

test:
	@echo "Running tests..."
	@$(MAKE) env2yaml && \
	$(MAKE) yaml2enc && \
	$(MAKE) enc2yaml && \
	$(MAKE) yaml2env
#	$(VENV_DIR)/bin/python -m pytest --maxfail=1 --disable-warnings -q
	@echo "✅ Tests completed."

yaml2enc:
	@$(VENV_DIR)/bin/python -m main yaml2enc

yaml2env:
	@$(VENV_DIR)/bin/python -m main yaml2env
