from pathlib import Path
from models.semantic_layer import SemanticLayer


class TrainingDocumentService:
    def __init__(self, semantic_layer: SemanticLayer, ddl: dict):
        self.semantic_layer = semantic_layer
        self.ddl = ddl
        
    def generate_document(self) -> str:
        doc = ["# Text2SQL Training Document\n"]
        
        doc.append("## Database Schema\n")
        for table, schema in self.ddl.items():
            doc.append(f"### {table}")
            doc.append(f"```sql\n{schema}\n```\n")
            
        doc.append("## Business Documentation\n")
        doc.append("### Entities")
        for entity in self.semantic_layer.entities:
            doc.append(f"**{entity.table_name}**")
            if entity.primary_key:
                doc.append(f"- Primary Key: {entity.primary_key}")
            doc.append("- Dimensions:")
            for dim in entity.dimensions:
                doc.append(f"  - {dim.column}: {dim.description}")
            doc.append("- Measures:")
            for meas in entity.measures:
                doc.append(f"  - {meas.column}: {meas.description} (Agg: {meas.aggregation})")
            if entity.date_rules:
                doc.append("- Date Rules:")
                for rule in entity.date_rules:
                    doc.append(f"  - {rule}")
            doc.append("")
            
        if self.semantic_layer.joins:
            doc.append("### Join Relationships")
            for join in self.semantic_layer.joins:
                doc.append(f"- {join.source_table}.{join.source_column} -> {join.target_table}.{join.target_column} ({join.relationship_type})")
            doc.append("")
            
        doc.append("### Rules and KPIs")
        for rule in self.semantic_layer.business_rules:
            doc.append(f"- {rule}")
        for kpi in self.semantic_layer.kpis:
            doc.append(f"- KPI: {kpi}")
        for note in self.semantic_layer.data_quality_notes:
            doc.append(f"- Quality Note: {note}")
        doc.append("")
            
        doc.append("## SQL Examples\n")
        for sql in self.semantic_layer.sql_examples:
            doc.append(f"```sql\n{sql}\n```\n")
            
        return "\n".join(doc)
        
    def save_document(self, output_path: Path) -> Path:
        doc = self.generate_document()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(doc)
        return output_path
