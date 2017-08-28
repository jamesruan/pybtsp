#!/usr/bin/env python3
import logging

from service import *
from bluetooth import *

def main():
    logging.basicConfig(
            filename='client.log',
            level=logging.DEBUG,
            filemode='w',
            format='%(asctime)s - %(levelname)s - %(message)s')

    d = find_service(uuid = SERVICE_UUID)
    print(d)

    saved = None
    for s in d:
        from jsonlpendec import encodeTo, decodeFrom
        while True:
            try:
                socket = BluetoothSocket()
                hp = (s['host'], s['port'])
                socket.connect(hp)
                saved = hp
                encodeTo(socket, {'request': 'getWifiInterface'})
                msg = decodeFrom(socket)
                print(msg)
                socket.close()
                break
            except btcommon.BluetoothError as e:
                print(e)

    while True:
        try:
            socket = BluetoothSocket()
            socket.connect(saved)
            encodeTo(socket, {'request': 'getWifiConnection'})
            msg = decodeFrom(socket)
            print(msg)
            socket.close()
            break
        except btcommon.BluetoothError as e:
            print(e)

if __name__ == "__main__":
    main()
