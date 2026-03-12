# Standard Library Imports
import os

# Third-Party Library Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Local Application Imports
from extensions import get_vector_store

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-5-nano", api_key=OPENAI_API_KEY, temperature=0)

HR_RAG_PROMPT = ChatPromptTemplate.from_template("""
You are an HR assistant. Answer the employee's question using ONLY the context below. 
If the answer is not in the context, say 'I couldn't find that in the HR documents.'

Context : {context}

Question : {question}
                                        
Answer : 
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def query_rag(question: str, k: int = 5) -> dict:
    try :
        # Step 1+2 : Convert query to embedding + vector search in Elasticsearch
        vector_store = get_vector_store()

        # Step 3+4 : Retrieve top k relevant chunks
        retriever = vector_store.as_retriever(search_kwargs={"k": k})

        # Step 5+6 : Build RAG chain using LCEL (LangChain Expression Language)
        rag_chain = (
            {"context" : retriever | format_docs, "question": RunnablePassthrough()}
            | HR_RAG_PROMPT
            | llm
            | StrOutputParser()
        )

        # Step 7 : Generate and return answer
        answer = rag_chain.invoke(question)

        # Also return source chunks for transparency
        source_docs = retriever.invoke(question)
        sources = list({doc.metadata.get("source", "unknown") for doc in source_docs})

        return {
            "answer" : answer,
            "sources" : sources
        }
    
    except Exception as e:
        raise RuntimeError(f"Retrieval failed : {str(e)}")