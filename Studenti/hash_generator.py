import hashlib
import os
import xml.etree.cElementTree as ET
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BLOCKSIZE = 65536


def fn_hash(input_path):
    hasher = hashlib.sha1()
    with open(str(input_path), "rb") as file:
        buf = file.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return str(hasher.hexdigest())


def settings():
    try:
        tree = ET.ElementTree(file="settings.xml")
        root = tree.getroot()
        input_path = None
        output_path = None
        matricola = None
        for child in root:
            if child.tag == "input-files-path":
                input_path = child.text
            elif child.tag == "output-files-path":
                output_path = child.text
            elif child.tag == "matricola":
                matricola = child.text
        if input_path is not None and output_path is not None:
            return [input_path, output_path, matricola]
        else:
            return None
    except FileNotFoundError:
        print("File settings not found!")
    except Exception as exc:
        print("Problem parsing settings file! " + str(exc))


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer, created):
        self.observer = observer
        self.created = created

    def on_created(self, event):
        for key in self.created.keys():
            if self.created[key] == "":
                self.created[key] = fn_hash(key) + ";\n"
        self.created[str(event.src_path)] = ""
        print("Created: " + str(event.src_path))


def main():
    settings_vect = settings()
    if settings_vect is None:
        print("Problem parsing settings file! ")
        exit(1)
    PATH = settings_vect[0]
    OUTPUT_PATH = settings_vect[1]
    matricola = settings_vect[2]
    observer = Observer()
    files = {}
    event_handler = MyEventHandler(observer, files)
    observer.schedule(event_handler, PATH, recursive=False)
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    hash_list = []
    for file_name in files.keys():
        head, tail = os.path.split(file_name)
        if files[file_name] == "":
            files[file_name] = fn_hash(file_name) + ";\n"
            hash_list.append(str(tail) + ";" + files[file_name])
        else:
            hash_list.append(str(tail) + ";" + files[file_name])
    with open(os.path.join(OUTPUT_PATH, matricola + "_output.csv"), "w") as output_file:
        for line in hash_list:
            output_file.write(line)
    return

if  __name__  ==  "__main__":
    main()
