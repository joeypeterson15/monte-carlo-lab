import os
import numpy as np
import param_models
import pydantic as pd
from pathlib import Path

KERNELS = {}
chunk_size = os.environ.get("CHUNK_SIZE", 1000)

class PiMetaData(pd.BaseModel):
    name: str ="pi",
    chunk_size: int = CHUNK_SIZE

pi_meta_data = PiMetaData

Path("kernel_meta_data.json").write_text(pi_meta_data.model_dump_json(indent=2), encoding="utf-8")

def register_kernel(meta_data):
    def wrapper(func):
        KERNELS[meta_data["name"]] = {"func": func, "chunk_size": meta_data["chunk_size"]}
        return func
    return wrapper

@register_kernel(*pi_meta_data)
def pi(version: int, params: PiParams) -> int:
    # Create randomized x,y values between (0,1) using seed so the randomization is deterministic
    seed_val = params["seed"]
    n = params["n"]
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

