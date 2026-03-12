from flask import Blueprint, request, jsonify
from services.agent import ask_agent

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("", methods=["POST"])
def chat():
    print("/chat triggerred")
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message :
        return jsonify({"error": "message is required"}), 400
    
    response = ask_agent(message)
    if "error" in response:
        return jsonify(response), 500
    return jsonify(response), 200