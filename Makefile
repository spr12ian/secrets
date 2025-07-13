KEY_FILE := .age-key.txt
# Set this to the absolute path of the parent directory for all GitHub repos
PROJECTS_DIR := $(GITHUB_PARENT_DIR)
SECRETS_DIR := $(PROJECTS_DIR)/secrets
export

.PHONY: \
	decrypt \
	decrypt-all \
	encrypt \
	encrypt-all

decrypt: ## Decrypt a specific repo's .env.age file
	@$(PROJECTS_DIR)/secrets/age-decrypt-env.sh "$(FILE)"

decrypt-all: ## Decrypt all .env.age files in SECRETS_DIR directory
	@echo "🔓 Decrypting all .env.age files in $(SECRETS_DIR)..."
	@find "$(SECRETS_DIR)" -type f -name '*.env.age' | while read -r file; do \
		"$(PROJECTS_DIR)/secrets/age-decrypt-env.sh" "$$file"; \
	done

encrypt:
	@$(PROJECTS_DIR)/secrets/age-encrypt-env.sh "$(FILE)"

encrypt-all: ## Encrypt all .env files in PROJECTS_DIR subdirectories
	@echo "🔐 Encrypting all .env files in $(PROJECTS_DIR) subdirectories..."
	@find "$(PROJECTS_DIR)" -type f -name '*.env' | while read -r file; do \
		"$(PROJECTS_DIR)/secrets/age-encrypt-env.sh" "$$file"; \
	done
