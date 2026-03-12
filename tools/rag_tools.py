# Standard Library Imports

# Third-Party Library Imports
from langchain.tools import tool

# Local Application Imports
from services.retrieval import query_rag

@tool
def hr_document_search_tool(question: str) -> str:
    """
    Search the company's internal HR documents for policies, procedures, benefits,
    onboarding guides, leave of absence rules, compensation details, open enrollment
    information, and any other HR-related content.
    Use this tool when the employee's question is about internal HR policies or 
    company-specific procedures. Do NOT use this for general knowledge questions.
    """
    print("entered hr_document_search_tool")
    try :
        result = query_rag(question)
        answer = result.get("answer", "No answer found in HR documents")
        sources = result.get("sources", [])
        if sources:
            sources_list = ", ".join(sources)
            return f"{answer}\n\n(Sources : {sources_list})"
        return answer
    except RuntimeError as e:
        return f"HR document search failed: {str(e)}"