# Docker Pool

A python package to create poolsof docker containers, and execute commands on them.

## Example

```py
from dockerpool import Pool
with Pools() as pools:
    pool_key = pools.create('python:2.7')
    pool = pools.get(pool_key)
    # the next two statements work instantaneously
    container = pool.get()
    container.execute('''python -c 'print "Hello World"' ''') # Hello World
```

## Installation

until now :)

```bash
git clone https://github.com/mie00/dockerpool
```

## TODO

* Restful API.
* [Python client](https://github.com/mie00/dockerpool-client)
* Integration with docker swarm.
* Falure handling.
* Packaging.
* Separation of stdin, stdout for execute method of a container.
* Retrieval of the return code of a process in exec.
* Better threading in the code.
* Raising custom exception.
* Resource management.
* Better control over the number of containers in a pool.
* Dynamic port binding for the containers in the pool.

## License

This package is licensed under [GPL](LICENSE)

Copyright © 2016 [Mohamed Elawadi](https://github.com/mie00)
