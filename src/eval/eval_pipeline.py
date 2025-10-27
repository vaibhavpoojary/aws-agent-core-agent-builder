import argparse, requests, time
from src.utils.mlflow_utils import start_agent_run, log_agent_run
def run_eval(endpoint, prompts=None, project=None, agent=None):
    prompts = prompts or [{"prompt":"Hi there"},{"prompt":"Give me 3 bullet points about LangGraph"},{"prompt":"Bye"}]
    run_id = start_agent_run(agent_name=agent, project_id=project)
    for p in prompts:
        t0=time.time()
        try:
            r=requests.post(endpoint, json={"prompt":p["prompt"], "run_id": run_id}, timeout=10)
            t1=time.time()
            lat = t1-t0
            if r.status_code==200:
                out=r.json().get("output")
                log_agent_run(run_id, p["prompt"], out, metrics={"latency_s": lat})
            else:
                log_agent_run(run_id, p["prompt"], f"ERROR {r.status_code}", metrics={"latency_s": lat})
        except Exception as e:
            t1=time.time()
            lat=t1-t0
            log_agent_run(run_id, p["prompt"], f"EXCEPTION {e}", metrics={"latency_s": lat})
    print("Eval complete")
if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument("--endpoint", required=True)
    p.add_argument("--project")
    p.add_argument("--agent")
    args=p.parse_args()
    run_eval(args.endpoint, project=args.project, agent=args.agent)
