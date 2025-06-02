import sys
import socketserver
import threading
import json

from timescale.database import init_db
from timescale.crud import read
from uart.uart import MBSerial

# generate fake data
# from timescale.factory import factory

# global
HOST           = "0.0.0.0"
UDP_PORT       = 10000
MICRO_COMMANDS = ["TLH", "THL", "LTH", "LHT", "HTL", "HLT"]
BASE_TYPES     = ["temperature", "humidity", "luminosity"]

uBitSerial = MBSerial()

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

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
        if cmd in MICRO_COMMANDS:
            uBitSerial.send(cmd)
            return

        act = data.get("action")
        if  act == "getValues()":
            # On renvoie toutes les dernières valeurs
            res = {}
            sensors = []
            for i in BASE_TYPES:
                sensor = read(i)
                sensors.append(sensor)
            for i in sensors:
                res.update({i.type_sensor: i.value})
            
            sock.sendto(json.dumps(res).encode(), self.client_address)
            return

        print(f"{thread_name}: Unknown JSON message: {data}")

if __name__ == '__main__':
    # timescale db initialization
    init_db()
    
    # Démarrage du serveur UDP
    server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"Server started at {HOST} port {UDP_PORT}")
    print('Press Ctrl-C to quit.')

    try:
        uBitSerial.start()
    except (KeyboardInterrupt, SystemExit):
        # Arrêt propre
        server.shutdown()
        server.server_close()
        # uBitSerial.close()
        sys.exit(0)