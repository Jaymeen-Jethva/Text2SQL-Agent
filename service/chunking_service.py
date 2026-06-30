from langchain_core.documents import Document
from models.semantic_layer import SemanticLayer

class ChunkingService:
    def __init__(self, semantic_layer: SemanticLayer, ddl: dict, db_name: str):
        self.semantic_layer = semantic_layer
        self.ddl = ddl
        self.db_name = db_name
        
    def generate_chunks(self) -> list[Document]:
        chunks = []
        chunk_id = 0
        
        # 1. DDL Chunks
        for table, schema in self.ddl.items():
            chunks.append(Document(
                page_content=f"CREATE TABLE statement for {table}:\n{schema}",
                metadata={
                    "database": self.db_name,
                    "table": table,
                    "section": "DDL",
                    "chunk_id": f"chunk_{chunk_id}",
                    "source": f"{table}_ddl"
                }
            ))
            chunk_id += 1
            
        # 2. Documentation Chunks (Entities)
        for entity in self.semantic_layer.entities:
            doc_lines = [f"Table: {entity.table_name}"]
            doc_lines.append(f"Primary Key: {entity.primary_key}")
            doc_lines.append("Dimensions:")
            for dim in entity.dimensions:
                doc_lines.append(f"- {dim.column}: {dim.description}")
            doc_lines.append("Measures:")
            for meas in entity.measures:
                doc_lines.append(f"- {meas.column}: {meas.description} (Agg: {meas.aggregation})")
            
            chunks.append(Document(
                page_content="\n".join(doc_lines),
                metadata={
                    "database": self.db_name,
                    "table": entity.table_name,
                    "section": "Documentation",
                    "chunk_id": f"chunk_{chunk_id}",
                    "source": f"{entity.table_name}_doc"
                }
            ))
            chunk_id += 1
            
        # 3. Joins
        if self.semantic_layer.joins:
            join_text = "Join Relationships:\n" + "\n".join([f"- {j.source_table}.{j.source_column} -> {j.target_table}.{j.target_column}" for j in self.semantic_layer.joins])
            chunks.append(Document(
                page_content=join_text,
                metadata={
                    "database": self.db_name,
                    "table": "all",
                    "section": "Documentation",
                    "chunk_id": f"chunk_{chunk_id}",
                    "source": "joins_doc"
                }
            ))
            chunk_id += 1

        # 4. Rules and KPIs
        rules_text = "Business Rules & KPIs:\n" + "\n".join(self.semantic_layer.business_rules + self.semantic_layer.kpis)
        chunks.append(Document(
            page_content=rules_text,
            metadata={
                "database": self.db_name,
                "table": "all",
                "section": "Documentation",
                "chunk_id": f"chunk_{chunk_id}",
                "source": "rules_doc"
            }
        ))
        chunk_id += 1
            
        # 5. SQL Examples
        for idx, sql in enumerate(self.semantic_layer.sql_examples):
            chunks.append(Document(
                page_content=f"SQL Example:\n{sql}",
                metadata={
                    "database": self.db_name,
                    "table": "all",
                    "section": "SQL Examples",
                    "chunk_id": f"chunk_{chunk_id}",
                    "source": f"sql_example_{idx}"
                }
            ))
            chunk_id += 1
            
        return chunks
