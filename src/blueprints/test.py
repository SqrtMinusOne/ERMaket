from flask import Blueprint

__all__ = ['test']
test = Blueprint('test', 'test')


@test.route('/')
def hello_world():
    return '<body>Hello, World!</body>'
