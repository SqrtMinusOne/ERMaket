import re

from api.erd import ModelError

__all__ = ['erd_to_sqla_type']


def erd_to_sqla_type(type_):
    conv = {
        'boolean': 'Boolean()',
        'float8': 'Float()',  # TODO
        'float4': 'Float()',
        'date': 'Date()',
        'json': 'JSON()',
        'int8': 'BigInteger()',
        'int4': 'Integer()',
        'int2': 'SmallInteger()',
        'time': 'Time()',
        'text': 'Text()'
    }
    try:
        return conv[type_]
    except KeyError:
        return _complex_types(type_)


def _complex_types(type_):
    if re.match(r'varchar\([0-9]{1,7}\)', type_):
        n = int(type_[8:-1])
        return f'String({n})'
    if re.match(r'decimal\([0-9]{1,10}(,( )*[0-9]{1,10})?\)', type_):
        n = type_[8:-1]
        return f'Numeric({n})'
    if re.match(r'enum\(( |\'[ \S]*\'(,)?)+\)', type_):
        return f'Enum({type_[5:-1]})'
    raise ModelError(f'Unknown type: {type_}')
