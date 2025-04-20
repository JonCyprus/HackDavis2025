# Quick fix DB connection
from flask import session, g, Flask
import psycopg2
# Act neccessary lol
import os
import json
from dotenv import load_dotenv, find_dotenv
# from source.sql.getAllUserTasks import getAllUserTasks
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from enum import Enum

from datetime import datetime

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
    dtetime = datetime.today()
    dtetime = dtetime.replace(second=0, microsecond=0)
    formattedPrompt = "You are a helpful scheduling assistant.\
 You cannot manipulate the schedule directly, only comment on it,\
and provide feedback relating to it. Keep your responses concise, with two sentences at most. If the user requests you to change something about the schedule, \
inform them you are not able to do so, and ask them to try entering \"command mode\". Likewise, if the user\
 requests something off-topic, please inform them that you are unable help them. However, always be kind and courteous. \
 The current date and time is: \
" + str(dtetime) + ". A list of currently scheduled events is as follows:\n"
    
    for task in tasks:
        print(task)
        DT = task[2]
        if (DT == None):
            time = "None"
            date = "None"
        else:
            time = str(DT.time().replace(second=0, microsecond=0))
            date = str(DT.date())
        currentTask = "Title: %s, Description: %s, Date: %s, Time: %s, Completion: %s\n" % (task[0], task[1], date, time, str(task[3]))
        formattedPrompt += currentTask
    return formattedPrompt

# def formatDate(unformDate):
    

# Called in the "CHAT MODE" of TaskLand.
# app.config["CURRENT_CHAT"] should contain an array of JSON objects, defining the conversation.
def cerebrasChat(app, prompt):

    # ifndef "CURRENT CONVERSATION", initialize it.
    #if app.config.get("CURRENT_CHAT") == None:
    #    aiPrompt = formatPrompt()
    #    app.config["CURRENT_CHAT"] = [{"role": "system", "content": aiPrompt}]

    # FIXME: Recieve prompt, not from input, but from an actual request.

    currentChat = [
        {"role": "system", "content": prompt}
    ]
    print("Connected! Waiting for input...")
    while True:

        # Attach client to API key
        load_dotenv(find_dotenv())
        client = Cerebras(
            api_key=os.getenv("CEREBRAS_API_KEY")
        )

        # Add user input to conversation history.
        userPrompt = input()
        currentChat.append({"role": "user", "content": userPrompt})

        # Start a stream
        chat = client.chat.completions.create(
            model="llama-4-scout-17b-16e-instruct",
            messages=currentChat
        )

        # Add AI response to conversation history, and print for the user.
        aiResponse = chat.choices[0].message.content
        print(aiResponse)
        currentChat.append({"role": "assistant", "content": aiResponse})
    

    # return aiResponse

# Quick dirty run test
def getAllUserTasks(email, conn):
    # conn = g.db
    cur = conn.cursor()
    results = None
    try:
        cur.execute("SELECT * FROM tasks WHERE email = %s", (email,))
        results = cur.fetchall()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # Always rollback on failure
        print(f"Could not get tasks for %s", email)

    return results

if __name__ == "__main__":
    app = Flask(__name__)
    print("Starting DB connection...")
    conn = psycopg2.connect("postgresql://HackDavis_owner:npg_PiwzBn1xSj2g@ep-weathered-lab-a6gnb5x1-pooler.us-west-2.aws.neon.tech/HackDavis?sslmode=require")
    results = getAllUserTasks("joncyprus99@gmail.com", conn)
    prompt = formatPrompt(sqlFormatTasks(results))
    cerebrasChat(None, prompt)
