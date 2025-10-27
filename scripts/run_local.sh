#!/bin/bash
export PYTHONPATH=./src:$PYTHONPATH
uvicorn src.agents.langgraph_agent.entrypoint:app --reload --port 8080
