import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect("./server/db/database.db", check_same_thread=False)
        return con
    except Error:
        print(Error)

def create_tables(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS bots (bot_id text PRIMARY KEY, status text, system text, node text, release text, version text, machine text, processor text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS geobots (bot_id text PRIMARY KEY, ip text, hostname text, city text, region text, country text, location text)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS tasks (task_id text PRIMARY KEY, bot_id text, type text, status text, date_start text, date_finish text, aux text, response text)")
    con.commit()

# SAVE BOT DATA

def add_bot(con, array):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT OR REPLACE INTO bots(bot_id, status, system, node, release, version, machine, processor) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", array)
    con.commit()

def add_bot_geolocation(con, array):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT OR REPLACE INTO geobots(bot_id, ip, hostname, city, region, country, location) VALUES(?, ?, ?, ?, ?, ?, ?)""", array)
    con.commit()

# GET BOT DATA

def get_bot(con, id):
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT * FROM bots WHERE bot_id = ? """, [f"{id}"])
    bot = cursorObj.fetchall()
    return bot

def get_bots(con):
    array = []
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM bots")
    bots = cursorObj.fetchall()
    for bot in bots:
        array.append(bot)
    return array

def get_connected_bots(con):
    array = []
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM bots WHERE status = 0")
    bots = cursorObj.fetchall()
    for bot in bots:
        array.append(bot)
    return array

def get_bot_geolocation(con, id):
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT * FROM geobots WHERE bot_id = ? """, [f"{id}"])
    geobot = cursorObj.fetchall()
    return geobot

def get_bots_geolocation(con):
    array = []
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM geobots")
    bots = cursorObj.fetchall()
    for geo in bots:
        array.append(geo)
    return array

# SAVE PENDING TASK

def add_task(con, array):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT OR REPLACE INTO tasks(task_id, bot_id, type, status, date_start, date_finish, aux, response) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", array)
    con.commit()

# GET PENDING TASKS

def get_pending_tasks(con):
    array = []
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM tasks WHERE status = 3")
    tasks = cursorObj.fetchall()
    for task in tasks:
        array.append(task)
    return array

def get_pending_tasks_bot(con, id):
    array = []
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT * FROM tasks WHERE status = 3 AND bot_id = ? """, [f"{id}"])
    tasks = cursorObj.fetchall()
    for task in tasks:
        array.append(task)
    return array

# SAVE COMPLETE TASK

def add_completed_task(con, array):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT OR REPLACE INTO tasks(task_id, bot_id, type, status, date_start, date_finish, aux, response) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", array)
    con.commit()

# GET ALL COMPLETE TASKS

def get_completed_tasks(con):
    array = []
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM tasks WHERE status != 3")
    tasks = cursorObj.fetchall()
    for task in tasks:
        array.append(task)
    return array

def get_completed_task_id(con, id):
    array = []
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT * FROM tasks WHERE status != 3 AND bot_id = ? """, [f"{id}"])
    tasks = cursorObj.fetchall()
    for task in tasks:
        array.append(task)
    return array

# GET SPECIFIC TASK

def get_task(con, id):
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT * FROM tasks WHERE task_id = ? """, [f"{id}"])
    array = cursorObj.fetchall()
    return array

# DELETE BOT

def delete_bot(con, id):
    cursorObj = con.cursor()
    cursorObj.execute("""DELETE FROM bots WHERE bot_id = ? """, [f"{id}"])
    cursorObj.execute("""DELETE FROM geobots WHERE bot_id = ? """, [f"{id}"])
    con.commit()
