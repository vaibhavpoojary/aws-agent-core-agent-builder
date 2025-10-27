# ==============================
# Project Variables
# ==============================
AGENT_NAME=claude_chatbot
AGENT_PATH=src/agents/claude_chatbot
DIST_DIR=dist
REGION=us-east-1
EXEC_ROLE=
ECR_REPO=agent-platform
IMAGE_TAG=latest
TARBALL=$(DIST_DIR)/$(AGENT_NAME).tar.gz
MLFLOW_TRACKING_URI=http://

.PHONY: all build package register push deploy run eval logs clean

# ==============================
# Full pipeline
# ==============================
all: clean package register deploy

# ==============================
# Build Docker image
# ==============================
build:
	@echo "🔨 Building Docker image..."
	docker build -t $(ECR_REPO):$(IMAGE_TAG) -f build/Dockerfile .

# ==============================
# Package agent as tarball with bootstrap
# ==============================
package:
	@echo "📦 Packaging agent into tarball..."
	mkdir -p $(DIST_DIR)
	python src/utils/package_agent.py --agent-path $(AGENT_PATH) --output $(TARBALL)

# ==============================
# Register tarball in MLflow
# ==============================
register:
	@echo "📝 Registering agent tarball in MLflow..."
	python src/utils/mlflow_utils.py \
		--agent-name $(AGENT_NAME) \
		--artifact-path $(TARBALL) \
		--mlflow-uri $(MLFLOW_TRACKING_URI)

# ==============================
# Push Docker image to ECR
# ==============================
push:
	@echo "🚀 Pushing Docker image to ECR..."
	bash build/build_push.sh $(ECR_REPO) $(IMAGE_TAG)

# ==============================
# Deploy agent to AgentCore
# ==============================
deploy:
	@echo "🛠 Deploying agent to AgentCore..."
	agentcore configure \
		--entrypoint src/agents/claude_chatbot/entrypoint.py \
		--name $(AGENT_NAME) \
		--requirements-file $(AGENT_PATH)/requirements.txt \
		--execution-role $(EXEC_ROLE) \
		--region $(REGION)
	agentcore launch

# ==============================
# Run agent locally
# ==============================
run:
	@echo "▶️ Running agent locally..."
	python $(AGENT_PATH)/entrypoint.py

# ==============================
# Run evaluation pipeline
# ==============================
eval:
	@echo "📊 Running evaluation pipeline..."
	python src/eval/eval_pipeline.py \
		--agent-name $(AGENT_NAME) \
		--endpoint http://localhost:8080 \
		--mlflow-uri $(MLFLOW_TRACKING_URI)

# ==============================
# Fetch logs (optional CloudWatch integration)
# ==============================
logs:
	@echo "📜 Fetching logs from CloudWatch..."
	python src/utils/cloudwatch_setup.py --logs --agent $(AGENT_NAME)

# ==============================
# Clean build artifacts
# ==============================
clean:
	@echo "🧹 Cleaning up build artifacts..."
	rm -rf $(DIST_DIR)/* __pycache__ */__pycache__
