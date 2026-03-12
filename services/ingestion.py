# Standard Library Imports
import os

# Third-Party Library Imports
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Local Application Imports
from extensions import postgres_db, get_vector_store
from models import HRDocument

ES_INDEX = "hr_documents"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def split_text(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100, # overlap to associate adjacent chunks, and preserve context
        length_function=len
    )
    return splitter.split_text(text)

def ingest_document(file_path: str, filename: str) -> HRDocument:
    try :
        # Step 1 : Extract text
        raw_text = extract_text_from_pdf(file_path)

        # Step 2 : Chunk text
        chunks = split_text(raw_text)

        # Step 3+4 : Generate embeddings + Store in ElasticSearch
        # ElasticsearchStore.add_texts handles embeddings + indexing in one call
        vector_store = get_vector_store()
        es_chunks_metadatas = [{"source" : filename, "chunk_index": i} for i in range(len(chunks))]
        vector_store.add_texts(texts=chunks, metadatas=es_chunks_metadatas)

        # Step 5 : Store file level metadata in PostgreSQL
        doc = HRDocument(
            filename=filename,
            chunk_count=len(chunks),
            es_index=ES_INDEX,
            status="processed"
        )
        postgres_db.session.add(doc)
        postgres_db.session.commit()
        return doc
    except Exception as e:
        postgres_db.session.rollback()
        raise RuntimeError(f"Ingestion failed : {str(e)}")
    
    