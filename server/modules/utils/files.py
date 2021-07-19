import os.path

def check_folder(path):
    isExist = os.path.exists(path)
    if isExist == False:
        try:
            os.mkdir(path)
        except:
            pass

def check_start():
    check_folder("./server/db")
    check_folder("./server/logs")
    check_folder("./server/logs/bots")
    check_folder("./server/logs/server")
    check_folder("./server/files")
    check_folder("./server/files/bots")
    check_folder("./server/files/upload")

def check_file(file):
    isExist = os.path.isfile(file)
    return isExist

def create_file(name):
    f = open(name, "w")
    f.write("")
    f.close()

def add_content_file(name, filetext):
    f = open(name, "a")
    f.write(filetext)
    f.close()

def save_file(location, data):
    f = open(location, "wb")
    f.write(data)
    f.close()

def read_file(location):
    f = open(location, "rb")
    return f.read()

def read_chunks(location, chunk_size=4096):
    try:
        with open(location, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data
    except:
        yield b""

def get_file_name(file):
    return os.path.basename(file)