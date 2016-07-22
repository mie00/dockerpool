from time import sleep
import threading

class GC(threading.Thread):
    def __init__(self, pools):
        super().__init__()
        self.pools = pools
        self.enabled = True
    def run(self):
        while self.enabled:
            self.pools.ensure()
            sleep(10)
