# -*- coding: utf-8 -*-
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pastepwn.util import TemplatingEngine
from .basicaction import BasicAction


class EmailAction(BasicAction):
    """This action sends out an e-mail to the receiver containing the paste, when executed"""
    name = "EmailAction"

    def __init__(self, username, password, receiver, hostname, port=465, template=None):
        super().__init__()
        mail_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if username is None or not re.match(mail_regex, username):
            raise ValueError("Invalid username !")
        else:
            self.username = username
        if receiver is None or not re.match(mail_regex, receiver):
            raise ValueError("Invalid reciever address !")
        else:
            self.receiver = receiver
        self.password = password
        self.hostname = hostname
        self.port = port
        self.template = template

    def perform(self, paste, analyzer_name=None, matches=None):
        """Sends an email to the specified receiver with the paste's content.
        :param paste: The paste passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the paste
        :param matches: A list of matches, on which the analyzer matched on
        :return: None
        """
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches)

        email = MIMEMultipart()
        email["From"] = self.username
        email["To"] = self.receiver
        email["Subject"] = "Paste matched by pastepwn via analyzer '{}'".format(analyzer_name)
        email.attach(MIMEText(text, "plain"))

        # TODO there should be a way to use starttls - check https://realpython.com/python-send-email/
        with smtplib.SMTP_SSL(self.hostname, self.port) as smtp:
            smtp.login(self.username, self.password)
            text = email.as_string()
            smtp.sendmail(self.username, self.receiver, text)
