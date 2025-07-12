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
	@$(PROJECTS_DIR)/secrets/age-decrypt-env.sh "$(REPO)"

decrypt-all: ## Decrypt all .env.age files in PROJECTS_DIR subdirectories
	@echo "🔓 Decrypting all .env.age files in $(PROJECTS_DIR)..."
	@find "$(PROJECTS_DIR)" -type f -name '.env.age' | while read -r file; do \
		repo_dir="$$(dirname "$$file")"; \
		echo "🔓 Decrypting $$file..."; \
		"$(PROJECTS_DIR)/secrets/age-decrypt-env.sh" "$$repo_dir"; \
	done

encrypt:
	@$(PROJECTS_DIR)/secrets/age-encrypt-env.sh "$(REPO)"

encrypt-all:
	loop through all directories in PROJECTs_DIR and encrypt .env where found
