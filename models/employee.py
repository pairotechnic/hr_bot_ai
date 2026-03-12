from extensions import postgres_db

class Employee(postgres_db.Model):
    __tablename__ = "employee"
    
    id          = postgres_db.Column(postgres_db.Integer, primary_key=True)
    name        = postgres_db.Column(postgres_db.String(100), nullable=False)
    email       = postgres_db.Column(postgres_db.String(120), unique=True) # Add Nullable = False later during Migration
    company     = postgres_db.Column(postgres_db.String(100))

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "email" : self.email,
            "company" : self.company
        }

    def __repr__(self):
        return f"<Employee {self.name}>"