# Standard Library Imports
import json

# Third-Party Library Imports
from langchain.agents import create_agent
from pydantic import BaseModel

# Local Application Imports
from tools.search_tools import duck_duck_go_search_tool, wiki_search_tool
from tools.custom_tools import save_text_to_file_tool

model = "gpt-5-nano"

class ResponseFormat(BaseModel):
    query: str
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

def ask_agent(query):
    tools = [duck_duck_go_search_tool, wiki_search_tool, save_text_to_file_tool]
    agent = create_agent(
        model=model,
        tools=tools,
        response_format=ResponseFormat,
        # TODO : Update this prompt to reflect the intended behaviour of the agent
        system_prompt="""
            You are an HR automation bot.
            You automate critical HR functions, including support, open enrollment, onboarding, leave of absence, compensation.
            You execute processes and workflows, streamline HR operations, and deliver employees the help they need instantly and conversationally
            Answer the user query and use necessary tools.
        """
    )
    
    stream = agent.stream(
        {
            "messages" : [
                {
                    "role" : "user",
                    "content" : query
                }
            ]
        },
        stream_mode = "updates"
    )

    final_structured_response = None

    for step in stream:
        print("\n--- AGENT STEP ---")
        print(json.dumps(step, indent=4, default=str))

        # capture final structured output
        if "structured_response" in step.get("model", {}):
            final_structured_response = step["model"]["structured_response"]

    if final_structured_response is None :
        return {"error" : "Sorry, I can't help you with that right now"}
    
    if isinstance(final_structured_response, ResponseFormat):
        print("\n--- FINAL STRUCTURED RESPONSE ---")
        print(final_structured_response)
        return final_structured_response.model_dump()

    # If some format other than ResponseFormat Pydantic BaseModel, return as-is
    return final_structured_response

    # response = agent.invoke({
    #     "messages" : [
    #         {
    #             "role" : "user",
    #             "content" : query
    #         }
    #     ]
    # })

    # print(json.dumps(response["structured_response"], indent=4, default=dict))