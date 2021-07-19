from datetime import datetime
from pytz import timezone

TIME_ZONE = "Europe/Madrid"

def get_time():
    try:
        zone = timezone(TIME_ZONE)
        format = "%d/%b/%Y:%H:%M:%S %z"
        tiempo = zone.localize(datetime.now())
        tiempo = tiempo.strftime(format)
        return tiempo
    except:
        return "TIEMPO NO DISPONIBLE"