import os
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240229-v1:0")
REGION = os.environ.get("AWS_REGION", "us-east-1")

model = BedrockModel(model_id=MODEL_ID, region_name=REGION)
agent = Agent(model=model)

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    user_prompt = payload.get("prompt", "Hello! How can I help you?")
    result = agent(user_prompt)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
