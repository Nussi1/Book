import threading
from datetime import datetime, timedelta
from random import randint

from django.core.mail import EmailMessage


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


def get_random_passcode():
    from trello.models import ActivationCode

    passcode = randint(100000, 999999)

    while ActivationCode.objects.filter(passcode=passcode, created_date__lte=(datetime.now() + timedelta(days=1))):
        passcode = randint(100000, 999999)

    return passcode
