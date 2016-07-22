from .pools import Pools

if __name__ == "__main__":
    with Pools() as p:
        import IPython
        IPython.embed()
