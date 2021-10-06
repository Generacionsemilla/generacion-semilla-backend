# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        message = "api = "+os.environ.get('SENDGRID_API_KEY')
        self.wfile.write(message.encode())
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print(os.environ)
        print(os.environ.get('SENDGRID_API_KEY'))

        return
