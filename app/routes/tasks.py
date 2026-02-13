from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Task


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "done": task.done,
        "user_id": task.user_id
    }


tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")


@tasks_bp.post("/")
@jwt_required()
def create_task():
    # pegar o id do usario do token
    user_id = get_jwt_identity()

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()

    if not title:
        return jsonify({"error": "title é obrigatório"}), 400

    task = Task(
        title=title,
        user_id=int(user_id)
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task_to_dict(task)), 200


@tasks_bp.get("/")
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=int(user_id)).all()

    return jsonify([task_to_dict(t) for t in tasks]), 200


@tasks_bp.patch("/<int:task_id>")
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=int(user_id)).first()

    if not task:
        return jsonify({"error": "Task não encontrada"}), 404

    data = request.get_json(silent=True) or {}

    if "done" in data:
        task.done = bool(data["done"])

    if "title" in data:
        task.title = data["title"]

    db.session.commit()

    return jsonify(task_to_dict(task)), 200


@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delet_task(task_id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=int(user_id)).first()
    if not task:
        return jsonify({"error": "Task não encontrada"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deletada"}), 200


@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(id=task_id, user_id=int(user_id)).first()
    if not task:
        return jsonify({"error": "Task não encontrada"}), 404

    return jsonify(task_to_dict(task)), 200
