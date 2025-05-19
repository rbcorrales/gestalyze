# === PHONY TARGETS ===
.PHONY: install dev build run run-ssl clean train extract-landmarks train-custom train-online mqtt-start mqtt-stop mqtt-test mqtt-setup ha-plugin-start ha-plugin-stop ssl-key-gen deploy-ha clean-models help help-header help-main help-mqtt help-ha help-training help-ssl check-system show-config version update-version website-build website-dev

default: help

# === VARIABLES ===
# Version information
VERSION := $(shell cat VERSION)
PROJECT_NAME := Gestalyze

# Define colors and formatting
BOLD := $(shell tput bold)
GREEN := $(shell tput setaf 2)
BLUE := $(shell tput setaf 4)
YELLOW := $(shell tput setaf 3)
RED := $(shell tput setaf 1)
RESET := $(shell tput sgr0)

# Message formatting functions
define header
	echo "$(BOLD)$(BLUE)$(1)$(RESET)"
endef

define success
	echo "$(BOLD)$(GREEN)✅ $(1)$(RESET)"
endef

define inform
	echo "$(BOLD)$(YELLOW)ℹ️  $(1)$(RESET)"
endef

define error
	echo "$(BOLD)$(RED)❌ $(1)$(RESET)" >&2
endef

# Command check function
define check-command
	@command -v $(1) >/dev/null 2>&1 || { echo "$(BOLD)$(RED)❌ $(2) is required but not installed$(RESET)" >&2; exit 1; }
endef

# Default Python virtual environment directory
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Frontend directory
FRONTEND_DIR = frontend
NPX = cd $(FRONTEND_DIR) && npx

# Backend directory
BACKEND_DIR = backend

# SSL configuration
SSL_DIR = $(BACKEND_DIR)/ssl
SSL_HOSTNAME ?= localhost

# Training directory
TRAINING_DIR = training

# MQTT configuration
MQTT_DIR = $(BACKEND_DIR)/mqtt
MQTT_CONFIG = $(MQTT_DIR)/mosquitto.conf
MQTT_PASSWORD_FILE = $(MQTT_DIR)/mosquitto.passwd
MQTT_ACL_FILE = $(MQTT_DIR)/mosquitto.acl

# Home Assistant plugin directory
HA_PLUGIN_DIR = homeassistant/gestalyze_plugin

# Website directory
WEBSITE_DIR = website

# === SYSTEM COMMANDS ===
# Check system requirements
check-system:
	@$(call header,"Checking system requirements...")
	@$(call check-command,python3,Python 3)
	@$(call check-command,node,Node.js)
	@$(call check-command,npm,npm)
	@$(call check-command,mosquitto,Mosquitto)
	@$(call success,"All system requirements are met!")

# Show version information
version:
	@$(call header,"$(PROJECT_NAME) v$(VERSION)")
	@echo "Python: $$(command -v python3) - $$(python3 --version 2>&1)"
	@echo "Node: $$(command -v node) - $$(node --version 2>&1)"
	@echo "npm: $$(command -v npm) - $$(npm --version 2>&1)"
	@echo "Mosquitto: $$(command -v mosquitto) - $$(mosquitto -h 2>&1 | head -n1)"

# Update version
update-version:
	@read -p "Enter new version (e.g., 0.1.0): " new_version; \
	echo "$$new_version" > VERSION
	@$(call success,"Version updated to $$(cat VERSION)")

# Show current configuration
show-config:
	@$(call header,"Current Configuration:")
	@echo "Project: $(PROJECT_NAME) v$(VERSION)"
	@echo "Python venv: $(VENV)"
	@echo "Frontend dir: $(FRONTEND_DIR)"
	@echo "Backend dir: $(BACKEND_DIR)"
	@echo "SSL hostname: $(SSL_HOSTNAME)"
	@echo "MQTT dir: $(MQTT_DIR)"
	@echo "Training dir: $(TRAINING_DIR)"
	@echo "Home Assistant plugin dir: $(HA_PLUGIN_DIR)"

# === INSTALLATION COMMANDS ===
# Install all dependencies
install: check-system install-python install-node mqtt-setup

# Set up Python virtual environment and install dependencies
install-python:
	@if [ ! -d "$(VENV)" ]; then \
		python -m venv $(VENV); \
	fi
	$(PIP) install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
	$(PIP) install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Install Node.js dependencies
install-node:
	cd $(FRONTEND_DIR) && npm install

# === DEVELOPMENT COMMANDS ===
# Run development servers
dev: dev-backend dev-frontend

# Run backend in development mode
dev-backend:
	PYTHONPATH=. $(PYTHON) -m uvicorn --app-dir $(BACKEND_DIR) main:app --reload

# Run frontend in development mode
dev-frontend:
	@command -v npx >/dev/null 2>&1 || { echo >&2 "Error: npx is not installed."; exit 1; }
	$(NPX) vite

# === APPLICATION COMMANDS ===
# Build the frontend for production
build:
	$(NPX) vite build

# Run the application
run: build mqtt-start
	PYTHONPATH=. $(PYTHON) -m uvicorn --app-dir $(BACKEND_DIR) main:app --host 0.0.0.0 --port 8000

run-ssl: build mqtt-start ssl-key-gen
	PYTHONPATH=. $(PYTHON) -m uvicorn --app-dir $(BACKEND_DIR) main:app --host 0.0.0.0 --port 8000 --ssl-keyfile $(SSL_DIR)/key.pem --ssl-certfile $(SSL_DIR)/cert.pem

# Clean up generated files
clean:
	@if [ -d "$(FRONTEND_DIR)/dist" ]; then rm -rf $(FRONTEND_DIR)/dist; fi
	@if [ -d "$(FRONTEND_DIR)/node_modules" ]; then rm -rf $(FRONTEND_DIR)/node_modules; fi
	@if [ -d "$(WEBSITE_DIR)/dist" ]; then rm -rf $(WEBSITE_DIR)/dist; fi
	@if [ -d "$(WEBSITE_DIR)/node_modules" ]; then rm -rf $(WEBSITE_DIR)/node_modules; fi
	@if [ -d "$(VENV)" ]; then rm -rf $(VENV); fi
	find . -type d -name __pycache__ -exec rm -rf {} +
	@if [ -d "$(MQTT_DIR)/logs" ]; then rm -rf $(MQTT_DIR)/logs; fi

# === MQTT COMMANDS ===
# Create MQTT password file and add user
mqtt-setup:
	@$(call header,"Setting up MQTT authentication...")
	@$(call inform,"Deleting old MQTT password and ACL files...")
	@rm -f $(MQTT_PASSWORD_FILE) $(MQTT_ACL_FILE)
	@touch $(MQTT_PASSWORD_FILE)
	@chmod 0700 $(MQTT_PASSWORD_FILE)
	@echo "# Allow users to read/write their own topics" > $(MQTT_ACL_FILE)
	@echo "pattern readwrite %u/#" >> $(MQTT_ACL_FILE)
	@echo "# Allow all users to read system topics" >> $(MQTT_ACL_FILE)
	@echo 'topic read $$SYS/#' >> $(MQTT_ACL_FILE)
	@chmod 0700 $(MQTT_ACL_FILE)
	@$(call inform,"Adding MQTT user 'gestalyze'...")
	@mosquitto_passwd -b $(MQTT_PASSWORD_FILE) gestalyze gestalyze_password
	@$(call success,"MQTT setup complete!")

# Start the MQTT broker
mqtt-start:
	@$(call header,"Starting MQTT broker...")
	@if pgrep mosquitto > /dev/null; then \
		$(call inform,"Mosquitto broker is already running."); \
	else \
		if [ ! -d "$(MQTT_DIR)/logs" ]; then \
			$(call inform,"Creating log directory...") && \
			mkdir -p $(MQTT_DIR)/logs; \
		fi; \
		$(call success,"Starting Mosquitto broker..."); \
		mosquitto -c $(MQTT_CONFIG) & \
	fi

# Stop the MQTT broker
mqtt-stop:
	@$(call header,"Stopping MQTT broker...")
	pkill mosquitto

# Test MQTT functionality
mqtt-test:
	@$(call header,"Testing MQTT functionality...")
	$(PYTHON) -m $(BACKEND_DIR).mqtt.mqtt_test

# === SSL COMMANDS ===
# Generate SSL certificates
ssl-key-gen:
	@$(call header,"Generating SSL certificates for $(SSL_HOSTNAME)...")
	@mkdir -p $(SSL_DIR)
	@openssl genrsa -out $(SSL_DIR)/key.pem 2048
	@openssl req -new -x509 -key $(SSL_DIR)/key.pem -out $(SSL_DIR)/cert.pem -days 365 -subj "/CN=$(SSL_HOSTNAME)"
	@$(call success,"SSL certificates generated successfully!")

# === TRAINING COMMANDS ===
# Extract landmarks from training and test datasets
# Usage: make extract-landmarks DATASET_NAME=<name>
extract-landmarks:
	@if [ -z "$(DATASET_NAME)" ]; then \
		$(call error,"DATASET_NAME is required"); \
		exit 1; \
	fi
	PYTHONPATH=. $(PYTHON) $(TRAINING_DIR)/extract_landmarks.py --dataset-name $(DATASET_NAME)

# Train ASL classifier models
# Usage: make train MODEL_TYPE=<type> DATASET_NAME=<name>
# Example: make train MODEL_TYPE=custom DATASET_NAME=custom_dataset
train:
	@if [ -z "$(MODEL_TYPE)" ]; then \
		$(call error,"MODEL_TYPE is required. Use 'custom' or 'online'"); \
		exit 1; \
	fi
	@if [ -z "$(DATASET_NAME)" ]; then \
		$(call error,"DATASET_NAME is required"); \
		exit 1; \
	fi
	# Generate model name from dataset name (remove special chars and spaces)
	@MODEL_NAME=$$(echo $(DATASET_NAME) | tr '/' '_' | tr -cd '[:alnum:]_' | tr '[:upper:]' '[:lower:]'); \
	PYTHONPATH=. $(PYTHON) $(TRAINING_DIR)/train.py \
		--model-type $(MODEL_TYPE) \
		--model-path models/$(MODEL_TYPE)_$$MODEL_NAME.joblib \
		--dataset-name $(DATASET_NAME)

# Clean up trained models
clean-models:
	rm -f models/*.joblib

# === HOME ASSISTANT COMMANDS ===
# Start the Home Assistant plugin
ha-plugin-start:
	@$(call header,"Starting Home Assistant plugin...")
	$(PYTHON) $(HA_PLUGIN_DIR)/run_plugin.py

# Stop the Home Assistant plugin
ha-plugin-stop:
	@$(call header,"Stopping Home Assistant plugin...")
	pkill -f "python.*run_plugin.py"

# === HOME ASSISTANT DEPLOYMENT ===
# Home Assistant deployment configuration
HA_HOST = 192.168.50.88
HA_PORT = 2222
HA_USER = root
INTEGRATION = gestalyze
LOCAL_PATH = ./homeassistant/custom_components/$(INTEGRATION)
REMOTE_PATH = /config/custom_components/$(INTEGRATION)

# Deploy to Home Assistant
deploy-ha:
	@$(call header,"🚀 Deploying $(INTEGRATION) to Home Assistant using SCP...")
	scp -P $(HA_PORT) -r $(LOCAL_PATH) $(HA_USER)@$(HA_HOST):/config/custom_components/
	@$(call success,"Deploy complete!")

# === WEBSITE COMMANDS ===
# Build the website for production
website-build:
	@$(call header,"Building website for production...")
	cd $(WEBSITE_DIR) && npm install && npm run build
	@$(call success,"Website built successfully!")

# Run website in development mode
website-dev:
	@$(call header,"Starting website development server...")
	cd $(WEBSITE_DIR) && npm install && npm run dev

# === HELP COMMANDS ===
# Help target to show available commands
help: help-header help-system help-main help-mqtt help-ha help-ssl help-training

# Show help header
help-header:
	@$(call inform,"$(PROJECT_NAME) v$(VERSION)")
	@echo ""
	@$(call header,"Available commands:")

# Show system commands help
help-system:
	@echo ""
	@$(call header,"System commands:")
	@echo "  $(GREEN)make check-system$(RESET)        - Check system requirements"
	@echo "  $(GREEN)make version$(RESET)             - Show version information"
	@echo "  $(GREEN)make update-version$(RESET)      - Update project version"
	@echo "  $(GREEN)make show-config$(RESET)         - Show current configuration"

# Show main commands help
help-main:
	@echo ""
	@$(call header,"Main commands:")
	@echo "  $(GREEN)make install$(RESET)             - Install all dependencies"
	@echo "  $(GREEN)make dev$(RESET)                 - Run development servers"
	@echo "  $(GREEN)make run$(RESET)                 - Run production server"
	@echo "  $(GREEN)make run-ssl$(RESET)             - Run production server with SSL"
	@echo "  $(GREEN)make clean$(RESET)               - Clean up generated files"
	@echo "  $(GREEN)make website-build$(RESET)       - Build website for production"
	@echo "  $(GREEN)make website-dev$(RESET)         - Run website in development mode"

# Show MQTT commands help
help-mqtt:
	@echo ""
	@$(call header,"MQTT commands:")
	@echo "  $(GREEN)make mqtt-start$(RESET)          - Start the MQTT broker"
	@echo "  $(GREEN)make mqtt-stop$(RESET)           - Stop the MQTT broker"
	@echo "  $(GREEN)make mqtt-test$(RESET)           - Test MQTT functionality"
	@echo "  $(GREEN)make mqtt-setup$(RESET)          - Set up MQTT authentication"

# Show Home Assistant commands help
help-ha:
	@echo ""
	@$(call header,"Home Assistant commands:")
	@echo "  $(GREEN)make ha-plugin-start$(RESET)     - Start the Home Assistant plugin"
	@echo "  $(GREEN)make ha-plugin-stop$(RESET)      - Stop the Home Assistant plugin"
	@echo "  $(GREEN)make deploy-ha$(RESET)           - Deploy the Home Assistant custom integration"

# Show SSL commands help
help-ssl:
	@echo ""
	@$(call header,"SSL commands:")
	@echo "  $(GREEN)make ssl-key-gen$(RESET)         - Generate SSL certificates for development"

# Show training commands help
help-training:
	@echo ""
	@$(call header,"Training commands:")
	@echo "  $(GREEN)make train MODEL_TYPE=<type> DATASET_NAME=<name>$(RESET)"
	@echo "    Train a model using the specified dataset"
	@echo "    $(YELLOW)MODEL_TYPE:$(RESET) 'custom' or 'online'"
	@echo "    $(YELLOW)DATASET_NAME:$(RESET) name of the dataset directory in datasets/ (for custom) or HuggingFace dataset name (for online)"
	@echo "    Note: Model name is automatically generated from dataset name"
	@echo ""
	@echo "  $(GREEN)make extract-landmarks DATASET_NAME=<name>$(RESET)"
	@echo "    Extract hand landmarks from a dataset"
	@echo ""
	@echo "  $(GREEN)make clean-models$(RESET)"
	@echo "    Remove all trained model files"
