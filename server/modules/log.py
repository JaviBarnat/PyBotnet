from server.modules.utils import time
from server.modules.utils import files

#   - 4317b8aa-b76e-11eb-83c8-04d4c4f12df5 [18/May/2021:02:19:32 +0200] "CONNECTION 'SE HA CONECTADO UN NUEVO HOST: 4317b8aa-b76e-11eb-83c8-04d4c4f12df5' HTTP/2" OK

def add(logname, user, type, text, status, protocol=""):
    log = f"{logname}.log"
    if not files.check_file(log):
        files.create_file(log)
    try:
        if protocol != "":
            text += f" {protocol}"
        if user == "":
            user = "-"
        logtext = f'- {user} [{time.get_time()}] "{type} {text}" {status}\n'
        files.add_content_file(log, logtext)
    except:
        pass

