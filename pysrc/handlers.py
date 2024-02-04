from lib.response import Response
import machine

def firmware_update(request):
    if request.http_method == "POST":
        boundary = request.headers["Content-Type"].split("boundary=")[1]
        print("\n\n\nBoundary: " + boundary + " End boundary")
        body = request.body
        file_content = body[body.find("\r\n\r\n", body.find("filename=")) + 4: body.find("--" + boundary, body.find("filename="))]
        init_file = open("init.py", "w")
        init_file.write(file_content)
        init_file.close()
        return [Response(), machine.reset]
    elif request.http_method == "GET":
        firmware_update_form = "<div><form action=\"/firmware\" method=\"POST\" enctype=\"multipart/form-data\">Upload new firmware (init.py): <input type=\"file\" name=\"new_init\" /><button onClick=\"refresh()\" type=\"submit\">Submit</button></form></div><script type=\"text/javascript\">async function refresh() {  await new Promise(resolve => setTimeout(resolve, 3000)); window.location.href = \"/\"; } </script>"
        response_body = "<body style=\"margin: 0; width: 100vw; height: 100vh; font-family: sans-serif; background-color: #ff5145;\">" + firmware_update_form + "</body>"
        return Response(200, response_body, {"Content-Type": "text/html", "Connection": "close"})

def wifi_creds_update(request):
    if request.http_method == "POST":
        body = request.body
        print("Body: " + body)
        ssid = body.split("&")[0].split("=", 1)[1].strip().replace("+", " ")
        password = body.split("&")[1].split("=", 1)[1].strip().replace("+", " ")
        wifi_creds_file = open("wifi.cfg", "w")
        wifi_creds_file.write("ssid=" + ssid + "\npassword=" + password)
        wifi_creds_file.close()
        return [Response(), machine.reset]
    elif request.http_method == "GET":
        wifi_creds_file = open("wifi.cfg", "r")
        wifi_creds_lines = wifi_creds_file.read().split("\n")
        wifi_creds_file.close()
        wifi_creds = {}
        for line in wifi_creds_lines:
            wifi_creds[line.split("=", 1)[0]] = line.split("=", 1)[1]
        del wifi_creds_file
        del wifi_creds_lines
        wifi_form = "<div><form action=\"/wifi\" method=\"POST\">SSID: <input type=\"text\" name=\"ssid\" value=\"" + wifi_creds["ssid"] + "\" /> Password: <input type=\"text\" name=\"password\" value=\"" + wifi_creds["password"] + "\" /><button onClick=\"refresh()\" type=\"submit\">Submit</button></form></div><script type=\"text/javascript\">async function refresh() {  await new Promise(resolve => setTimeout(resolve, 3000)); window.location.href = \"/\"; } </script>"
        response_body = "<body style=\"margin: 0; width: 100vw; height: 100vh; font-family: sans-serif; background-color: #ff5145;\">" + wifi_form + "</body>"
        return Response(200, response_body, {"Content-Type": "text/html", "Connection": "close"})