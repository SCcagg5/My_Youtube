from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from datetime import datetime
from Source.email.new_user import *

smtp_user =     str(os.getenv('SMTP_USER', None))
smtp_pass =     str(os.getenv('SMTP_PASS', None))
smtp_server =   str(os.getenv('SMTP_SERVER', None))


class Mailer():
    def __init__(self):
        """Open connection to the mail server"""
        self.sender = smtp_user
        self.password = smtp_pass
        print(smtp_user, smtp_pass)
        self.server = smtplib.SMTP_SSL(smtp_server, 465)
        self.server.login(self.sender, self.password)
        self.msg = MIMEMultipart()

    def new_user(self, to, key, timestamp):
        """Send a message to the recipient"""
        date = datetime.fromtimestamp(timestamp)
        self.html = new_header + new_body.format(valid_link = "act_key=" + key.replace("=", "%3D"),
                                                        key = str(key))
        self.to_list = [to]
        self.msg['Subject'] = "Votre inscription youtube"
        self.__send()
        return [True, {}, None]

    def __send(self):
        self.message = ""
        self.msg['From'] = self.sender
        self.msg['To'] = ", ".join(self.to_list)
        self.msg.attach(MIMEText(self.html, 'html'))
        self.msg.attach(MIMEText(self.message, 'plain'))
        self.server.sendmail(self.sender, self.to_list, self.msg.as_string())
        self.__close()
        return


    def __close(self):
        """Close the server connection"""
        self.server.quit()
