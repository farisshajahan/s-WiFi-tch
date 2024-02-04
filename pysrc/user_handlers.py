import time
from machine import Pin
from lib.response import Response

def turn_pin_off_and_wait(pin, timeout):
    gpio_pin = Pin(pin, Pin.OUT)
    gpio_pin.off()
    time.sleep(timeout*60)
    gpio_pin.on()

def default(request):
    timer = None
    print(request.query_params)
    if "timer" in request.query_params.keys():
        timer = request.query_params["timer"]
    response = ""
    if timer:
        #TODO: Jinja for templates
        response = "<body style=\"margin: 0; width: 100vw; height: 100vh; font-family: sans-serif; background-color: #ff5145;\"> <form method=\"get\"><div style=\"display: flex; width: 100%; height: 100%; flex-direction: column; justify-content: center; align-items: center; color: white\"> <h1>WiFi Switch turned on for " + timer + " minute(s)</h1> <div id=\"hide-form\" style=\"display: none; width: 100%; height: 70%; flex-direction: column; justify-content: center; align-items: center; color: black\"> <input type=\"text\" name=\"timer\" required style=\"margin: 1rem; width: 50%; height: 10%; font-size: 2rem; text-align: center; border-radius: 3rem;\" placeholder=\"Enter time in minutes to turn switch on\" /> <input type=\"submit\" value=\"Turn ON\" style=\"width: 30%; height: 10%; font-size: 2rem; border-radius: 3rem; border: none; background-color: black; color: white\" /></div></div> </form><script type=\"text/javascript\">setTimeout(function () {document.getElementById(\"hide-form\").style.display = \"flex\";}, " + str(float(timer)*60*1000) + ")</script></body>"
        return [Response(200, response, {"Content-Type": "text/html", "Connection": "close"}), lambda : turn_pin_off_and_wait(0, float(request.query_params["timer"]))]
    elif request.http_method == "GET":
        response = "<body style=\"margin: 0; width: 100vw; height: 100vh; font-family: sans-serif; background-color: #ff5145;\"> <form method=\"get\"> <div style=\"display: flex; width: 100%; height: 100%; flex-direction: column; justify-content: center; align-items: center;\"> <h1>WiFi Switch</h1> <input type=\"text\" name=\"timer\" required style=\"margin: 1rem; width: 50%; height: 10%; font-size: 2rem; text-align: center; border-radius: 3rem;\" placeholder=\"Enter time in minutes to turn switch on\" /> <input type=\"submit\" value=\"Turn ON\" style=\"width: 30%; height: 10%; font-size: 2rem; border-radius: 3rem; border: none; background-color: black; color: white\" /> </div> </form></body>"
    return Response(200, response, {"Content-Type": "text/html", "Connection": "close"})

handlers = {
    "/": default
}

def get_handlers():
    return handlers