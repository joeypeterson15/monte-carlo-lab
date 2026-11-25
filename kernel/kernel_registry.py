import os
import numpy as np
import pydantic as pd
from pathlib import Path
import params_registry

CHUNK_SIZE = os.environ.get("CHUNK_SIZE", 1000) 
KERNEL_REGISTRY= {}

def register_kernel(name: str):
    def wrapper(func):
        KERNEL_REGISTRY[name] = func
        return func
    return wrapper


@register_kernel("pi")
def pi(job, params) -> int:
    # Create randomized x,y values between (0,1) using seed so the randomization is deterministic. 
    # Its possible for jobs to be retried if the worker takes a long time to process them and lease expires. 
    # So we achieve idempotency if a duplicate job is added to results
    seed_val = job["seed_id"]
    chunk_id
    rng = np.random.default_rng(seed=seed_val)
    values = rng.random(2,n) #2xn array w. 0<=num<=1
    square = 0
    circle = 0
    for i,j in range(len(values[0])):
        x,y = values[0][i], values[1][j]
        mag = np.sqrt(x^2 + y^2)
        if mag <= 1:
            circle += 1
        else:
            square += 1
    return 4 * (circle/square)

