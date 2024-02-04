class InvalidHttpRequestException(Exception):
    pass

class Request:
    __valid_http_methods = ["GET", "POST", "PUT", "PATCH", "HEAD", "DELETE"]

    def __init__(self, request):
        self.raw_request_string = request
        self.url = None
        self.headers = None
        self.http_method = None
        self.body = None
        if request.find("\r\n") == -1:
            return
        first_line = request[:request.find("\r\n")].split()
        self.http_method = first_line[0]
        if self.http_method not in self.__valid_http_methods:
            raise InvalidHttpRequestException("Unable to parse request: " + request)
        self.url = first_line[1]
        self.query_params = {}
        if "?" in self.url:
            query_params_str = self.url[self.url.find("?") + 1:].split("&")
            self.url = self.url[:self.url.find("?")]
            for param in query_params_str:
                param = param.split("=")
                if len(param) != 2:
                    raise InvalidHttpRequestException("Unable to parse request " + request)
                self.query_params.update({param[0].strip(): param[1].strip()})
        self.headers = {}
        body_start = request.find("\r\n\r\n", request.find("\r\n"))
        if body_start == -1:
            self.headers = {}
        else:
            header_pairs = request[request.find("\r\n") + 2: body_start].replace("\r\n", "\n").split("\n")
            print(header_pairs)
            for header in header_pairs:
                colon_index = header.find(":")
                if colon_index == -1:
                    raise InvalidHttpRequestException("Unable to parse request: " + request)
                self.headers.update({header[:colon_index].strip(): header[colon_index + 1:].strip()})
        if body_start != -1:
            self.body = request[ body_start + 4:]
        else:
            self.body = None
