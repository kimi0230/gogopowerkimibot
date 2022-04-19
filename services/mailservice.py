import smtplib
from decouple import config

smtpObj = smtplib.SMTP(config('GMAIL_SMTP'), config('GMAIL_TLS_PORT'))
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(config('GMAIL_USER'), config('GMAIL_PASSWORD'))


def HelloWord():
    smtpObj.sendmail('kimi0x03@gmail.com', 'kimi0230@gmail.com',
                     'Subject: Hello World\nHi Kimi,\nHow are you?')


def SendMail(to, subject, body):
    mailBody = "Subject: %s\n%s" % (subject, body)
    smtpObj.sendmail(config('GMAIL_USER'), to,
                     mailBody)


if __name__ == "__main__":
    # HelloWord()
    SendMail('kimi0230@gmail.com', "Hi KK", "Dear Kimi,\nHow are you?")
