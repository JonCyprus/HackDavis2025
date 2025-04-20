from source.getEmail import getSessionEmail
from source.sql.getAllUserTasks import getAllUserTasks
from source.respondWithJSON import respondWithJSON


def getAllTasks(app):
    email = getSessionEmail()
    tasks = getAllUserTasks(email)
    parentTasks = []
    
    # Extract root tasks
    for task in tasks:
        if task[2] is None:
            parentTasks.append(task)

    formattedTasks = []
    for task in parentTasks:
        DT = task[5]
        if DT is None:
            date = None
            time = None
        else:
            date = task[5].date()
            time = task[5].time().replace(second=0, microsecond=0)
        arr = [task[0], task[3], str(task[4]), str(date), str(time), task[8]]
        formattedTasks.append({"TASKID": arr[0], "TITLE": arr[1], "DESC": arr[2], "DATE": arr[3], "TIME": arr[4], "COMPLETE": arr[5]})
    print(formattedTasks)
    return respondWithJSON(formattedTasks)