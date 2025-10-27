import boto3, json
from .config import AWS_REGION, PROJECT_ID, AGENT_NAME
def create_dashboard(project_id=None, agent_name=None):
    project_id = project_id or PROJECT_ID
    agent_name = agent_name or AGENT_NAME
    client = boto3.client("cloudwatch", region_name=AWS_REGION)
    dashboard_name = f"{project_id}-{agent_name}-dashboard"
    body = json.dumps({"widgets": []})
    client.put_dashboard(DashboardName=dashboard_name, DashboardBody=body)
    print("Created dashboard:", dashboard_name)
