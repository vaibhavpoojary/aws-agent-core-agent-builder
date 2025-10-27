import argparse, tarfile, tempfile, os, time
from pathlib import Path
from .s3_utils import upload_file, ensure_bucket
from .mlflow_utils import register_artifact

def package_agent(agent: str, version: str, bucket: str):
    base = Path("src/agents") / agent
    if not base.exists():
        raise FileNotFoundError(f"Agent dir {base} does not exist")
    ensure_bucket(bucket)
    timestamp = str(int(time.time()))
    artifact_name = f"{agent}_{version}_{timestamp}.tar.gz"
    out_path = Path(tempfile.gettempdir()) / artifact_name
    with tarfile.open(out_path, "w:gz") as tar:
        for p in base.iterdir():
            tar.add(p, arcname=p.name)
    key = f"agents/{artifact_name}"
    s3_uri = upload_file(str(out_path), bucket, key)
    register_artifact(agent, version, s3_uri)
    print(s3_uri)
    return s3_uri
if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument("--agent", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--bucket", required=True)
    args=p.parse_args()
    package_agent(args.agent, args.version, args.bucket)
