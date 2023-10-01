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
    smtp.login(send_from, "asdfasdfasdfasdf")
    smtp.sendmail(send_from, send_to, msg.as_string())
    # smtp.close()
    smtp.quit()

# https://onboard.bits-pilani.ac.in/viewtopic.php?p=6890 no need to use f and t params


BASE = 'https://onboard.bits-pilani.ac.in'

url = BASE+"/viewforum.php?f=26"

payload = {}
headers = {
 ####
}

response = requests.request("GET", url, headers=headers, data=payload)
# print(response.text)
soup = BeautifulSoup(response.text, "html.parser")

target_element = soup.select("#page-body > div.forumbg > div > ul.topiclist.topics > li > dl > dt > div > a.topictitle " )

count = 5
for target in target_element:
    count -= 1
    if count < 0:
        break
    topic_url = (BASE+target.get('href')[1:])
    # topic_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=6884' #image, and lots of newlines
    # topic_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=7071' #drive
    # topic_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=6955' #weird font font written
    
    # https://onboard.bits-pilani.ac.in/viewtopic.php?f=30&t=6811
    # https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=6808
    # ^^ both these are same post
    
    print(topic_url)

    topic_response = requests.request("GET", topic_url, headers=headers, data=payload)
    
    topic_soup = BeautifulSoup(topic_response.text, "html.parser")
    topic_title = topic_soup.select("#page-body > h2 > a")[0].text
    print(topic_title)

    # topic_title = topic_soup.select("#page-body > div.post.has-profile.bg2 > div.inner > div.postbody > div > h5 > a")[0].text
    # print(topic_title)

    topic_content = topic_soup.select("#page-body > div.post.has-profile.bg2 > div.inner > div.postbody > div > div.content")
    # kk = ("\n".join(list(map(str,topic_content))))

    kk = ""
    files = []
    prev_tag = None
    for tag in topic_content:
        # print(tag.text)
        # print(tag)
        # if prev_tag and prev_tag.text == "" and tag.text == "":
        #     continue

        kk += (tag.text.replace("[font]",'\t').replace("[/font]",'\n')) #.replace("\n",'').replace("\t",'').replace("\r",'')) 

        if tag.select('a') and 'drive.google.com' in tag.select('a')[0]['href']:
            kk += tag.select('a')[0]['href'] + '\n'

        elif tag.select('img'):

            if 'http' in tag.select('img')[0]['src']:
                print(tag.select('img')[0]['src'])
                data = requests.get(tag.select('img')[0]['src'],headers=headers).content
                f = open('img.png','wb')
                f.write(data)
                f.close()
                files.append(f.name)
            elif tag.select('img')[0]['src'][0] == '.':
                print(BASE + tag.select('img')[0]['src'][1:])
                data = requests.get(BASE + tag.select('img')[0]['src'][1:],headers=headers).content
                f = open('img.png','wb')
                f.write(data)
                f.close()
                files.append(f.name)
            else:
                print(tag.select('img')[0]['src'])
                print("Unknown case")

        prev_tag = tag
            
    # print(kk)
    break

    # print(files, kk)
    # send_mail(files = files, subject = topic_title, text = kk)
    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login("", "kljlkjlkjl")
    # message = "Subject: {}\n\n{}".format(topic_title, kk).encode("UTF-8")
    # s.sendmail(".@gmail.com", "bits-pilani.ac.in", message)
    # s.quit()
    # print()
    # break

