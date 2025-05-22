# server.py
# Passerelle UDP ↔ micro:bit via USB tty, stockage des valeurs reçues dans un fichier JSON

import time
import sys
import socket
import socketserver
import serial
import threading
import json
import os

HOST           = "0.0.0.0"
UDP_PORT       = 10000
MICRO_COMMANDS = ["TLH", "THL", "LTH", "LHT", "HTL", "HLT"]
FILENAME       = "values.json"

# On gère 3 valeurs séparées
LAST_VALUES = {
    "temperature": None,
    "humidity": None,
    "luminosity": None
}

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        raw = self.request[0].strip().decode()
        sock = self.request[1]
        thread_name = threading.current_thread().name

        # On ne traite que du JSON entrant
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print(f"{thread_name}: Invalid JSON received: {raw!r}")
            return

        print(f"{thread_name}: client: {self.client_address}, received JSON: {data}")

        cmd = data.get("command")
        act = data.get("action")

        if cmd in MICRO_COMMANDS:
            sendUARTMessage(cmd)

        elif act == "getValues()":
            # On renvoie toutes les dernières valeurs
            response = LAST_VALUES
            sock.sendto(json.dumps(response).encode(), self.client_address)

        else:
            print(f"{thread_name}: Unknown JSON message: {data}")

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

# Configuration du port série
SERIALPORT = "COM6"       # ou "/dev/ttyUSB0" sur Linux
BAUDRATE   = 115200
ser        = serial.Serial()

def initUART():
    ser.port     = SERIALPORT
    ser.baudrate = BAUDRATE
    ser.bytesize = serial.EIGHTBITS
    ser.parity   = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout  = None       # lecture bloquante sur readline
    ser.xonxoff  = False
    ser.rtscts   = False
    ser.dsrdtr   = False
    print('Starting Up Serial Monitor')
    try:
        ser.open()
    except serial.SerialException:
        print(f"Serial {SERIALPORT} port not available")
        sys.exit(1)

def sendUARTMessage(msg):
    ser.write(msg.encode())
    print(f"Message <{msg}> sent to micro-controller.")


# Dictionnaire des unités associées à chaque clé
UNITS = {
    "temperature": "°C",
    "humidity": "%",
    "luminosity": "lux"
}


def append_value_to_json(key, value):
    """Ajoute une entrée {'timestamp': ..., 'key': ..., 'unit': ..., 'value': ...} au fichier JSON."""
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "key": key,
        "unit": UNITS.get(key, ""),  # Ajoute l'unité correspondante ou vide si inconnue
        "value": value
    }
    if not os.path.isfile(FILENAME):
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(FILENAME, "r+", encoding="utf-8") as f:
        try:
            data_list = json.load(f)
        except json.JSONDecodeError:
            data_list = []
        data_list.append(entry)
        f.seek(0)
        f.truncate()
        json.dump(data_list, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    initUART()
    print('Press Ctrl-C to quit.')
    
    # Démarrage du serveur UDP
    server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"Server started at {HOST} port {UDP_PORT}")

    try:
        # Boucle de lecture du port série : lire ligne par ligne pour éviter les fragments JSON
        while ser.isOpen():
            line = ser.readline().decode(errors="replace").strip()
            if line and ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key in LAST_VALUES:
                    LAST_VALUES[key] = value
                print(f"Received from micro:bit -> {key} = {value}")
                append_value_to_json(key, value)
            # elif line:
            #     print(f"Ligne reçue sans ':': {line}")
    except (KeyboardInterrupt, SystemExit):
        # Arrêt propre
        server.shutdown()
        server.server_close()
        ser.close()
        sys.exit(0)