import socket
from machine import Pin
import gc
import handlers
import user_handlers
from lib.request import Request
from lib.response import Response
from utils import *

handler = {
    "/firmware": handlers.firmware_update,
    "/wifi": handlers.wifi_creds_update,
    # "/getconfig": None
}

http_methods = ["GET", "POST"]

def main():
    wifi_creds_file = open("wifi.cfg", "r")
    wifi_creds_lines = wifi_creds_file.read().split("\n")
    wifi_creds_file.close()
    wifi_creds = {}
    for line in wifi_creds_lines:
        wifi_creds[line.split("=", 1)[0]] = line.split("=", 1)[1]
    del wifi_creds_file
    del wifi_creds_lines
    gc.collect()
    wifi_connect_or_ap(wifi_creds["ssid"], wifi_creds["password"])

    gpio_pin = Pin(0, Pin.OUT)
    gpio_pin.on()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 80))
    s.listen(5)
    handler.update(user_handlers.get_handlers())

    while True:
        conn, _addr = s.accept()
        request = Request(get_full_request(conn))
        if request.url in handler:
            response = handler[request.url](request)
            if type(response) == Response:
                conn.sendall(response.text().encode())
                conn.close()
            elif type(response) == list and type(response[0]) == Response and callable(response[1]):
                conn.sendall(response[0].text().encode())
                conn.close()
                response[1]()
        else:
            conn.close()
