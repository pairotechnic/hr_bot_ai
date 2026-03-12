# Standard Library Imports

# Third-Party Library Imports
from flask import Blueprint, request, jsonify

# Local Application Imports
from services.agent import ask_agent
from services.conversation import load_history, save_turn


chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("", methods=["POST"])
def chat():
    print("/chat triggerred")
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "").strip() # Conversation ID in Teams/Slack etc
    employee_id = data.get("employee_id", "").strip() # From Teams/Slack user profile

    if not message :
        return jsonify({"error": "message is required"}), 400
    if not session_id :
        return jsonify({"error": "session_id is required"}), 400
    
    # Load prior history from Mongo DB
    history = load_history(session_id)

    # Run agent with full context
    response = ask_agent(message, history=history)
    if "error" in response:
        return jsonify(response), 500
    
    # Persist this exchange (turn) to MongoDB
    save_turn(
        session_id=session_id,
        employee_id=employee_id,
        human_message=message,
        ai_response=response["response"]
    )
    return jsonify(response), 200