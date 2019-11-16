import json


__all__ = ['Config']


class Config:
    """configs JSON wrapper"""
    configs = {}

    def __init__(self):
        self.read()

    def __getattr__(self, key: str):
        return self.configs[key]

    def read(self):
        with open('./config/config.json') as f:
            self.configs = json.load(f)

    def __str__(self):
        return str(self.configs)
