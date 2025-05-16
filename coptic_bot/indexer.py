from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import PreProcessor, EmbeddingRetriever
from haystack.schema import Document
import os
import nltk

nltk.download('punkt')

WEB_DATA_DIR = "data/web_data"

# Load documents
all_docs = []
for fname in os.listdir(WEB_DATA_DIR):
    with open(os.path.join(WEB_DATA_DIR, fname), "r", encoding="utf-8") as f:
        content = f.read()
        all_docs.append(Document(content=content, meta={"source_file": fname}))

# 1. Initialize FAISS document store
document_store = FAISSDocumentStore(
    faiss_index_factory_str="Flat",   # You can change to "HNSW", "IVF10,PQ", etc.
    sql_url="sqlite:///models/faiss_document_store.db",  # For persistence
    embedding_dim=384
)

# 2. Preprocess text
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    split_by="word",
    split_length=200,
    split_respect_sentence_boundary=True
)
processed_docs = preprocessor.process(all_docs)
document_store.write_documents(processed_docs)

# 3. Initialize retriever
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    use_gpu=True
)

# 4. Update document embeddings
document_store.update_embeddings(retriever)

# 5. Save FAISS index and metadata
document_store.save(index_path="models/faiss_index.faiss")
print("FAISS document store with embeddings saved.")
