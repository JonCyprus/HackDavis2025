import source.sql
from source.getEmail import getSessionEmail
from source.respondWithJSON import respondWithJSON


def getAllSubtasks(app):
    email = getSessionEmail()
    results = source.sql.getNestedTasks(email)
    task_tree = build_task_tree(results)
    return respondWithJSON(task_tree)

def build_task_tree(tasks):
    task_dict = {t["task_id"]: {**t, "subtasks": []} for t in tasks}
    root_tasks = []

    for task in tasks:
        if task["parent_id"]:
            parent = task_dict.get(task["parent_id"])
            if parent:
                parent["subtasks"].append(task_dict[task["task_id"]])
        else:
            root_tasks.append(task_dict[task["task_id"]])

    return root_tasks


