from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object (used for ORM functionality)
db = SQLAlchemy()

# Employee model representing the 'employee' table in the database
class Employee(db.Model):
    # Primary Key - Unique ID for each employee
    id = db.Column(db.Integer, primary_key = True)

    # Employee full name (cannot be NULL, max length 100 characters)
    name = db.Column(db.String(100), nullable = False)

    # Employee email (cannot be NULL, max length 120 characters)
    email = db.Column(db.String(120), unique = True, nullable = False)

    # Employee's phone number (cannot be null and repeated and it should be unique)
    phone = db.Column(db.String(15), unique = True, nullable = False)

    # Employee's job position/title (e.g., Developer, Manager, etc.)
    position = db.Column(db.String(100), nullable = False)  # ✅ keep as position

    # Employee salary (stored as a floating-point number, cannot be NULL)
    salary = db.Column(db.Float, nullable = False)

    # Employee address (cannot be NULL, max length 200 characters)
    address = db.Column(db.String(200), nullable = False)

    # Date when the employee joined the company (stored as string for simplicity)
    joining_date = db.Column(db.String(20), nullable = False)

    # Optional: Date when the employee left/ends contract (nullable=True)
    end_date = db.Column(db.String(20), nullable = True)

    # String representation for debugging/logging
    def __repr__(self):
        return f"<Employee {self.name}>"
