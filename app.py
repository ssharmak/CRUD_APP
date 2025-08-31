from flask import Flask
from models import db
import routes

# Create the Flask application
app = Flask(__name__)

# =======================
# App Configuration
# =======================

# Secret key (used for sessions, cookies, and CSRF protection in forms)
app.config['SECRET_KEY'] = 'supersecretkey'  

# Database setup: Here we are using a SQLite database file named "employees.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'

# Disable modification tracking:
# This improves performance since we are not using event-based object change tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link the SQLAlchemy database instance (from models.py) with our Flask app
db.init_app(app)

# =======================
# Database Initialization
# =======================

# Create all the database tables defined in models.py
# (only runs if the tables don’t already exist)
with app.app_context():
    db.create_all()

# =======================
# Route Registration
# =======================

# Import and register all routes (endpoints) from routes.py
# This keeps routes organized and separate from the main app file
routes.init_app(app)

# =======================
# Application Entry Point
# =======================

if __name__ == "__main__":
    # Start the Flask development server
    # debug=True reloads the server automatically on code changes
    app.run(debug=True)
