import os
import signal
import sys
import time
import worker_node
import json
import redis.asyncio as redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
WORKER_QUEUE = os.environ.get("WORKER_QUEUE", "queue:jobs")
RESULT_QUEUE = os.environ.get("RESULT_QUEUE", "queue:results")
IDLE_SECONDS = float(os.environ.get("QUEUE_IDLE_SECONDS", "5"))


if not WORKER_QUEUE:
    raise SystemExit("WORKER_QUEUE is required")
if not RESULT_QUEUE:
    raise SystemExit("RESULT_QUEUE is required")

client = redis.Redis.from_url(REDIS_URL)


def _stop(_signum: int, _frame: object) -> None:
    sys.exit(0)


def main(worker: Worker) -> None:
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    while True:
        try:
            if not worker.isBusy:
                job = client.brpop(WORKER_QUEUE, timeout= IDLE_SECONDS)
                if job:
                    name,version,payload = job
                    result = worker.run(name, version, json.loads(payload))
                    client.lpush(RESULT_QUEUE, json.dumps(result))
        except redis.exceptions.RedisError:
            # TELL CORDINATOOR 
            time.sleep(1)
            continue
        time.sleep(IDLE_SECONDS)


if __name__ == "__main__":
    worker = new Worker()
    main(worker)
