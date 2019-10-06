import smtplib
import re
from .basicaction import BasicAction

class SendEmailAction(BasicAction):
    """Action to send a Email containing the paste through SMTP protocol to a certain email-id"""
    name = "SendEmailAction"

    def __init__(self, username,password,reciever_email,hostname,port):
        super().__init__()

        if not re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", username) or username is None:
            raise ValueError("username not correct or None!")
        if not re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", reciever_email) or reciever_email is None:
            raise ValueError("reciever_email not correct or None!")
        self.username = username
        self.password =password
        self.reciever_email = reciever_email
        self.hostname = hostname
        self.port = port


    def perform(self, paste, analyzer_name=None):
        address = self.username
        password = self.password
        mailto = self.reciever_email
        msg = 'Subject: {}\n\n{}'.format("From Pastepwn", str(paste))
        mailServer = smtplib.SMTP(self.hostname , self.port)
        mailServer.starttls()
        mailServer.login(address ,password)
        mailServer.sendmail(address, mailto , msg)
        mailServer.quit()
