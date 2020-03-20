class UserScript:
    def __init__(self, id=None):
        self.functions = []
        self._function_by_name = {}
        self.id = id

    def __len__(self):
        return len(self.functions)

    def register(self, func):
        self.functions.append(func)
        self._function_by_name[func.__name__] = func

    def exec(self, index=None, name=None, *args, **kwargs):
        if index is not None:
            return self.functions[index](*args, **kwargs)
        elif name is not None:
            return self._function_by_name[name](*args, **kwargs)
        raise ValueError("index and name are both None")
