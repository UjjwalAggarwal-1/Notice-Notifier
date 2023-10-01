# imports
import requests
from bs4 import BeautifulSoup 
import v1.my_secrets as env


BASE = env.ONBOARD_BASE

UNA = "You are not authorised to read this forum."
DNE = "The requested notice does not exist."
LOUT = "The board requires you to be registered and logged in to view this forum."


############### main  #############

url = BASE+f"/viewtopic.php?p="
pid = env.LAST_PID

while True:
    pid += 1
    response = requests.get(url+str(pid),headers=env.COPIED_HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    target_element = soup.select("#page-body")
    
    if len(target_element) == 0:
        print(f"\033[92m Funny, no page body found at {pid} \033[00m")
        continue

    text = target_element[0].text
    
    if UNA in text:
        with open('logs/unauthorised.txt','a') as f:
            f.write(str(pid)+'\n')
        continue

    if DNE in text:
        print(f"\033[92m Last pid found at {pid} \033[00m")
        break

    # valid post (notice)

    #extract info, send mail, update last

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find("div",class_="content")
    topic_title = soup.select("#page-body > h2 > a")[0].text
    with open('logs/valid_post.txt','a') as f:
        f.write(str(pid)+','+topic_title+'\n')
