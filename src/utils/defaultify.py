from collections.abc import Callable

__all__ = ['defaultify_init']


def make_init(class_, root_kwargs):
    def __init__(self, *args, **kwargs):
        class_.__init__(self, *args, **kwargs)
        for key, value in root_kwargs.items():
            if getattr(self, key) is None:
                if isinstance(value, Callable):
                    setattr(self, key, value(self))
                else:
                    setattr(self, key, value)

    return __init__


def defaultify_init(class_, classname, **kwargs):
    return type(
        classname, (class_, ), {
            "__init__": make_init(class_, kwargs),
        }
    )
