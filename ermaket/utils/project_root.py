from pathlib import Path

__all__ = ['get_project_root']


def get_project_root():
    return Path(__file__).parent.parent
