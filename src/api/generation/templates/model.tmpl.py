import sqlalchemy as sa

from .base import Base

__all__ = ['{{ Names.class_name(schema, table.name) }}']


class {{ Names.class_name(schema, table.name) }}(Base):
    __tablename__ = '{{ table.name }}'
    __table_args__ = {'schema': '{{ schema }}'}

    {% for col in table.columns %}
    {{ Names.attribute_name(col.name) }} = sa.Column(sa.{{ sa_type(col.type_, col.name) }}, primary_key={{ col.pk }}, nullable={{ not col.not_null }}, unique={{ col.unique }}, autoincrement={{ col.auto_inc }})
    {%- endfor %}
    {% for col in table.foreign_keys %}
    {{ Names.attribute_name(col.name) }} = sa.Column(sa.{{ sa_type(col.type_, col.name) }}, sa.ForeignKey('{{ schema }}.{{ col.fk.table.name }}.{{ col.fk.column.name }}', ondelete='{{ col.fk.ondelete }}', onupdate='{{ col.fk.onupdate }}'), primary_key={{ col.pk }}, unique={{ col.unique }})
    {%- endfor %}
    {% for col in table.foreign_keys %}
    {%- if col.fk.add_backref %}
    {{ Names.rel_name(col.fk.table.name, col.fk.relation_name) }} = sa.orm.relationship('{{ Names.class_name(schema, col.fk.table.name) }}', backref='{{ Names.backref_name(table.name, col.fk.relation_name) }}', foreign_keys=[{{ Names.attribute_name(col.name) }}])
    {% endif -%}
    {%- endfor %}
    {%- for sec in table.secondary %}
    {{ Names.rel_name(sec.backref_table.name, sec.relation_name) }} = sa.orm.relationship('{{ Names.class_name(schema, sec.backref_table.name) }}', secondary='{{ schema }}.{{ sec.link_table.name }}', backref='{{ Names.rel_name(sec.ref_table.name, sec.relation_name) }}')
    {%- endfor -%}
