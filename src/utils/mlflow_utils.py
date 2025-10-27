import mlflow, time
from .config import MLFLOW_TRACKING_URI, PROJECT_ID
from .logger import get_logger
logger = get_logger("mlflow_utils")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
def start_agent_run(agent_name=None, project_id=None):
    agent_name = agent_name or PROJECT_ID
    project_id = project_id or PROJECT_ID
    run = mlflow.start_run(run_name=f"{project_id}_{agent_name}_{int(time.time())}")
    logger.info(f"Started MLflow run: {run.info.run_id}")
    return run.info.run_id
def log_agent_run(run_id: str, input_text: str, output_text: str, metrics: dict=None, params: dict=None):
    with mlflow.start_run(run_id=run_id):
        mlflow.log_param("input_text", input_text)
        mlflow.log_param("output_text", output_text)
        if params:
            for k,v in params.items():
                mlflow.log_param(k,v)
        if metrics:
            for k,v in metrics.items():
                mlflow.log_metric(k, float(v))
    logger.info(f"Logged to MLflow run {run_id}")
def register_artifact(agent_name: str, version: str, s3_uri: str):
    logger.info(f"Registering artifact {s3_uri} for {agent_name}:{version} in MLflow (placeholder)")
    return True
