import os
import signal
import sys
import time
import worker_node
import json
import redis.asyncio as redis
from lua_claim_script import claim_script

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
WORKER_QUEUE = os.environ.get("WORKER_QUEUE", "queue:jobs")
RESULT_QUEUE = os.environ.get("RESULT_QUEUE", "queue:results")
IDLE_SECONDS = float(os.environ.get("QUEUE_IDLE_SECONDS", "5"))
LEASE_TTL = 5


if not WORKER_QUEUE:
    raise SystemExit("WORKER_QUEUE is required")
if not RESULT_QUEUE:
    raise SystemExit("RESULT_QUEUE is required")

client = redis.Redis.from_url(REDIS_URL)
redis_pop_job_create_lease_and_inflight = client.register_script(claim_script)

def _stop(_signum: int, _frame: object) -> None:
    sys.exit(0)

def main(worker: Worker) -> None:
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    while True:
        try:
            raw_job = redis_pop_job_create_lease_and_inflight([WORKER_QUEUE], [worker.id, LEASE_TTL])
            result = worker.run(raw_job)
            with redis.pipeline() as pipe:
                pipe.lpush(RESULT_QUEUE, json.dumps(result)) # TS aggregator needs JSON
                pipe.delete(f"lease:{job.job_id}:{job.chunk_id}")
                pipe.srem(f"inflight:{job.job_id}:{job.chunk_id}")
                pipe.execute()

        except redis.exceptions.RedisError:
            time.sleep(1)
            continue
        time.sleep(IDLE_SECONDS)


if __name__ == "__main__":
    worker = new Worker()
    main(worker)
