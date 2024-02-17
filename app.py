from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from auth.routes import auth_bp
from tasks.routes import tasks_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8045)

