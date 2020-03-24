__all__ = ['UserScript']


class UserScript:
    def __init__(self, id=None, activations=None):
        self.functions = []
        self._function_by_name = {}
        self.id = id
        self.activations = [] if activations is None else activations

    def __len__(self):
        return len(self.functions)

    def __getitem__(self, index):
        return self.functions[index]

    def register(self, func):
        self.functions.append(func)
        self._function_by_name[func.__name__] = func

    def exec(self, index=None, name=None, *args, **kwargs):
        if index is not None:
            return self.functions[index](*args, **kwargs)
        elif name is not None:
            return self._function_by_name[name](*args, **kwargs)
        raise ValueError("index and name are both None")
