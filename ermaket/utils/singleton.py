__all__ = ['Singleton']


class Singleton(type):
    _instances = {}
    _block = False

    def __call__(cls, *args, **kwargs):
        if cls._block:
            return super(Singleton, cls).__call__(*args, **kwargs)

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset(cls):
        cls._instances = {}

    @classmethod
    def block(cls):
        class Blocked:
            def __enter__(self):
                cls._block = True

            def __exit__(self, type, value, tb):
                cls._block = False

        return Blocked()
