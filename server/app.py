import os
import sys
sys.path.insert(0, '/app')

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:
    raise ImportError(f"openenv is required: {e}")

from models import HallucinationsAction, HallucinationsObservation
from server.hallucinations_environment import HallucinationsEnvironment

app = create_app(
    HallucinationsEnvironment,
    HallucinationsAction,
    HallucinationsObservation,
    env_name="hallucinations",
    max_concurrent_envs=1,
)

def main(host: str = "0.0.0.0", port: int = 7860):
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
