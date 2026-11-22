import kernel.registry.KERNELS
import JSON from typing

class Worker():
    def __init__(self, id, lease_exp):
        self.id = f"worker-{id}"
        self.active = False
        self.lease_exp = lease_exp

    def run(self, job: JSON):
        kernel_name, chunk, payload = json.load(job)
        try:
            return KERNELS[name(params)]
        except Exception as e:
            raise f"An error occured calling kernel function in worker node: {e}"
        # exit loop? Kill node? Or try grabbing another job? 
        

