# Standard Library Imports

# Third-Party Library Imports
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool

# Local Application Imports

duck_duck_go_search = DuckDuckGoSearchRun()

@tool
def duck_duck_go_search_tool(query: str) -> str:
    """Search the web for information using Duck Duck Go API"""
    return duck_duck_go_search.run(query)

wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=1000)
wiki_search_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)