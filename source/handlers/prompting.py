# Quick fix DB connection
from flask import session, g, Flask, request
import psycopg2
# Act neccessary lol
import os
import json
# from dotenv import load_dotenv, find_dotenv
from source.sql.getAllUserTasks import getAllUserTasks
from source.sql.createTask import createTask
from source.sql.deleteTask import deleteTask
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from enum import Enum
from datetime import datetime
from source.getEmail import getSessionEmail

class column(Enum):
    TASKID = 0
    EMAIL = 1
    PARENT_ID = 2
    TITLE = 3
    DESC = 4
    TIME = 5
    CREATED_AT = 6
    UPDATED_AT = 7
    COMPLETE = 8

# Helper function. Clears chat history. Sets CURRENT_CHAT to None.
def clearChatHistory(app):
    if app.config.get("CURRENT_CHAT") != None:
        app.config["CURRENT_CHAT"] = None

def sqlFormatTasks(results):

    formattedResults = []
    for task in results:
        if task[column.PARENT_ID.value] is None:
            arr = [task[column.TITLE.value], task[column.DESC.value],
                task[column.TIME.value], task[column.COMPLETE.value]]
            formattedResults.append(arr)
    return formattedResults

def formatPrompt(tasks):
    formattedPrompt = "You are a helpful scheduling assistant named Tasky. \
You will help the user manage tasks that they wish to complete, by a certain date. \
You will also give the user info regarding tasks they have scheduled already. \
The user is only able to interface data through you. \
Provide feedback and offer encouragement on completed tasks, or show concern about missed tasks. \
You cannot manipulate the schedule directly, only comment on it, \
and provide feedback relating to it. Keep your responses concise, two sentences at most. \
If the user requests you to change something about the schedule, \
inform them you are not able to do so, and ask them to try entering \"command mode\". Likewise, if the user \
requests something off-topic, please inform them that you are unable help them. \
However, always be kind and courteous. Do not demand anything of the user, or ask them to do something. \
The current date and time is: \
" + str(datetime.today().replace(second=0, microsecond=0)) + ". A list of currently scheduled tasks is as follows:\n"
    
    for task in tasks:
        print(task)
        DT = task[2]
        if (DT == None):
            time = "None"
            date = "None"
        else:
            time = str(DT.time().replace(second=0, microsecond=0))
            date = str(DT.date())
        currentTask = "Title: %s, Description: %s, Date: %s, Time: %s, Completion: %s \n " % (task[0], task[1], date, time, str(task[3]))
        formattedPrompt += currentTask
    return formattedPrompt

def getTasks(app):
    results = getAllUserTasks(getSessionEmail())
    return results

# Called in the "CHAT MODE" of TaskLand.
# app.config["CURRENT_CHAT"] should contain an array of JSON objects, defining the conversation.
def cerebrasChat(app, prompt):

    currentChat = app.config.get("CURRENT_CONVERSATION")

    if not currentChat:  # If it's None or an empty list
        app.config["CURRENT_CONVERSATION"] = [{"role": "system", "content": formatPrompt(sqlFormatTasks(getTasks(app)))}]
        currentChat = app.config["CURRENT_CONVERSATION"]

    # Attach client to API key
    # load_dotenv(find_dotenv())
    client = Cerebras(
        api_key=app.config["CEREBRAS_API_KEY"]
    )

    # Add user input to conversation history.
    userPrompt = prompt
    currentChat.append({"role": "user", "content": userPrompt})

    # Start a stream
    chat = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=currentChat
    )

    print("Connected successfully with Cerebras, \\source\\handlers\\prompting.py")

    # Add AI response to conversation history
    aiResponse = chat.choices[0].message.content
    # print(aiResponse)
    currentChat.append({"role": "assistant", "content": aiResponse})
    app.config["CURRENT_CONVERSATION"] = currentChat

    return aiResponse

# parse the user input into a command readable by "execute command" with Cerebras
def cerebrasCommand(app, prompt):
    type_string = {"type": "string"}
    task_schema = {
        "type": "object",
        "properties": {
            "command": type_string,
            "title": type_string,
            "description": type_string,
            "date": type_string,
            "time": type_string,
            "response": type_string
        },
        "required": ["command", "title", "date", "time"],
        "additionalProperties": False
    }

    client = Cerebras(
        api_key=app.config["CEREBRAS_API_KEY"]
    )

    aiPrompt = "You are a task scheduling assistant, translating regular text into an object with multiple parameters. \
You must interpret a command that the user is trying to execute. The available commands are: \
ADD, DELETE, EDIT, NULL. \
If the message is not a command, return NULL, and ask for better input. \
Fill in any remaining fields as required, or as specified by the user. \
Include a small polite response, describing what it is you did. \
Always be polite and courteous. \
The current date and time is: " + str(datetime.today().replace(second=0, microsecond=0)) + ". \
A list of current scheduled tasks is as follows:\n "
    tasks = getTasks(app)
    fPrompt = ""
    for task in tasks:
        DT = task[5]
        if (DT == None):
            time = "None"
            date = "None"
        else:
            time = str(DT.time().replace(second=0, microsecond=0))
            date = str(DT.date())
        fPrompt += "Title: %s, Description: %s, Date: %s, Time: %s, Completion: %s \n " % (task[column.TITLE.value], task[column.DESC.value], date, time, str(task[column.COMPLETE.value]))

    aiPrompt += fPrompt

    currChat=[{"role": "system", "content": aiPrompt}]

    # Add user input to conversation history.
    print(prompt)
    currChat.append({"role": "user", "content": str(prompt)})
    print(currChat)

    # Start a stream
    chat = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=currChat,
        response_format={
        "type": "json_schema", 
        "json_schema": {
            "name": "task_schema",
            "strict": True,
            "schema": task_schema
        }
    }
    )

    print("Connected successfully with Cerebras, \\source\\handlers\\prompting.py")

    # Add AI response to conversation history
    task_data = json.loads(chat.choices[0].message.content)
    print(task_data)
    print(json.dumps(task_data, indent=2))

    executeCommand(app, task_data)
    return task_data.get("response")


def executeCommand(app, params):
    command = params.get("command")
    if command == "ADD":
        app.config["CURRENT_CONVERSATION"] = None
        date_string = params.get("date") + " " + params.get("time")
        DT_OBJ = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        createTask(getSessionEmail(), params.get("title"), params.get("description"), DT_OBJ,
                   None, False)
    elif command == "DELETE":
        app.config["CURRENT_CONVERSATION"] = None
        date_string = params.get("date") + " " + params.get("time")
        DT_OBJ = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        deleteTask(getSessionEmail(), params.get("title"))
    return