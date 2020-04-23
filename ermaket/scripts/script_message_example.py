from ermaket.api.scripts import ReturnContext, UserScript

__all__ = ['script']

script = UserScript(id=0, activations=['login'])


@script.register
def send_message(context):
    ctx = ReturnContext()
    ctx.add_message("I'm the reason for this days behaviour")
    ctx.add_message(
        "This is a message sent by a business logic script",
        variant="secondary"
    )
    return ctx
