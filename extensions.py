# Standard Library Imports
import os

# Third-Party Library Imports
from flask_sqlalchemy import SQLAlchemy
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings

# Local Application Imports

db = SQLAlchemy()

ES_URL = os.environ.get("ELASTICSEARCH_URL", "http://elasticsearch:9200")
ES_INDEX = "hr_documents"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def get_vector_store():
    return ElasticsearchStore(
        es_url=ES_URL,
        index_name=ES_INDEX,
        embedding=embeddings
    )