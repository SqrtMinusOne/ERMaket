from ermaket.api.scripts import ReturnContext, UserScript

__all__ = ['script']

script = UserScript(id=1)


@script.register
def step_1(context):
    ctx = ReturnContext(abort=418)
    ctx.add_message("Sorry, this won't work", variant="danger")
    return ctx
