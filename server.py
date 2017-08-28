#!/usr/bin/env python3
import logging
from service import *
from bluetooth import *

class BTSPServer:
    def __init__(self):
        logging.info("init BTSPServer")
        socket = BluetoothSocket()
        socket.bind(('', PORT_ANY))
        socket.listen(0)

        advertise_service(
                socket, 'SP',
                provider = 'pybtsp server',
                service_id = SERVICE_UUID,
                service_classes = [ SERVICE_UUID, SERIAL_PORT_CLASS ],
                profiles = [ SERIAL_PORT_PROFILE ]
                )
        self.socket = socket
        self.clients = {}

    def __del__(self):
        stop_advertising(self.socket)
        self.socket.close()
        for s in self.clients:
            self.close_client(self.clients[s])

    def __str__(self):
        server = self.socket.getsockname()
        clients = [k for k in self.clients.keys()]

        return '<server on RFCOMM: {!s}\n clients {!s}>'.format(server, clients)

    def accept_client(self):
        socket, info = self.socket.accept()
        logging.info('connection from client {!s}'.format(info))
        self.clients[info] = socket
        return info

    def close_client(self, socketid):
        logging.info('closing socket to client {!s}'.format(socketid))
        socket = self.clients[socketid]
        socket.close()
        del self.clients[socketid]

    def handle_msg(self, socketid, timeout):
        socket = self.clients[socketid]
        CLOSE = 0
        def handleRequest(msg):
            """return: reply, closeConnect"""
            import wifi
            req = msg.get("request")
            param = msg.get("param")
            if req == "getWifiInterface":
                return wifi.getWifiInterface(), CLOSE
            elif req == "getScanResult":
                return wifi.getScanResult(), CLOSE
            elif req == "getWifiConnection":
                return wifi.getWifiConnection(), CLOSE
            elif req == "activateWifiConnection":
                uuid = param.get("uuid")
                iface = param.get("iface")
                v = wifi.activateWifiConnection(uuid, iface)
                if v.get("error"):
                    return v, CLOSE
                else:
                    return v, CLOSE
            elif req == "createWifiConnection":
                ssid = param.get("ssid")
                passwd = param.get("password")
                iface = pararm.get("iface")
                v = wifi.createWifiConnection(ssid, passwd, iface)
                if v.get("error"):
                    return v, CLOSE
                else:
                    return v, CLOSE
            elif req == "deleteWifiConnection":
                uuid = param.get("uuid")
                v = wifi.deleteWifiConnection(uuid)
                if v.get("error"):
                    return v, CLOSE
                else:
                    return v, CLOSE
            elif req == "disconnectWifi":
                iface = param.get("iface")
                v = wifi.disconnectWifi(iface)
                if v.get("error"):
                    return v, CLOSE
                else:
                    return v, CLOSE
            else:
                return {"error": "unknown request"}, True
            # end of handleRequest()

        from jsonlpendec import encodeTo, decodeFrom
        while True:
            socket.settimeout(timeout)
            try:
                msg = decodeFrom(socket)
                socket.settimeout(None)
                logging.info('<- {!s}'.format(msg))
            except btcommon.BluetoothError as e:
                logging.info(e)
                return False

            reply, what_to_do = handleRequest(msg)
            logging.info('-> {!s}'.format(reply))
            msg["reply"] = reply

            try:
                encodeTo(socket, msg)
            except btcommon.BluetoothError as e:
                logging.info(e)
                return False

            if what_to_do == CLOSE:
                return True
            # wait for next msg

    def run(self):
        logging.info('server started and waiting for connection')
        while True:
            socketid = self.accept_client()
            if self.handle_msg(socketid, 1):
                self.close_client(socketid)

def set_piscan():
    import subprocess
    if subprocess.call(['hciconfig', 'hci0', 'piscan']) != 0:
        logging.error("cant't set piscan for hci0")
        return False
    return True

def main():
    logging.basicConfig(
            filename='server.log',
            level=logging.DEBUG,
            #filemode='w',
            format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        if not set_piscan():
            return
        a = BTSPServer()
        logging.info(a)
        a.run()
    except KeyboardInterrupt:
        logging.info('exiting')

if __name__ == "__main__":
    main()
