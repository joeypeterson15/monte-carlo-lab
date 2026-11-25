from pydantic import BaseModel
# Path("kernel_meta_data.json").write_text(pi_meta_data.model_dump_json(indent=2), encoding="utf-8")
CHUNK_SIZE = os.environ.get("CHUNK_SIZE", 1000)

# EXPORT ALL KERNEL PARAMS AND METADATA TO JSON FILE FOR COORDINATOR
class PiParams(pd.BaseModel):
    dummy: str = "dumbo" 

class KernelDataSchema(pd.BaseModel):
    job_id: str
    chunk_size: int = CHUNK_SIZE
    kernel: str
    kernel_version: int
    params: dict
    n: int
    entropy: int
    schema_version: int

job_id	job42	Which job this belongs to (used for lease, inflight, and result keys)
chunk_id	7	Which slice of the job. Also the seed input and the dedupe key
kernel	"pi"	Registry lookup name
kernel_version	1	The worker refuses the chunk if its code version doesn't match
params	{} for pi	Validated kernel parameters, passed through untouched
n	250000	Samples in this chunk, not the whole job
entropy	a big integer	The job's base seed. The worker combines it with chunk_id to build the seed
schema_version	1	Version of the message format itself