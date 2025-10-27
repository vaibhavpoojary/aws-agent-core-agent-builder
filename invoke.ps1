param (
    [string]$Task = "all"
)

# ==============================
# Project Variables
# ==============================
$AGENT_NAME = "claude_chatbot"
$AGENT_PATH = "src/agents/claude_chatbot"
$DIST_DIR = "dist"
$REGION = "us-east-1"
$EXEC_ROLE = ""
$ECR_REPO = "agent-platform"
$IMAGE_TAG = "latest"
$TARBALL = "$DIST_DIR/$AGENT_NAME.tar.gz"
$MLFLOW_TRACKING_URI = ""

switch ($Task) {

    "all" {
        . .\invoke.ps1 clean
        . .\invoke.ps1 package
        . .\invoke.ps1 register
        . .\invoke.ps1 deploy
    }

    "build" {
        Write-Host "Building Docker image..."
        docker build -t "${ECR_REPO}:${IMAGE_TAG}" -f build/Dockerfile .
    }

    "package" {
        Write-Host "Packaging agent into tarball..."
        if (-not (Test-Path $DIST_DIR)) { New-Item -ItemType Directory -Path $DIST_DIR | Out-Null }
        python -m src.utils.package_agent --agent-path $AGENT_PATH --output $TARBALL
    }

    "register" {
        Write-Host "Registering agent tarball in MLflow..."
        python src/utils/mlflow_utils.py `
            --agent-name $AGENT_NAME `
            --artifact-path $TARBALL `
            --mlflow-uri $MLFLOW_TRACKING_URI
    }

    "push" {
        Write-Host "Pushing Docker image to ECR..."
        bash build/build_push.sh $ECR_REPO $IMAGE_TAG
    }

    "deploy" {
        Write-Host "Deploying agent to AgentCore..."
        agentcore configure `
            --entrypoint src/agents/claude_chatbot/entrypoint.py `
            --name $AGENT_NAME `
            --requirements-file "$AGENT_PATH/requirements.txt" `
            --execution-role $EXEC_ROLE `
            --region $REGION
        agentcore launch
    }

    "run" {
        Write-Host "Running agent locally..."
        python "$AGENT_PATH/entrypoint.py"
    }

    "eval" {
        Write-Host "Running evaluation pipeline..."
        python src/eval/eval_pipeline.py `
            --agent-name $AGENT_NAME `
            --endpoint http://localhost:8080 `
            --mlflow-uri $MLFLOW_TRACKING_URI
    }

    "logs" {
        Write-Host "Fetching logs..."
        python src/utils/cloudwatch_setup.py --logs --agent $AGENT_NAME
    }

    "clean" {
        Write-Host "Cleaning up build artifacts..."
        if (Test-Path $DIST_DIR) { Remove-Item -Recurse -Force "$DIST_DIR/*" }
        Get-ChildItem -Recurse -Include __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }

    Default {
        Write-Host "Unknown task: $Task"
    }
}
