import json
import os
from http.server import BaseHTTPRequestHandler

from gmail import service_account_login, create_message, send_message

from http.server import BaseHTTPRequestHandler,HTTPServer

#PORT_NUMBER = 8080

# Email variables. Modify this!
#EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_TO = os.environ.get('EMAIL_TO')
EMAIL_SUBJECT = 'Contacto - Nuevo mensaje desde el sitio de {from_name} <{from_email}>'
EMAIL_CONTENT = 'Te contactaron del sitio con el siguiente mensaje: {message}'
SEND_EMAIL = os.environ.get('EMAIL_SEND_ENABLED')

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        content = self.headers.get('Content-Length')
        data = None

        if content:
            content_len = int(content)
            body = self.rfile.read(content_len)
            print(body)
            data = json.loads(body)
            print(data)
            print(data['from_name'])
            print(data['from_email'])
            print(data['message'])


        if SEND_EMAIL and 'true' == SEND_EMAIL.lower():
            if data:
                # Call the Gmail API
                service = service_account_login()
                message = create_message(data['from_email'], EMAIL_TO, EMAIL_SUBJECT.format(from_name=data['from_name'], from_email=data['from_email']), EMAIL_CONTENT.format(message=data['message']))
                sent = send_message(service, 'me', message)

                #TODO errors handling pending

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Email sent!".encode())
            else:
                print("No data")

        else:
            print("SEND flag is disabled, email not sent")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Email send is disabled".encode())
        return

#def run(server_class=HTTPServer, handler_class=handler, port=8080):
#    server_address = ('', port)
#    httpd = server_class(server_address, handler_class)
#    try:
#        httpd.serve_forever()
#    except KeyboardInterrupt:
#        pass
#    httpd.server_close()
#
#if __name__ == '__main__':
#    from sys import argv
#
#    if len(argv) == 2:
#        run(port=int(argv[1]))
#    else:
#        run()