import os
def env(k, d=None): return os.getenv(k, d)
MLFLOW_TRACKING_URI = env("MLFLOW_TRACKING_URI", "http://localhost:5000")
AWS_REGION = env("AWS_REGION", "us-east-1")
AWS_S3_BUCKET = env("AWS_S3_BUCKET", "your-agent-artifacts-bucket")
PROJECT_ID = env("PROJECT_ID", "my_project")
AGENT_NAME = env("AGENT_NAME", "langgraph_agent")
AGENT_VERSION = env("AGENT_VERSION", "v1")
AGENTCORE_CLI = env("AGENTCORE_CLI", "agentcore")
