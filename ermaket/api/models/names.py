import stringcase

__all__ = ['NamesConverter']

SYSTEM = 'system'


class NamesConverter:
    @staticmethod
    def db_table_to_class(table_name):
        """DB table name (schema.table_name) to class name

        :param table_name:
        """
        return stringcase.pascalcase(table_name.split('.')[1])

    @staticmethod
    def class_name(schema, entity_name):
        if schema == SYSTEM:
            return stringcase.pascalcase(entity_name)
        return stringcase.pascalcase(schema + '_' +
                                     entity_name).replace('_', '')

    @staticmethod
    def table_name(entity_name):
        return stringcase.snakecase(stringcase.camelcase(entity_name))

    @staticmethod
    def attribute_name(name):
        name = name.replace(' ', '_')
        return stringcase.snakecase(stringcase.camelcase(name))

    @staticmethod
    def fk_name(table, column):
        return NamesConverter.attribute_name(table + '_' + column)

    @staticmethod
    def referral_rel_name(table, relation_name):
        return NamesConverter.attribute_name(table + '_' + relation_name)

    @staticmethod
    def referrer_rel_name(table, relation_name):
        return NamesConverter.attribute_name(relation_name + '_' + table)
