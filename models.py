from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    joining_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Employee {self.name}>"
