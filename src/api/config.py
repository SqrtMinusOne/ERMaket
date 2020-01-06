import json


__all__ = ['Config']


_configs = {}


class Config:
    """configs JSON wrapper"""
    configs = {}

    def __init__(self, reload=False):
        self.read(reload)

    def __getattr__(self, key: str):
        return self.configs[key]

    def read(self, reload):
        global _configs
        if len(_configs) == 0 or reload:
            with open('./config/config.json') as f:
                _configs = json.load(f)
        self.configs = _configs

    def __str__(self):
        return str(self.configs)
