import sqlalchemy as sa

from models.base import Base

__all__ = ['{{ Names.class_name(schema, table.name) }}']


class {{ Names.class_name(schema, table.name) }}(Base):
    __tablename__ = '{{ table.name }}'
    __table_args__ = {'schema': '{{ schema }}'}

    {% for col in table.columns %}
    {{ Names.attribute_name(col.name) }} = sa.Column(sa.{{ sa_type(col.type_) }}, primary_key={{ col.pk }}, nullable={{ not col.not_null }}, unique={{ col.unique }}, autoincrement={{ col.auto_inc }})
    {% endfor %}
