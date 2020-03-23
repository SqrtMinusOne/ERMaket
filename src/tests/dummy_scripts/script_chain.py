import random

from api.scripts import Context, ReturnContext, UserScript

__all__ = ['chain']

chain = UserScript(id=1)
data = None


@chain.register
def step_1(context: Context):
    global data
    context.exec_data['data'] = random.randint(0, 100000)
    data = context.exec_data['data']
    return ReturnContext()


@chain.register
def step_2(context: Context):
    global data
    if context.exec_data['data'] == data:
        return ReturnContext()
    return ReturnContext(abort=500)
