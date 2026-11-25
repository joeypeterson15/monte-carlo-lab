import kernel.registry.KERNELS
import JSON from typing

class Worker():
    def __init__(self, id, lease_exp):
        self.id = f"worker-{id}"

    def run(self, job: JSON):
        raw_job = json.load(job)
        try:
            return KERNELS[raw_job.name(raw_job)]
        except Exception as e:
            raise f"An error occured calling kernel function in worker node: {e}"
        # exit loop? Kill node? Or try grabbing another job? 
        

