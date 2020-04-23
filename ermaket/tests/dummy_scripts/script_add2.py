from ermaket.api.scripts import ReturnContext, UserScript

__all__ = ['script']

script = UserScript(id=4)


@script.register
def add(context):
    return ReturnContext({"data2": "EXAMPLE_DATA2"})
