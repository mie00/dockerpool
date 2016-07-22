from docker import Client

from .gc import GC
from .pool import Pool

class Pools:
    def __init__(self, client='unix://var/run/docker.sock'):
        self.pools = {}
        self.client = Client(base_url=client)
        self.gc = GC(self)
        self.gc.start()

    def ensure(self):
        for pool in self.pools.values():
            pool.ensure()

    def create(self, *args, **kwargs):
        container_count = kwargs.pop('container_count', None)
        standby_count = kwargs.pop('standby_count', None)
        if container_count == standby_count == None:
            standby_count = 1
        p = {'args': args, 'kwargs': kwargs}
        for k, v in self.pools.items():
            if v == p:
                if v.container_count == container_count and v.standby_count == standby_count:
                    return k
                else:
                    raise Exception('the pool does exist')

        new_pool = Pool(self, self.client, container_count, standby_count, args, kwargs)
        key = new_pool.key
        self.pools[key] = new_pool
        self.ensure()
        return key

    def get(self, key):
        return self.pools[key]

    def destroy(self, key):
        p = self.pools[key]
        p.__exit__()
        del self.pools[key]

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.gc.enabled = False
        self.gc.join()
        for key in list(self.pools.keys()):
            self.destroy(key)
