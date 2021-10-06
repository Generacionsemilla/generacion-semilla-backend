from http.server import BaseHTTPRequestHandler
from urllib import parse


class Handler(BaseHTTPRequestHandler):
    def do_get(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        if "name" in dic:
            message = "Hello, " + dic["name"] + "!"
        else:
            message = "Hello, stranger!"

        self.wfile.write(message.encode())
        return
