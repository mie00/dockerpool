import uuid
import threading

from .dockerwrapper import Docker

class Pool:
    def __init__(self, pools, client, container_count, standby_count, args, kwargs):
        self.pools = pools
        self.client = client
        name = (args and args[0]) or kwargs['image']
        self.client.inspect_image(name)
        if (container_count, standby_count) == (None, None):
            container_count = 10
        if container_count is not None and stadby_count is not None:
            raise Excpetion('you can oonly pass one')
        self.container_count = container_count
        self.standby_count = standby_count
        self.args = args
        self.kwargs = kwargs
        self.key = uuid.uuid4()
        self.used_containers = {}
        self.standby_containers = {}

    def __str__(self):
        return 'Pool(%s)'%self.key

    def __eq__(self, other):
        if isinstance(other, Pool):
            return self.args == other.args and self.kwargs == other.kwargs
        elif isinstance(other, dict):
            return self.args == other['args'] and self.kwargs == other['kwargs']

    def _clean(self):
        for container in self.standby_containers.values():
            if not container.is_running:
                contanier._start()

    def ensure(self):
        self._clean()
        if self.container_count is not None:
            n = self.container_count - len(self.used_container) - len(self.standby_containers)
        else:
            n = self.standby_count - len(self.standby_containers)
        if n <= 0:
            return True
        else:
            for i in range(n):
                block = len(self.standby_containers) == 0
                self.create(block=block)

    def create(self, block=False):
        thread = threading.Thread(target=self._create)
        thread.start()
        if block:
            thread.join()
        
    def _create(self):
        container = Docker(self, self.client, self.args, self.kwargs)
        container.__enter__()
        key = container.id
        self.standby_containers[key] = container

    def get(self, key=None):
        if key is None:
            key = next(self.standby_containers.keys().__iter__())
        if key in self.standby_containers:
            self.used_containers[key] = self.standby_containers[key]
            del self.standby_containers[key]

        return self.used_containers[key]

    def destroy(self, key, block=False):
        thread = threading.Thread(target=self._destroy, args=(key,))
        thread.start()
        if block:
            thread.join()

    def _destroy(self, key):
        container = self.get(key)
        del self.used_containers[key]
        container.__exit__()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        for key in list(self.standby_containers.keys()):
            self.destroy(key)
        for key in list(self.used_containers.keys()):
            self.destroy(key)

    def stop(self):
        self.pools.destroy(self.key)
