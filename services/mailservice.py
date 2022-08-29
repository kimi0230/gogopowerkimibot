import smtplib
import os
from decouple import config

smtpObj = smtplib.SMTP(os.environ.get('GMAIL_SMTP'),
                       os.environ.get('GMAIL_TLS_PORT'))
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(os.environ.get('GMAIL_USER'), os.environ.get('GMAIL_PASSWORD'))


def HelloWord():
    smtpObj.sendmail('kimi0x03@gmail.com', 'kimi0230@gmail.com',
                     'Subject: Hello World\nHi Kimi,\nHow are you?')


def SendMail(to, subject, body):
    mailBody = "Subject: %s\n%s" % (subject, body.as_string())
    # print("mailBody --->", config('GMAIL_USER'), mailBody)
    smtpObj.sendmail(s.environ.get('GMAIL_USER'), to,
                     mailBody)


if __name__ == "__main__":
    # HelloWord()
    SendMail('kimi0230@gmail.com', "Hi KK", "Dear Kimi,\nHow are you?")
