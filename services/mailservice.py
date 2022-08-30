import smtplib
import os
from django.conf import settings

smtpObj = smtplib.SMTP(settings.GMAIL_SMTP,
                       settings.GMAIL_TLS_PORT)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(settings.GMAIL_USER, settings.GMAIL_PASSWORD)


def HelloWord():
    smtpObj.sendmail('kimi0x03@gmail.com', 'kimi0230@gmail.com',
                     'Subject: Hello World\nHi Kimi,\nHow are you?')


def SendMail(to, subject, body):
    mailBody = "Subject: %s\n%s" % (subject, body.as_string())
    # print("mailBody --->", config('GMAIL_USER'), mailBody)
    smtpObj.sendmail(settings.GMAIL_USER, to,
                     mailBody)


if __name__ == "__main__":
    # HelloWord()
    SendMail('kimi0230@gmail.com', "Hi KK", "Dear Kimi,\nHow are you?")
