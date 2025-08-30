from flask import render_template, request, redirect, url_for, flash
from models import db, Employee

def init_app(app):
    @app.route("/")
    def dashboard():
        employees = Employee.query.all()
        return render_template("dashboard.html", employees=employees)

    @app.route("/add", methods=["POST"])
    def add_employee():
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        salary = request.form['salary']
        address = request.form['address']
        joining_date = request.form['joining_date']
        end_date = request.form['end_date'] if request.form['end_date'] else None

        new_employee = Employee(
            name=name,
            email=email,
            position=position,
            salary=salary,
            address=address,
            joining_date=joining_date,
            end_date=end_date
        )
        db.session.add(new_employee)
        db.session.commit()
        flash("Employee added successfully!", "success")
        return redirect(url_for("dashboard"))

    @app.route("/update/<int:id>", methods=["GET", "POST"])
    def update_employee(id):
        employee = Employee.query.get_or_404(id)
        if request.method == "POST":
            employee.name = request.form['name']
            employee.email = request.form['email']
            employee.position = request.form['position']
            employee.salary = request.form['salary']
            employee.address = request.form['address']
            employee.joining_date = request.form['joining_date']
            employee.end_date = request.form['end_date'] if request.form['end_date'] else None

            db.session.commit()
            flash("Employee updated successfully!", "info")
            return redirect(url_for("dashboard"))

        return render_template("update_employee.html", employee=employee)

    @app.route("/delete/<int:id>")
    def delete_employee(id):
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        flash("Employee deleted successfully!", "danger")
        return redirect(url_for("dashboard"))
