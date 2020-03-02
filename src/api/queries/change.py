

class Transaction:
    def __init__(self, session, params):
        self._session = session
        self._params = params

    def execute(self):
        print(self._params)
