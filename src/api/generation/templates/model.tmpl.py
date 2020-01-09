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
    {% for rel in table.primary_rels -%}
    {%- if rel.fk_col is not none %}
    {{ Names.referrer_rel_name(rel.ref_table.name, rel.name) }} = sa.orm.relationship('{{ Names.class_name(schema, rel.ref_table.name) }}', back_populates='{{ Names.referral_rel_name(table.name, rel.name) }}', foreign_keys=[{{ Names.attribute_name(rel.fk_col.name) }}])
    {%- else %}
    {{ Names.referral_rel_name(rel.ref_table.name, rel.name) }} = sa.orm.relationship('{{ Names.class_name(schema, rel.ref_table.name) }}', back_populates='{{ Names.referrer_rel_name(table.name, rel.name) }}')
    {% endif -%}
    {% endfor -%}
    {%- for rel in table.secondary_rels %}
    {{ Names.referrer_rel_name(rel.ref_table.name, rel.name) }} = sa.orm.relationship('{{ Names.class_name(schema, rel.ref_table.name) }}', secondary='{{ schema }}.{{ rel.secondary_table.name }}', back_populates='{{ Names.referrer_rel_name(table.name, rel.name) }}')
    {% endfor -%}
