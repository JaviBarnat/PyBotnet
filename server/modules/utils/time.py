from datetime import datetime
from pytz import timezone

def get_time():
    try:
        zone = timezone("Europe/Madrid")
        format = "%d/%b/%Y:%H:%M:%S %z"
        tiempo = zone.localize(datetime.now())
        tiempo = tiempo.strftime(format)
        return tiempo
    except:
        return "TIEMPO NO DISPONIBLE"