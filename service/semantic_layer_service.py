from pathlib import Path
from models.semantic_layer import (
    SemanticLayer, Entity, Dimension, Measure, JoinRelationship
)
from models.column_profile import TableProfile
from service.ddl_service import DDLService


class SemanticLayerService:
    def __init__(self, db_path: Path, profiles: list[TableProfile]):
        self.db_path = db_path
        self.profiles = profiles
        self.ddl_service = DDLService(db_path)

    def generate(self) -> SemanticLayer:
        entities = []
        joins = []
        business_rules = []
        kpis = []
        currency_rules = []
        data_quality_notes = []
        sql_examples = []

        for profile in self.profiles:
            table_name = profile.table_name
            dimensions = []
            measures = []
            date_rules = []
            filter_rules = []
            primary_key = None

            # Get DB metadata for foreign keys
            meta = self.ddl_service.get_table_metadata(table_name)
            for fk in meta["foreign_keys"]:
                # fk tuple: (id, seq, table, from, to, on_update, on_delete, match)
                target_table = fk[2]
                source_column = fk[3]
                target_column = fk[4]
                joins.append(JoinRelationship(
                    source_table=table_name,
                    source_column=source_column,
                    target_table=target_table,
                    target_column=target_column,
                    relationship_type="N:1" # Standard FK assumption
                ))

            for col in profile.columns:
                if col.primary_key:
                    primary_key = col.column_name

                # Infer Dimensions
                if col.is_categorical or col.is_boolean or col.is_identifier or col.semantic_type in ["TEXT", "DATE", "EMAIL", "PHONE"]:
                    dimensions.append(Dimension(
                        name=col.column_name.replace("_", " ").title(),
                        column=col.column_name,
                        description=f"{col.semantic_type} dimension for {col.column_name}"
                    ))

                # Infer Measures
                if col.semantic_type in ["INTEGER", "FLOAT", "CURRENCY", "PERCENTAGE"] and not col.is_identifier:
                    agg = "SUM" if col.semantic_type in ["CURRENCY", "INTEGER", "FLOAT"] else "AVG"
                    measures.append(Measure(
                        name=f"Total {col.column_name.replace('_', ' ').title()}",
                        column=col.column_name,
                        aggregation=agg,
                        description=f"Aggregated {col.column_name}"
                    ))
                    if col.semantic_type == "CURRENCY":
                        currency_rules.append(f"Always format {col.column_name} as currency.")

                # Date Rules
                if col.is_date:
                    date_rules.append(f"Can group by Year, Month, Day using {col.column_name}.")

                # Data Quality
                if col.null_count > 0:
                    pct_null = (col.null_count / profile.row_count) * 100 if profile.row_count else 0
                    if pct_null > 20:
                        data_quality_notes.append(f"{table_name}.{col.column_name} has {pct_null:.1f}% NULL values. Handle with COALESCE or IS NOT NULL.")

            # Create default KPI for the table
            kpis.append(f"Total count of {table_name}: SELECT COUNT(*) FROM {table_name}")
            sql_examples.append(f"SELECT * FROM {table_name} LIMIT 5;")

            entity = Entity(
                table_name=table_name,
                primary_key=primary_key,
                dimensions=dimensions,
                measures=measures,
                date_rules=date_rules,
                filter_rules=filter_rules
            )
            entities.append(entity)

        business_rules.append("Prefer INNER JOIN unless explicitly looking for missing records.")
        business_rules.append("Use aliases for all table names in queries.")

        return SemanticLayer(
            entities=entities,
            joins=joins,
            business_rules=business_rules,
            kpis=kpis,
            currency_rules=currency_rules,
            data_quality_notes=data_quality_notes,
            sql_examples=sql_examples
        )
