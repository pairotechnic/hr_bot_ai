from extensions import db

class Employee(db.Model):
    __tablename__ = "employee"
    
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), unique=True) # Add Nullable = False later during Migration
    company     = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "email" : self.email,
            "company" : self.company
        }

    def __repr__(self):
        return f"<Employee {self.name}>"