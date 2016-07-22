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

## License

This package is licensed under [GPL](LICENSE)
Copyright © 2016 [Mohamed Elawadi](https://github.com/mie00)
