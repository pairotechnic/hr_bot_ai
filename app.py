from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQL_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = "employee"
    
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), unique=True) # Add Nullable = False later during Migration
    company     = db.Column(db.String(100))

    def __repr__(self):
        return f"<Employee {self.name}>"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/employee", methods=["GET"])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([
        {
            "id": e.id,
            "name": e.name,
            "email": e.email,
            "company": e.company
        } for e in employees
    ]), 200

@app.route("/employee", methods=["POST"])
def add_employee():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    email = data.get("email", "")
    company = data.get("company", "")

    if not name :
        return jsonify({"error": "name is required"}), 400
    elif not email :
        return jsonify({"error": "email is required"}), 400
    
    # Later we will add input validation for company as well, when testing migration
    
    employee = Employee(name=name, email=email, company=company) 
    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "company": employee.company
    }), 201

@app.route("/employee/<int:id>", methods=["GET"])
def get_employee_by_id(id):
    employee = Employee.query.get_or_404(id)
    
    return jsonify({
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "company": employee.company
    }), 200

@app.route("/employee/<int:id>", methods=["PUT"])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    name = data.get("name", "")
    email = data.get("email", "")
    company = data.get("company", "")

    if not name :
        return jsonify({"error": "name is required"}), 400
    elif not email :
        return jsonify({"error": "email is required"}), 400
    
    # Later we will add input validation for company as well, when testing migration
    
    employee.name = name
    employee.email = email
    employee.company = company

    db.session.commit()
    return jsonify({
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "company": employee.company
    }), 200

@app.route("/employee/<int:id>", methods=["PATCH"])
def partial_update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    # Only update fields that were actually sent
    if "name" in data:
        employee.name = data["name"]
    if "email" in data:
        employee.email = data["email"]
    if "company" in data:
        employee.company = data["company"]

    db.session.commit()
    return jsonify({
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "company": employee.company
    }), 200

@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({
        "message": f"Employee {id} deleted"
    }), 200


def main():
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Tables created...")
    
    # Run the flask app
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()