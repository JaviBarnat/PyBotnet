import os
import glob
from pathlib import Path, PureWindowsPath

def download_file(rule, filename):
    ruta = "../server/files"
    f = ""
    if "/files/bots/" in rule.rule:
        ids = filename.split("/")
        bot_id = ids[0]
        ruta += f"/bots/{bot_id}"
        f = ids[1]
    elif "/files/upload" in rule.rule:
        ruta += f"/upload"
        f = filename
    return ruta, f

def download_log(rule):
    ruta = "../server/logs"
    if "/logs/bots/" in rule.rule:
        ruta += f"/bots"
    elif "/logs/server/" in rule.rule:
        ruta += f"/server"
    return ruta

def get_filename(path):
    filepath = (str(Path(PureWindowsPath(path)))).replace("\\","/")
    array = filepath.split("/")
    array.pop(0)
    filename = array[-1]
    filepath = "/".join(array)
    return filename, filepath

def get_files(path):
    dir = {}
    for name in os.listdir(path):
        if os.path.isdir(f"{path}/{name}"):
            a = []
            array = glob.glob(f"{path}/{name}/*.*")
            for i in array:
                filename, filepath = get_filename(i)
                if ".png" in filename or ".jpg" in filename or ".gif" in filename or ".bmp" in filename:
                    html = f'&#128247 <a href="{filepath}"> {filename} </a>'
                elif ".mp4" in filename or ".avi" in filename or ".mpeg" in filename or ".mwv" in filename:
                    html = f'&#127916 <a href="{filepath}"> {filename} </a>'
                elif ".exe" in filename or ".bat" in filename or ".dll" in filename or ".sys" in filename or ".msi" in filename:
                    html = f'&#128190 <a href="{filepath}"> {filename} </a>'
                elif ".mp3" in filename or ".wav" in filename or ".wma" in filename:
                    html = f'&#127911 <a href="{filepath}"> {filename} </a>'
                elif ".zip" in filename or ".rar" in filename or ".tar" in filename:
                    html = f'&#128230 <a href="{filepath}"> {filename} </a>'
                elif ".txt" in filename or ".doc" in filename or ".docx" in filename:
                    html = f'&#128221 <a href="{filepath}"> {filename} </a>'
                elif ".log" in filename:
                    html = f'&#128220 <a href="{filepath}"> {filename} </a>'
                else:
                    html = f'&#128196 <a href="{filepath}"> {filename} </a>'
                a.append(html)
            dir[name] = a
    return dir