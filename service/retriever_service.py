from service.vector_store_service import VectorStoreService


class RetrieverService:
    def __init__(self, vector_store: VectorStoreService):
        self.vector_store = vector_store
        
    def retrieve_context(self, user_query: str, k: int = 10) -> str:
        """
        Retrieves DDL, Business Rules, and SQL Examples.
        Merges, deduplicates, and formats into optimized context.
        """
        raw_docs = self.vector_store.similarity_search(user_query, k=k)
        
        # Deduplicate based on content
        unique_docs = []
        seen_content = set()
        
        for doc in raw_docs:
            if doc.page_content not in seen_content:
                seen_content.add(doc.page_content)
                unique_docs.append(doc)
                
        # Merge and format
        context_parts = []
        for i, doc in enumerate(unique_docs):
            section = doc.metadata.get('section', 'General')
            context_parts.append(f"--- Context {i+1} ({section}) ---\n{doc.page_content}\n")
            
        return "\n".join(context_parts)
