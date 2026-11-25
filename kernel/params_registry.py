from pydantic import BaseModel
CHUNK_SIZE = os.environ.get("CHUNK_SIZE", 1000) 

PARAMS_REGISTRY = {}

def register_kernel_params():
    def wrapper(model):
        PARAMS_REGISTRY[model["name"]] = model
        return model
    return wrapper

@register_kernel_params()   
class PiParams(pd.BaseModel):
    dummy: str = "dumbo"
    name: str = "pi"


#EXPORT THIS CLASS-CONTAINS ALL INFORMATION FOR COORDINATOR
class KernelDataSchema(pd.BaseModel):
    job_id: str
    chunk_id: int
    chunk_size: int = CHUNK_SIZE
    name: str
    entropy: int = 9876543210123456789
    # schema_version: int

PARAMS_REGISTRY['data'] = KernelDataSchema

# job_id	job42	Which job this belongs to (used for lease, inflight, and result keys)
# chunk_id	7	Which slice of the job. Also the seed input and the dedupe key
# kernel	"pi"	Registry lookup name
# kernel_version	1	The worker refuses the chunk if its code version doesn't match
# params	{} for pi	Validated kernel parameters, passed through untouched
# n	250000	Samples in this chunk, not the whole job
# entropy	a big integer	The job's base seed. The worker combines it with chunk_id to build the seed
# schema_version	1	Version of the message format itself

# # Master dispatcher creates tasks using a shared base entropy and unique spawn_keys
# BASE_ENTROPY = 9876543210123456789

# def worker_task(job_id: int) -> np.ndarray:
#     # Reconstruct the exact child SeedSequence from primitive integers
#     ss = np.random.SeedSequence(entropy=BASE_ENTROPY, spawn_key=(job_id,))
#     rng = np.random.default_rng(ss)
#     return rng.random(3)

# # Worker 0 and Worker 1 get guaranteed independent streams without sharing state
# print("Job 0:", worker_task(0))
# print("Job 1:", worker_task(1))