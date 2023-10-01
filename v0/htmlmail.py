import requests
from bs4 import BeautifulSoup 
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def send_mail(send_from='email@gmail.com', send_to = ['email@pilani.bits-pilani.ac.in'], subject="NOSUB", text="no text..", files=None,
              server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    # msg['priority'] = 'high'
    # msg['Importance'] = 'high'

    msg.attach(MIMEText(text, 'html'))

    for f in files or []:
        part = MIMEApplication(open(f, 'rb').read())
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(send_from, "APP PASSWORD")
    smtp.sendmail(send_from, send_to, msg.as_string())
    # smtp.close()
    smtp.quit()



headers = {
  'authority': 'onboard.bits-pilani.ac.in',
  # ...
  # ...
}

response = requests.get("https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=7079",headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
content = soup.find("div",class_="content")

# print(content)

str_content = str(content)
str_content = str_content.replace('href="./','href="https://onboard.bits-pilani.ac.in/')
send_mail(text=
          "<html><body>"+str_content+"</body></html>"
         )
print('ok')

