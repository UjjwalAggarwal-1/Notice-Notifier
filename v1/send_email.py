import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, make_msgid
import my_secrets as env


class EmailWorker:
# by making a class, I just import the class rather than all functions

    def __init__(self) -> None:
        self.instantiate_smtp()

    def instantiate_smtp(self):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(env.SENDER_EMAIL, env.APP_PASSWORD)
        self.smtp = smtp

    def close_smtp(self):
        # can i start a thread to end it if not in use after 5 mins?
        self.smtp.quit()

    def send_email(
            self, 
            send_from=env.SENDER_EMAIL, 
            send_to = env.ME_LIST, 
            subject="DEFAULT SUBJECT", 
            text="no text other than default <br>👍👍 ", 
            files=[], 
            ):

        msg = MIMEMultipart()
        msg['From'] = send_from
        # msg['BCC'] = COMMASPACE.join(send_to)
        # msg['To'] = COMMASPACE.join(send_to)
        # msg['reply-to'] = send_from
        # msg['Cc'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        # msg['Message-id'] = make_msgid(domain = "cognixai.com")
        # msg['priority'] = 'high'
        # msg['Importance'] = 'high'

        ## for normal text
        # msg.attach(MIMEText(text))
        ## for html template
        msg.attach(MIMEText(text, 'html'))

        for f in files:
            part = MIMEApplication(open(f, 'rb').read())
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        self.smtp.sendmail(send_from, send_to, msg.as_string())


    def send_test_email(self, *args, **kwargs):
        self.send_email(send_to=env.ME_LIST, *args, **kwargs)


if __name__=="__main__":
    print("starting test email job")
    ew = EmailWorker()
    ew.send_test_email()
    ew.close_smtp()
    print('test email job completed')