import os
import signal
import sys
import time

import redis

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
WORKER_QUEUE = os.environ.get("WORKER_QUEUE", "jobs")
RESULT_QUEUE = os.environ.get("RESULT_QUEUE", "results")
IDLE_SECONDS = float(os.environ.get("WORKER_IDLE_SECONDS", "5"))

if not WORKER_QUEUE:
    raise SystemExit("WORKER_QUEUE is required")
if not RESULT_QUEUE:
    raise SystemExit("RESULT_QUEUE is required")

client = redis.Redis.from_url(REDIS_URL)


def _stop(_signum: int, _frame: object) -> None:
    sys.exit(0)


def main() -> None:
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    while True:
        try:
            client.ping()
        except redis.exceptions.RedisError:
            time.sleep(1)
            continue
        time.sleep(IDLE_SECONDS)


if __name__ == "__main__":
    main()
