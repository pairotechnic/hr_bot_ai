# Standard Library Imports
import os

# Third-Party Library Imports
from flask_sqlalchemy import SQLAlchemy
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

# Local Application Imports

# PostgreSQL
postgres_db = SQLAlchemy()

# MongoDB
_mongo_client = None
_mongo_db = None

# ElasticSearch
ES_URL = os.environ.get("ELASTICSEARCH_URL", "http://elasticsearch:9200")
ES_INDEX = "hr_documents"

# OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def get_vector_store():
    return ElasticsearchStore(
        es_url=ES_URL,
        index_name=ES_INDEX,
        embedding=embeddings
    )

def init_mongo():
    global _mongo_client, _mongo_db
    mongo_uri = os.environ.get("MONGO_URI")
    _mongo_client = MongoClient(mongo_uri)
    _mongo_db = _mongo_client.get_default_database()

def get_mongo_db():
    if _mongo_db is None:
        raise RuntimeError("MongoDB has not been initialized. Call init_mongo(app) first.")
    return _mongo_db