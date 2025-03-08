from flask import Flask, jsonify, request

app = Flask(__name__)

tasks_db = {
    "tasks": {
        "1": {
            "id": 1,
            "title": "Task Title",
            "description": "Task Description",
            "completed": False,
        }
    }
}


def get_all_tasks():
    task_list = []
    for task_id, task in tasks_db["tasks"].items():
        task_list.append(task)
    return task_list


def get_specific_task(task_id):
    task = tasks_db["tasks"][task_id]
    return task


def update_task_repository(task_data, task_id):
    tasks_db["tasks"].update({f"{task_id}": task_data})


def register_task(task_data):
    task_id = int(max(tasks_db["tasks"].keys())) + 1
    task_data.update({"id": f"{task_id}", "completed": False})
    update_task_repository(task_data, task_id)
    return jsonify(task_data), 201


def put_task(task_data, task_id):
    task_data.update({"id": f"{task_id}", "completed": False})
    update_task_repository(task_data, task_id)
    return jsonify({"message": "Task updated successfully."}), 201

def delete_task(task_id):
    tasks_db["tasks"].pop(task_id)
    return jsonify({"message": "Task deleted successfully."}), 200

def complete_task(task_id):
    tasks_db["tasks"][task_id]["completed"] = True
    return jsonify({"message": "Task marked as completed."}), 200


# optional route for argument
@app.route("/tasks", methods=["GET", "POST"])
@app.route("/tasks/<task_id>", methods=["GET", "PUT", "DELETE"])
@app.route("/tasks/<task_id>/complete", methods=["PATCH"])
def task(task_id=False):
    match request.method:
        case "GET":
            if task_id:
                return get_specific_task(task_id)

            else:
                return get_all_tasks()

        case "POST":      
            return register_task(request.json)

        case "PUT":
            return put_task(request.json, task_id)
 
        case "DELETE":
            return delete_task(task_id)

        case "PATCH":
            return complete_task(task_id)
