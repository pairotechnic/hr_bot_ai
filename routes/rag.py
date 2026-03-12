# Standard Library Imports
import os

# Third-Party Library Imports
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

# Local Application Imports
from services.ingestion import ingest_document
from services.retrieval import query_rag

rag_bp = Blueprint("rag", __name__, url_prefix="/rag")

UPLOAD_FOLDER = "/tmp/hr_uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@rag_bp.route("/ingest", methods=["POST"])
def ingest():
    if "file" not in request.files:
        return jsonify({"error" : "No file provided"}), 400
    
    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error" : "This file type is not supported at the moment"}), 415
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try :
        doc = ingest_document(file_path, filename)
        return jsonify({"message" : "Document ingested", "document": doc.to_dict()}), 201
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    finally :
        if os.path.exists(file_path):
            os.remove(file_path) # Cleanup temp file

@rag_bp.route("/query", methods=["POST"])
def query():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "question is required"}), 400
    
    try :
        result = query_rag(question)
        return jsonify(result), 200
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500