from flask import Blueprint, render_template, request, redirect, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
import logging

from models import User, db

auth_bp = Blueprint('auth', __name__)
logging.basicConfig(filename='app.log', level=logging.ERROR)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        error_message = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if not user:
                error_message = 'Incorrect username or password.'
            elif not user.verify_password(password):
                error_message = 'Incorrect username or password.'
            else:
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                resp = redirect('/api/home')
                set_access_cookies(resp, access_token)
                set_refresh_cookies(resp, refresh_token)
                return resp
        return render_template('login.html', error_message=error_message)
    except Exception as e:
        logging.error(f"An error occurred in login route: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                error_message = "Username already exists. Please choose a different username."
                return render_template('register.html', error_message=error_message)
            else:
                user = User(username=username)
                user.password = password
                db.session.add(user)
                db.session.commit()
                return redirect('/login')
        return render_template('register.html')
    except Exception as e:
        logging.error(f"An error occurred in register route: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500
