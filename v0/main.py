# imports
import requests
from bs4 import BeautifulSoup 
import v1.my_secrets as env
import re
import uuid
import os


BASE = env.ONBOARD_BASE
IMAGE_SERVER = env.IMAGE_SERVER
FORUM_ID = 26
NOTICE_START = 0

############### get the list of urls  #############

url = BASE+f"/viewforum.php?f={FORUM_ID}&start={NOTICE_START}"
print(url)
response = requests.get(url,headers=env.COPIED_HEADERS)
print(response.status_code)
soup = BeautifulSoup(response.text, "html.parser")

target_element = soup.select("#page-body > div.forumbg > div > ul.topiclist.topics > li > dl > dt > div > a.topictitle ")

stack = []
for target in target_element:
    topic_url = (BASE + target.get('href')[1:]) # remove the first dot (.) in the href link
    
    # check if the url is for a old notice
    if topic_url == env.LAST_NOTICE_URL: 
        # this should be changed to post id logic
        break
    stack.append(topic_url)
stack.reverse()


def remove_unwanted_tags(html):
    html = html.replace('[font]','')
    html = html.replace('[/font]','')
    
    return html

def replace_image_logic(html):
    return
    ## not correct
    files = get_image_files_logic(html)
    for k,i in enumerate(files):
        # api to store and return the urls
        html.replace(f'img{k}.png',f'{IMAGE_SERVER}/backend-media/{i}')
    return html

def get_image_files_logic(html):
    files = []
    found = re.findall(r'<img.*src=[\"\']\..+>', html)
    for inst in found: # inst for instance
        m = re.search(r'src=[\"\'](.+)[\"\']', inst)
        if not m:
            message = "No image found in the given url!!"
            print(f"\033[91m {message}\033[00m")
            continue
        # print(m.group(0))
        print(m.group(1))
        l = m.group(1).replace("./", BASE+"/")
        print(l)
        # should i put a try catch here? it can fail, but i'll have traceback
        data = requests.get(l, headers=env.COPIED_HEADERS).content
        with open(f'img{uuid.uuid4()}.png','wb') as f:
            f.write(data)
        files.append(f.name)
    return files


# for a url(a notice), get that notice's content
def get_html_content(url):
    response = requests.get(url,headers=env.COPIED_HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find("div",class_="content")
    topic_title = soup.select("#page-body > h2 > a")[0].text

    str_content = str(content)
    # str_content = remove_unwanted_tags(str(content))

    html_content = "<html><body>"+str_content+"</body></html>"
    return topic_title, html_content

def delete_files(files):
    for f in files:
        os.remove(f)

########## main #############

# print(stack)
# smtp = instantiate_smtp()
# for topic_url in stack:
#     title, html_content = get_html_content(topic_url)
#     files_ = get_image_files_logic(html_content)
#     send_mail(
#         smtp_instance=smtp,
#         text=remove_unwanted_tags(html_content),
#         subject=title, 
#         files = files_
#     )
#     delete_files(files_)
# close_smtp(smtp)


########  to do  ############

# also,
# update last as the first one this time
# traverse next page using notice_start till last is found

# if i attach images, gdrive will be used, but locally i can delete
##### why not just delete the mails??
# to avoid this, i can upload on server, but then not delete them

# experiment with headers
# experiment specially with cookies

# if use a cron, lets say every x mins
# when getting the list of urls, i can check for the notices posted in last x+1 mins



#############   test    #############
## test particular url
# test_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=6884'
# sub,html = get_html_content(test_url)

# print(sub)
# print(html)
# send_mail(
#     text=remove_unwanted_tags(html),
#     subject=sub,
#     # files = get_image_files_logic(html)
# )
# print('------------------')
# print(remove_unwanted_tags(html))
# print('------------------') 
# print(image_logic(html))
# print('------------------')
# print(get_image_files_logic(html))