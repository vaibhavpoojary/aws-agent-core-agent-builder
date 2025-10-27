# 📘 Agent Platform

An **AWS-native platform** for building, evaluating, deploying, and observing **LangGraph / LangChain / CrewAI-based agents**.  
It integrates with **MLflow**, **AgentCore**, and the **AWS observability stack** for an end-to-end multi-tenant agent workflow.

---

## 📂 Folder Structure

```plaintext
agent-platform/
│── Makefile                     # Automation shortcuts
│── requirements.txt              # Python dependencies
│── .env.example                  # Example environment variables
│── README.md                     # Project documentation
│
├── build/
│   ├── Dockerfile                # Container for agent
│   ├── build_push.sh             # Build & push Docker to ECR
│
├── src/
│   ├── agents/
│   │   └── langgraph_agent/
│   │       ├── graph_stub.py     # Sample LangGraph graph
│   │       ├── entrypoint.py     # FastAPI wrapper for AgentCore
│   │       └── bootstrap.sh      # Bootstrap script for AgentCore runtime
│   │
│   ├── utils/
│   │   ├── mlflow_utils.py       # Log/run/register agents in MLflow
│   │   ├── ecr_utils.py          # ECR repo & image helper
│   │   ├── agentcore_deploy.py   # Deploy agent tarball to AgentCore
│   │   ├── package_agent.py      # Package agent into tarball
│   │   └── cloudwatch_setup.py   # Dashboards, alarms, logs
│   │
│   └── eval/
│       ├── eval_pipeline.py      # Run evaluation pipelines
│       └── agenteval_integration.py # Hooks for agent evaluation
│
├── infra/
│   ├── ecr_s3_iam.yaml           # CloudFormation / CDK IaC for ECR + S3 + IAM
│   └── codepipeline.yaml         # CI/CD pipeline definition
│
├── scripts/
│   ├── run_local.sh              # Run agent locally
│   ├── run_eval.sh               # Run evaluation locally
│   └── agentcore_cmds.sh         # AgentCore CLI shortcuts
│
└── tests/
    └── test_agent.py             # Unit tests for agent
```

---

## 🚀 Quickstart

### 1️⃣ Setup Environment
```bash
cp .env.example .env
pip install -r requirements.txt
```

### 2️⃣ Build, Package & Deploy
Use the **Makefile** for automation:

```bash
make build      # Build Docker image
make package    # Package agent into tarball with bootstrap
make push       # Push image to ECR
make deploy     # Deploy tarball to AgentCore
```

Or run everything in one go:
```bash
make all
```

### 3️⃣ Run Evaluation
```bash
make eval
```
This runs evaluation pipeline, logs metrics (latency, cost, accuracy) into **MLflow**, and compares across agent versions.

### 4️⃣ Observe
```bash
make logs
```
Fetch **CloudWatch logs** and metrics.  
Dashboards & alarms are configured via `cloudwatch_setup.py`.

---

## 🛠️ Components

- **Build Layer** → Docker + SageMaker-ready packaging  
- **Evaluation Layer** → Hosted MLflow integration  
- **Deployment Layer** → AgentCore runtime (tarball deployment)  
- **Observability Layer** → CloudWatch metrics/logs + SNS/EventBridge alerts  

---

## ✅ Best Practices

- Use **IAM least privilege** roles in `infra/ecr_s3_iam.yaml`  
- Apply **project-based tagging** for multi-tenancy (`ProjectID`, `Owner`, `Environment`)  
- Use **tarball packaging** for reproducible deployments  
- Keep **evaluation scripts modular** for multiple frameworks (LangGraph, CrewAI, etc.)  

---

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Simulate an end-to-end flow:
```bash
make all
make eval
make logs
```
