class InvalidHttpResponseException(Exception):
    pass

class Response:
    valid_http_status_codes = [200]

    def __init__(self, status_code=200, body="", headers={"Content-Type": "text/html", "Connection": "close"}):
        self.status_code = status_code
        self.body = body
        self.headers = headers
        if status_code not in self.valid_http_status_codes or type(headers) != dict or type(body) != str:
            raise InvalidHttpResponseException("Unable to create response object with headers")
        self.response = "HTTP/1.1 " + str(status_code) + " OK\r\n"
        for header in headers.keys():
            self.response += header + ": " + headers[header] + "\r\n"
        self.response += "\r\n"
        self.response += "" if body is None else body
    
    def text(self):
        return self.response
