#!/bin/bash
python3 src/eval/eval_pipeline.py --endpoint http://127.0.0.1:8080/invoke --project my_project --agent langgraph_agent
