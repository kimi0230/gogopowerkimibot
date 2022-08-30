import smtplib
import os
from django.conf import settings
from decouple import config


try:
    GMAIL_SMTP = settings.GMAIL_SMTP
    GMAIL_TLS_PORT = settings.GMAIL_TLS_PORT
    GMAIL_USER = settings.GMAIL_USER
    GMAIL_PASSWORD = settings.GMAIL_USER
except:
    GMAIL_SMTP = config('GMAIL_SMTP')
    GMAIL_TLS_PORT = config('GMAIL_TLS_PORT')
    GMAIL_USER = config('GMAIL_USER')
    GMAIL_PASSWORD = config('GMAIL_PASSWORD')

smtpObj = smtplib.SMTP(GMAIL_SMTP, GMAIL_TLS_PORT)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(GMAIL_USER, GMAIL_PASSWORD)


def HelloWord():
    smtpObj.sendmail('kimi0x03@gmail.com', 'kimi0230@gmail.com',
                     'Subject: Hello World\nHi Kimi,\nHow are you?')


def SendMail(to, subject, body):
    mailBody = "Subject: %s\n%s" % (subject, body.as_string())
    smtpObj.sendmail(GMAIL_USER, to,
                     mailBody)


if __name__ == "__main__":
    # HelloWord()
    SendMail('kimi0230@gmail.com', "Hi KK", "Dear Kimi,\nHow are you?")
