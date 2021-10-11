import os
from http.server import BaseHTTPRequestHandler

from gmail import service_account_login, create_message, send_message

# Email variables. Modify this!
EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_TO = os.environ.get('EMAIL_TO')
EMAIL_SUBJECT = 'Contacto - Nuevo mensaje desde el sitio de {from_name} <{from_email}>'
EMAIL_CONTENT = 'Hello, this is a test siqtal siqtal'
SEND_EMAIL = os.environ.get('EMAIL_SEND_ENABLED')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Send with gmail api"""

        from_name_test = 'test'
        from_email_test = 'test@hmm.com'

        print(self)

        service = service_account_login()
        # Call the Gmail API
        message = create_message(from_email_test, EMAIL_TO, EMAIL_SUBJECT.format(from_name=from_name_test, from_email=from_email_test), EMAIL_CONTENT)
        if SEND_EMAIL.lower() == 'true':
            sent = send_message(service, 'me', message)
            print("Email sent!")

            #TODO errors handling pending

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Email sent!")
        else:
            print("SEND flag is disabled, email not sent")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Email send is disabled")
        return
