PROJECTS_DIR := $(GITHUB_PARENT_DIR) # Change as required

.PHONY: \
	decrypt_env \
	encrypt_env

decrypt_env:
	@$(PROJECTS_DIR)/secrets/decrypt.sh

encrypt_env:
	@$(PROJECTS_DIR)/secrets/encrypt.sh
