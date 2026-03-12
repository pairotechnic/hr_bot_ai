# Standard Library Imports
import json
import os

# Third-Party Library Imports
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# Local Application Imports
from tools.search_tools import duck_duck_go_search_tool, wiki_search_tool
from tools.custom_tools import save_text_to_file_tool
from tools.rag_tools import hr_document_search_tool

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Instantiate the model explicitly — required for reliable tool use
# Do NOT use response_format here: combining tools + structured output in
# LangChain 1.x causes known recursion/conflict issues (ToolStrategy conflict).
llm = ChatOpenAI(
    model="gpt-5-nano", 
    api_key=OPENAI_API_KEY, 
    temperature=0,
    max_retries=2
)

SYSTEM_PROMPT = """
You are an HR automation assistant for an enterprise company.
You help employees with HR-related needs including:
- HR policies, benefits, and procedures (use the hr_document_search_tool)
- Open enrollment, onboarding, leave of absence, compensation questions
- General knowledge or background information (use wiki_search_tool)
- Current events or information not in HR documents (use duck_duck_go_search_tool)
- Saving research summaries when asked (use save_text_to_file_tool)

Decision guide for tool use:
1. If the question is about THIS company's HR policies, benefits, or procedures
   -> Always use hr_document_search_tool first
2. If the question requires general knowledge or definitions
   -> Use wiki_search_tool
3. If the question requires current/recent information
   -> Use duck_duck_go_search_tool
4. If HR documents don't have the answer, say so clearly and suggest contacting HR directly.

Always be professional, empathetic, and concise.
"""

def ask_agent(query):
    try :
        print("entered ask_agent")
        tools = [
            duck_duck_go_search_tool, 
            wiki_search_tool, 
            save_text_to_file_tool,
            hr_document_search_tool
        ]
        agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=SYSTEM_PROMPT
        )

        response = agent.invoke({
            "messages" : [
                {
                    "role" : "user",
                    "content" : query
                }
            ]
        })

        print(json.dumps(response, indent=4, default=dict))

        messages = response.get("messages", [])
        if messages : 
            last_message = messages[-1]
            content = getattr(last_message, "content", None) or last_message.get("content", "")
            return {"response": content}
        
        return {"error": "The agent did not produce a response. Please try again."}
    except Exception as e :
        return {"error": f"Agent failed unexpectedly: {str(e)}"}

    

    