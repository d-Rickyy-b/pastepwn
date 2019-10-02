# -*- coding: utf-8 -*-
from .basicaction import BasicAction
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailAction(BasicAction):
    """This action takes a username, password, receiver mail address,
    hostname, port and when executed sends out a an
     e-mail to the receiver containing the paste."""

    name = "EmailAction"

    def __init__(self, username, password, receiver, hostname, port):
        super().__init__()
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", username) or username is None:
            raise ValueError('Invalid username !')
        else:
            self.username = username
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", receiver) or receiver is None:
            raise ValueError('Invalid reciever address !')
        else:
            self.receiver = receiver
        self.password = password
        self.hostname = hostname
        self.port = port

    def perform(self, paste):
        email = MIMEMultipart()
        email['From'] = self.username
        email['To'] = self.receiver
        email['Subject'] = 'Paste sent from pastepwn'
        email.attach(MIMEText(paste, 'plain'))
        session = smtplib.SMTP(self.hostname, self.port)
        session.starttls()
        session.login(self.username, self.password)
        text = email.as_string()
        session.sendmail(self.username, self.receiver, text)
        session.quit()
        print('Email sent to {0}'.format(self.receiver))
