from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import os

app = Flask(__name__)
CORS(app)

# In-memory storage (we'll add a DB in later phases if you want)
tasks = {}

# ──────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health_check():
    """Health endpoint — Kubernetes and Prometheus will ping this"""
    return jsonify({"status": "healthy", "service": "flask-taskmanager"}), 200


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks"""
    return jsonify({"tasks": list(tasks.values()), "count": len(tasks)}), 200


@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Return a single task by ID"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "status": data.get('status', 'pending'),   # pending | in-progress | done
        "priority": data.get('priority', 'medium') # low | medium | high
    }
    tasks[task_id] = task
    return jsonify(task), 201


@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task['title']       = data.get('title',       task['title'])
    task['description'] = data.get('description', task['description'])
    task['status']      = data.get('status',      task['status'])
    task['priority']    = data.get('priority',    task['priority'])

    tasks[task_id] = task
    return jsonify(task), 200


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    deleted = tasks.pop(task_id)
    return jsonify({"message": "Task deleted", "task": deleted}), 200


# ──────────────────────────────────────────
# RUN
# ──────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
