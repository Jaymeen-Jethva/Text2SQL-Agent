from pydantic import BaseModel


class Dimension(BaseModel):
    name: str
    column: str
    description: str


class Measure(BaseModel):
    name: str
    column: str
    aggregation: str
    description: str


class Entity(BaseModel):
    table_name: str
    primary_key: str | None
    dimensions: list[Dimension]
    measures: list[Measure]
    date_rules: list[str]
    filter_rules: list[str]


class JoinRelationship(BaseModel):
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    relationship_type: str


class SemanticLayer(BaseModel):
    entities: list[Entity]
    joins: list[JoinRelationship]
    business_rules: list[str]
    kpis: list[str]
    currency_rules: list[str]
    data_quality_notes: list[str]
    sql_examples: list[str]
