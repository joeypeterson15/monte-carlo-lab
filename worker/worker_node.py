import kernel.registry.KERNELS

class Worker():
    def __init__(self):
        self.isBusy = False
        self.lease_time = 15

    def run(self, name, version, params):
        try:
            return KERNELS[name(version, params)]
        except Exception as e:
            raise f"An error occured calling kernel function in worker node: {e}"
        # exit loop? Kill node? Or try grabbing another job? 
        

