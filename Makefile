GITHUB_PROJECTS_DIR ?= $(HOME)/projects
KEY_FILE := .age-key.txt
SECRETS_DIR := $(GITHUB_PROJECTS_DIR)/secrets
export GITHUB_PROJECTS_DIR KEY_FILE SECRETS_DIR

.PHONY: \
	create-key \
	decrypt \
	decrypt-all \
	encrypt \
	encrypt-all \
	setup

decrypt: ## Decrypt a specific repo's .env.age file
	@$(GITHUB_PROJECTS_DIR)/secrets/age-decrypt-env.sh "$(FILE)"

decrypt-all: ## Decrypt all .env.age files in SECRETS_DIR directory
	@echo "🔓 Decrypting all .env.age files in $(SECRETS_DIR)..."
	@find "$(SECRETS_DIR)" -type f -name '*.env.age' | while read -r file; do \
		"$(SECRETS_DIR)/age-decrypt-env.sh" "$$file"; \
	done

encrypt:
	@$(GITHUB_PROJECTS_DIR)/secrets/age-encrypt-env.sh "$(FILE)"

encrypt-all: ## Encrypt all .env files in GITHUB_PROJECTS_DIR subdirectories
	@echo "🔐 Encrypting all .env files in $(GITHUB_PROJECTS_DIR) subdirectories..."
	@find "$(GITHUB_PROJECTS_DIR)" -type f -name '*.env' | while read -r file; do \
		"$(SECRETS_DIR)/age-encrypt-env.sh" "$$file"; \
	done

setup: ## Install age (https://github.com/FiloSottile/age#installation) and create key
	@sudo apt install age
	age --version
	make create-key

KEY_FILE := .age-key.txt

create-key: ## Create a new key if it doesn't already exist
	@test -f $(KEY_FILE) && echo "✅ Key file already exists: $(KEY_FILE)" || age-keygen -o $(KEY_FILE)

