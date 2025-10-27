PYTHON?=python3
VENV?=.venv
PIP?=$(VENV)/bin/python -m pip

# Azure variables (override with your values)
ACR_NAME?=apihockey
ACR_LOGIN_SERVER?=$(shell az acr show --name $(ACR_NAME) --query loginServer --output tsv 2>/dev/null || echo "$(ACR_NAME).azurecr.io")
IMAGE_NAME?=my-image
IMAGE_TAG?=latest
RESOURCE_GROUP?=apihockey
CONTAINER_NAME?=apihockey

# Default target
.PHONY: help install venv clean-venv docker-build docker-push docker-deploy azure-update

help:
	@echo "Available targets:"
	@echo ""
	@echo "  Python/Venv:"
	@echo "    install         Create a venv (default .venv) and install dependencies"
	@echo "    venv            Create the virtualenv only"
	@echo "    clean-venv      Remove the virtualenv directory"
	@echo ""
	@echo "  Docker:"
	@echo "    docker-build    Build the Docker image locally"
	@echo "    docker-push     Push the Docker image to Azure Container Registry"
	@echo "    docker-deploy   Build and push in one command"
	@echo ""
	@echo "  Azure:"
	@echo "    azure-update    Build, push and restart the Azure container (full deploy)"
	@echo ""
	@echo "  Variables (override with VAR=value):"
	@echo "    ACR_NAME=$(ACR_NAME)"
	@echo "    IMAGE_NAME=$(IMAGE_NAME)"
	@echo "    RESOURCE_GROUP=$(RESOURCE_GROUP)"
	@echo "    CONTAINER_NAME=$(CONTAINER_NAME)"

venv:
	@echo "Ensuring virtualenv $(VENV) exists..."
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "Created virtualenv at $(VENV)"; \
	else \
		echo "Virtualenv $(VENV) already exists"; \
	fi

install: venv
	@echo "Installing from requirements.txt into $(VENV)..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

clean-venv:
	@echo "Removing virtualenv directory $(VENV)..."
	@rm -rf $(VENV)

# Docker targets
docker-build:
	@echo "Building Docker image $(IMAGE_NAME):$(IMAGE_TAG)..."
	@docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(ACR_LOGIN_SERVER)/$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✓ Image built and tagged successfully"

docker-push:
	@echo "Logging into Azure Container Registry..."
	@az acr login --name $(ACR_NAME)
	@echo "Pushing image to $(ACR_LOGIN_SERVER)/$(IMAGE_NAME):$(IMAGE_TAG)..."
	@docker push $(ACR_LOGIN_SERVER)/$(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✓ Image pushed successfully"

docker-deploy: docker-build docker-push
	@echo "✓ Build and push completed"

# Azure deployment targets
azure-update: docker-deploy
	@echo "Restarting Azure container $(CONTAINER_NAME)..."
	@az container restart \
		--resource-group $(RESOURCE_GROUP) \
		--name $(CONTAINER_NAME)
	@echo "✓ Container restarted successfully"
	@echo ""
	@echo "Getting container URL..."
	@az container show \
		--resource-group $(RESOURCE_GROUP) \
		--name $(CONTAINER_NAME) \
		--query ipAddress.fqdn \
		--output tsv
	@echo ""
	@echo "✓ Deployment complete!"
