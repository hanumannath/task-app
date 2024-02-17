from flask import Blueprint, render_template, request, redirect, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from models import Task, db

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/api/home', methods=['GET', 'POST'])
@jwt_required()
def home():
    try:
        current_user_id = get_jwt_identity()
        if request.method == 'POST':
            title = request.form['title']
            desc = request.form['desc']
            task = Task(title=title, desc=desc, user_id=current_user_id)
            db.session.add(task)
            db.session.commit()
        user_tasks = Task.query.filter_by(user_id=current_user_id).all()
        return render_template('index.html', user_tasks=user_tasks)
    except Exception as e:
        logging.error(f"An error occurred in home route: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500


@tasks_bp.route('/api/update/<int:id>', methods=['GET','POST'])
@jwt_required()
def update(id):
    try:
        task = Task.query.get_or_404(id)
        current_user_id = get_jwt_identity()
        if task.user_id != current_user_id:
            return "You are not authorized to update this task.", 403
        if request.method == 'POST':
            title = request.form['title']
            desc = request.form['desc']
            task.title = title
            task.desc = desc
            db.session.commit()
            return redirect("/api/home")
        return render_template('update.html', task=task)
    except Exception as e:
        logging.error(f"An error occurred in update route: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500


@tasks_bp.route('/api/delete/<int:id>', methods=['GET', 'DELETE'])
@jwt_required()
def delete(id):
    try:
        current_user_id = get_jwt_identity()
        task = Task.query.get_or_404(id)
        if task.user_id != current_user_id:
            return "You are not authorized to delete this task.", 403
        db.session.delete(task)
        db.session.commit()
        return redirect("/api/home")
    except Exception as e:
        logging.error(f"An error occurred in delete route: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500
