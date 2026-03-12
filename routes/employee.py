from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from extensions import postgres_db
from models import Employee

employee_bp = Blueprint("employee", __name__, url_prefix="/employee")

@employee_bp.route("", methods=["GET"])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([e.to_dict() for e in employees]), 200

@employee_bp.route("/<int:id>", methods=["GET"])
def get_employee_by_id(id):
    employee = Employee.query.get_or_404(id)
    
    return jsonify(employee.to_dict()), 200

@employee_bp.route("", methods=["POST"])
def add_employee():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    company = data.get("company", "").strip()

    if not name :
        return jsonify({"error": "name is required"}), 400
    elif not email :
        return jsonify({"error": "email is required"}), 400
    
    # Later we will add input validation for company as well, when testing migration
    
    employee = Employee(name=name, email=email, company=company) 
    postgres_db.session.add(employee)

    try :
        postgres_db.session.commit()
    except IntegrityError :
        postgres_db.session.rollback()
        return jsonify({"error" : "email already exists"}), 409

    return jsonify(employee.to_dict()), 201

@employee_bp.route("/<int:id>", methods=["PUT"])
def update_employee(id):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json(silent=True) or {}
    

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    company = data.get("company", "").strip()

    if not name :
        return jsonify({"error": "name is required"}), 400
    elif not email :
        return jsonify({"error": "email is required"}), 400
    
    # Later we will add input validation for company as well, when testing migration
    
    employee = Employee.query.get_or_404(id)
    employee.name = name
    employee.email = email
    employee.company = company

    try :
        postgres_db.session.commit()
    except IntegrityError :
        postgres_db.session.rollback()
        return jsonify({"error" : "email already exists"}), 409
    
    return jsonify(employee.to_dict()), 200

@employee_bp.route("/<int:id>", methods=["PATCH"])
def partial_update_employee(id):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    data = request.get_json(silent=True) or {}

    employee = Employee.query.get_or_404(id)
    # Only update fields that were actually sent
    if "name" in data:
        employee.name = data["name"].strip()
    if "email" in data:
        employee.email = data["email"].strip()
    if "company" in data:
        employee.company = data["company"].strip()

    try :
        postgres_db.session.commit()
    except IntegrityError :
        postgres_db.session.rollback()
        return jsonify({"error" : "email already exists"}), 409
    
    return jsonify(employee.to_dict()), 200

@employee_bp.route("/<int:id>", methods=["DELETE"])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    postgres_db.session.delete(employee)
    postgres_db.session.commit()
    return jsonify({
        "message": f"Employee {id} deleted"
    }), 200