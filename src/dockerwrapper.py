class Docker:
    def __init__(self, pool, client, args, kwargs):
        self.pool = pool
        self.client = client
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        self.id = self.client.create_container(*self.args, command='/bin/sleep {s}'.format(s=10000000), **self.kwargs)['Id']
        self._start()
        return self

    def _start(self):
        self.client.start(self.id)

    def _stop(self):
        self.client.stop(self.id)

    def stop(self):
        self.pool.destroy(self.id)

    def __exit__(self, *args, **kwargs):
        self._stop()
        self.client.remove_container(self.id, v=True)
        return self

    @property
    def is_running(self):
        return self.client.inspect_container(self.id)['State']['Running']

    def execute(self, cmd, stdout=True, stderr=True, stream=False):
        if not self.is_running:
            self._start()
        cmd2 = self.client.exec_create(self.id, cmd, stdout=stdout, stderr=stderr)['Id']
        r = self.client.exec_start(cmd2, stream=stream)
        return r
