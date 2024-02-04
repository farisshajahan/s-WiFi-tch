import network
import time

def wifi_connect_or_ap(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if password == "":
        station.connect(ssid, None)
    else:
        station.connect(ssid, password)
    for i in range(0, 20):
        if station.isconnected():
            break
        time.sleep(1)
    if station.isconnected() == False:
        ssid = 'WifiSwitch-AP'
        password = 'pass123word'
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid, password=password)
        while ap.active() == False:
          pass
        print('Connection successful')
        print(ap.ifconfig())
        print("Received IP: " + station.ifconfig()[0])
    else:
        print("Received IP: " + station.ifconfig()[0])

def get_full_request(conn):
    request = conn.recv(1024).decode()
    post_method = request.find("POST ")
    content_length = ""
    while post_method == 0 and request.find("Content-Length: ") == -1:
            request += conn.recv(1024).decode()
    if post_method == 0:
            content_length = request[request.find("Content-Length: ") + 16: request.find("\r", request.find("Content-Length: "))]
            content_length = int(content_length)
            body_start_index = request.find("\r\n\r\n")
    while post_method == 0 and (body_start_index == -1 or (len(request) - body_start_index - 4) < content_length):
            request += conn.recv(1024).decode()
            body_start_index = request.find("\r\n\r\n")
    return request
