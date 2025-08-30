from flask import Flask
from models import db
import routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Register routes
routes.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
