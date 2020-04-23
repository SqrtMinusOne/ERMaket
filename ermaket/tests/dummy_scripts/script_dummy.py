from ermaket.api.scripts import UserScript

__all__ = ['dummy']

dummy = UserScript(id=101)


@dummy.register
def dummy1():
    return 'dummy1'


@dummy.register
def dummy2():
    return 'dummy2'
