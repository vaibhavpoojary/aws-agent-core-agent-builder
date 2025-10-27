import argparse, subprocess
from .config import AGENTCORE_CLI
def deploy_agent(agent: str, version: str, artifact_s3_uri: str):
    cfg_cmd = [AGENTCORE_CLI, "configure", "--project", agent, "--agent", agent, "--artifact", artifact_s3_uri]
    print("Running:", " ".join(cfg_cmd))
    subprocess.run(cfg_cmd, check=True)
    launch_cmd = [AGENTCORE_CLI, "launch", "--project", agent, "--agent", agent]
    print("Running:", " ".join(launch_cmd))
    subprocess.run(launch_cmd, check=True)
if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument("--agent", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--artifact-s3-uri", required=True)
    args=p.parse_args()
    deploy_agent(args.agent, args.version, args.artifact_s3_uri)
