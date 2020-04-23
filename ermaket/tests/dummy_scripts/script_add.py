from ermaket.api.scripts import ReturnContext, UserScript

__all__ = ['script']

script = UserScript(id=3)


@script.register
def add(context):
    return ReturnContext({"data": "EXAMPLE_DATA"})
