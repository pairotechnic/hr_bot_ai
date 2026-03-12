# Standard Library Imports
from datetime import datetime, timezone

# Third-Party Library Imports
from langchain_core.messages import HumanMessage, AIMessage

# Local Application Imports
from extensions import get_mongo_db

COLLECTION = "conversations"

def load_history(session_id: str) -> list:
    """Load conversation history as LangChain message objects."""

    mongo_db = get_mongo_db()
    doc = mongo_db[COLLECTION].find_one({"session_id": session_id})
    if not doc :
        print(f"No history found for this conversation. session_id : {session_id}")
        return []
    
    messages = []
    for m in doc.get("messages", []):
        if m["role"] == "human":
            messages.append(HumanMessage(content=m["content"]))
        elif m["role"] == "ai":
            messages.append(AIMessage(content=m["content"]))
    return messages

def save_turn(session_id: str, employee_id: int, human_message: str, ai_response: str):
    """Append a Human+AI turn to the conversation history"""
    turn = [
        {"role" : "human", "content": human_message, "timestamp": datetime.now(timezone.utc)},
        {"role" : "ai", "content": ai_response, "timestamp": datetime.now(timezone.utc)},
    ]
    mongo_db = get_mongo_db()
    mongo_db[COLLECTION].update_one(
        {"session_id": session_id},
        {
            "$push": {"messages": {"$each": turn}},
            "$set": {"employee_id": employee_id, "last_updated": datetime.now(timezone.utc)},
            "$setOnInsert": {"$created": datetime.now(timezone.utc)}
        },
        upsert=True
    )


def clear_session(session_id: str):
    """Clear history for a session (eg: employee explicitly starts over)"""
    mongo_db = get_mongo_db()
    mongo_db[COLLECTION].delete_one({"session_id": session_id})