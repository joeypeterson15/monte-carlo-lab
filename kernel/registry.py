# USE a decorator to register kernel functions
import numpy as np
import param_models 
KERNELS = {}

def register_kernel(name: str):
    def wrapper(func):
        KERNELS[name] = func
        return func
    return wrapper

@register_kernel("pi")
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





