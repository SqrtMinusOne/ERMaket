import re

from ermaket.api.erd import ModelError

__all__ = ['erd_to_sqla_type']


def erd_to_sqla_type(type_, *args, **kwargs):
    conv = {
        'array': 'ARRAY(sa.String())',  # TODO
        'boolean': 'Boolean()',
        'float8': 'Float()',  # TODO
        'float4': 'Float()',
        'date': 'Date()',
        'json': 'JSON()',
        'int8': 'BigInteger()',
        'int4': 'Integer()',
        'int2': 'SmallInteger()',
        'time': 'Time()',
        'text': 'Text()',
        'timestamp': 'DateTime()'
    }
    try:
        return conv[type_]
    except KeyError:
        return _complex_types(type_, *args, **kwargs)


def _complex_types(type_, name):
    if re.match(r'varchar\([0-9]{1,7}\)', type_):
        n = int(type_[8:-1])
        return f'String({n})'
    if re.match(r'decimal\([0-9]{1,10}(,( )*[0-9]{1,10})?\)', type_):
        n = type_[8:-1]
        return f'Numeric({n})'
    if re.match(r'enum\(( |\'[ \S]*\'(,)?)+\)', type_):
        return f"Enum({type_[5:-1]}, name='{name}')"
    raise ModelError(f'Unknown type: {type_}')
