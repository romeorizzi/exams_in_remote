import hashlib
import os
import xml.etree.cElementTree as ET
import csv
BLOCKSIZE = 65536
matricole_path = {}


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
        for child in root:
            if child.tag == "input-files-path":
                input_path = child.text
        if input_path is not None:
            return input_path
        else:
            return None
    except FileNotFoundError:
        print("File settings not found!")
    except Exception as exc:
        print("Problem parsing settings file! " + str(exc))


def main():
    matricole_file = settings()
    if matricole_file is None:
        print("Problem parsing settings file! ")
        exit(1)
    with open(matricole_file, "r") as matricole_csv:
        csv_reader = csv.reader(matricole_csv, delimiter=';')
        line_counter = 1
        for line in csv_reader:
            if len(line) == 3:
                matricole_path[line[0]] = line[1]
            else:
                print("Error parsing line" + str(line_counter) + ": " + str(line))
                exit(1)
            line_counter = line_counter + 1
    elaborated = 1
    print("Inzio elaborazione " + str(elaborated) + "/" + str(len(matricole_path)))
    matricole = matricole_path.keys()
    for matricola in matricole:
        # Elaborazione matricola
        print("\t Inizio elaborazione files della matricola " + str(matricola))
        path = matricole_path[matricola]
        num_files = len(next(os.walk(path))[2]) - 1
        hash_dict = {}
        with open(os.path.join(path, str(matricola) + "_output.csv"), "r") as input_hash:
            input_csv = csv.reader(input_hash, delimiter=';')
            line_counter = 1
            for line in input_csv:
                if len(line) == 3:
                    hash_dict[line[0]] = line[1]
                else:
                    print("\tError parsing line " + str(line_counter) + ": " + str(line))
                    exit(1)
                line_counter = line_counter + 1
        # conto il numero dei files
        if num_files > 0 and num_files == len(hash_dict):
            counter = 0
            # scorro contenuto cartella
            print("\tInizio elaborazione di " + str(num_files) + " files")
            fail = False
            for element in os.listdir(path):
                current_path = os.path.join(path, element)
                if os.path.isfile(current_path) and "_output.csv" not in element:
                    # considero solo i file
                    hash = fn_hash(current_path)
                    hash_student = hash_dict.get(element)
                    # verify if exist
                    if hash != hash_student:
                        print("\tErrore nel file: " + str(element))
                        print("\tHash sottoposto: " + str(hash_student))
                        print("\tHash calcolato: " + str(hash))
                        fail = True
                    counter = counter + 1
                    print("\t" + str(element) + " elaborato " + str(counter) + "\\" + str(num_files))
            if not fail:
                print("\tElaborazione terminata con successo per matricola " + str(matricola))
            else:
                print("\tElaborazione terminata con errori per matricola " + str(matricola))
        else:
            if num_files == 0:
                print("\tErrore nessun file trovato nella directory: " + str(path))
            else:
                print("\tErrore numero file non combacia!")
        elaborated = elaborated + 1
    print("Elaborazione terminata")


if  __name__  ==  "__main__":
    main()
