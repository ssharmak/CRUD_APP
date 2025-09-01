from flask import render_template, request, redirect, url_for, flash
from models import db, Employee
from sqlalchemy import or_

# This function is called from app.py to register all routes with the Flask app
def init_app(app):

    # ======================
    # Dashboard Route (Main Page)
    # ======================
    @app.route("/", methods=["GET", "POST"])
    def dashboard():
        # Start with the base query for all employees
        query = Employee.query

        # ---- Search ----
        # Get the search value from the request (example: ?search=John)
        search = request.args.get("search")
        if search:
            # If search is provided, filter employees by name, email, or position (case-insensitive)
            query = query.filter(
                or_(
                    Employee.name.ilike(f"%{search}%"),
                    Employee.email.ilike(f"%{search}%"),
                    Employee.position.ilike(f"%{search}%"),
                )
            )

        # ---- Filters ----
        # Filtering employees based on salary range
        min_salary = request.args.get("min_salary")
        max_salary = request.args.get("max_salary")
        if min_salary:
            query = query.filter(Employee.salary >= float(min_salary))  # Salary >= min
        if max_salary:
            query = query.filter(Employee.salary <= float(max_salary))  # Salary <= max

        # Filter employees by joining date range
        join_from = request.args.get("join_from")
        join_to = request.args.get("join_to")
        if join_from:
            query = query.filter(Employee.joining_date >= join_from)  # Joined after this date
        if join_to:
            query = query.filter(Employee.joining_date <= join_to)    # Joined before this date

        # Filter employees by end date range
        end_from = request.args.get("end_from")
        end_to = request.args.get("end_to")
        if end_from:
            query = query.filter(Employee.end_date >= end_from)       # Ended after this date
        if end_to:
            query = query.filter(Employee.end_date <= end_to)         # Ended before this date

        # ---- Sorting ----
        # Sorting employees based on the selected option
        sort_by = request.args.get("sort_by")
        if sort_by == "name":
            query = query.order_by(Employee.name.asc())              # Sort by name (A-Z)
        elif sort_by == "salary":
            query = query.order_by(Employee.salary.desc())           # Sort by salary (high → low)
        elif sort_by == "joining_date":
            query = query.order_by(Employee.joining_date.desc())     # Sort by recent joining
        elif sort_by == "end_date":
            query = query.order_by(Employee.end_date.desc())         # Sort by recent end date

        # Execute the final query and get the list of employees
        employees = query.all()

        # Render the dashboard template and pass the employees list
        return render_template("dashboard.html", employees=employees)

    # ======================
    # Add Employee Route
    # ======================
    @app.route("/add", methods=["GET", "POST"])
    def add_employee():
        if request.method == "POST":
            # Collect form data submitted by the user
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            position = request.form['position']
            salary = float(request.form['salary']) if request.form['salary'] else 0
            address = request.form['address']
            joining_date = request.form['joining_date']
            end_date = request.form['end_date'] if request.form['end_date'] else None

            # Create a new Employee object with form data
            new_employee = Employee(
                name=name,
                email=email,
                phone = phone,
                position=position,
                salary=salary,
                address=address,
                joining_date=joining_date,
                end_date=end_date
            )

            # Add new employee to database
            db.session.add(new_employee)
            db.session.commit()

            # Show success message on the page
            flash("Employee added successfully!", "success")

            # Redirect to dashboard after adding
            return redirect(url_for("dashboard"))

        # If GET request → show the Add Employee form
        return render_template("add_employee.html")

    # ======================
    # Update Employee Route
    # ======================
    @app.route("/update/<int:id>", methods=["GET", "POST"])
    def update_employee(id):
        # Fetch the employee by ID, or show 404 if not found
        employee = Employee.query.get_or_404(id)

        if request.method == "POST":
            # Update the employee object with new data from the form
            employee.name = request.form['name']
            employee.email = request.form['email']
            employee.phone = request.form['phone']
            employee.position = request.form['position']
            employee.salary = float(request.form['salary']) if request.form['salary'] else 0
            employee.address = request.form['address']
            employee.joining_date = request.form['joining_date']
            employee.end_date = request.form['end_date'] if request.form['end_date'] else None

            # Save the updated changes in the database
            db.session.commit()

            # Show update confirmation message
            flash("Employee updated successfully!", "info")

            # Redirect back to dashboard
            return redirect(url_for("dashboard"))

        # If GET request → show the Update Employee form pre-filled with existing data
        return render_template("update_employee.html", employee=employee)

    # ======================
    # Delete Employee Route
    # ======================
    @app.route("/delete/<int:id>")
    def delete_employee(id):
        # Get employee by ID, or 404 if not found
        employee = Employee.query.get_or_404(id)

        # Remove the employee from the database
        db.session.delete(employee)
        db.session.commit()

        # Flash message with red color (danger type)
        flash("Employee deleted successfully!", "danger")

        # Redirect back to dashboard after deletion
        return redirect(url_for("dashboard"))
