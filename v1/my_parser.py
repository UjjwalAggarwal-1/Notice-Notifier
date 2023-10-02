import requests
from bs4 import BeautifulSoup 
import my_secrets as env
import re
import uuid
import os
from send_email import EmailWorker
import time
from datetime import datetime


BASE = env.ONBOARD_BASE

class TopicParser:

    def __init__(self, url) -> None:
        self.url:str = url
        self.topic:str = None 
        self.html:str = None
        self.attachments_html:str = None
        self.files = []
        self.attachments = []


    # for a url(a notice), get that notice's content
    def set_content(self):
        response = requests.get(self.url,headers=env.COPIED_HEADERS)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        topic_title = soup.select("#page-body > h2 > a")[0].text
        self.topic = topic_title
        
        content = soup.find("div",class_="content")
        str_content = str(content)
        
        form_message = "<br><br><i> would 💖 it if you could leave a <a href = 'https://forms.gle/rizq81bBCLhMfxKG6'>feedback</a></i>"

        self.html = "<html><body>"+str_content+form_message+"</body></html>"
        self.remove_unwanted_tags()

        self.attachments_html = str(soup.find("dl",class_="attachbox"))

        

    def remove_unwanted_tags(self):
        self.html = self.html.replace('[font]','')
        self.html = self.html.replace('[/font]','')
        

    def set_files(self):
        print('setting files')
        print('setting files....')
        files = []
        found = re.findall(r'<[^>]*=[\"\']\.\/download[^>]+>', self.html)
        # print(found)
        for inst in found: # inst for instance
            m = re.search(r'=[\"\']\.\/download[^>]+>', inst)
            
            if not m:
                message = f"No file found in the given url {self.url}"
                with open('logs/no_file_re.txt','a') as f:
                    f.write(f"{datetime.now()}|{message}\n")
                return 
            
            if "postlink" in inst:
                ftype = "pdf"
            elif 'postimage' in inst:
                ftype = "png"
            else:
                message = f"No file found in the given url {self.url}"
                with open('logs/no_file_class_re.txt','a') as f:
                    f.write(f"{datetime.now()}|{message}\n")
                return 

            print(m.group(0))
            # print(m.group(1))
            l = m.group(0)[2:-2].replace("./", BASE+"/")
            # print(l)
            
            try:            
                data = requests.get(l, headers=env.COPIED_HEADERS).content
            except:
                message = f"file not found at {l}"
                with open('logs/no_file_request.txt','a') as f:
                    f.write(f"{datetime.now()}|{message}\n")
                
                continue
                
            with open(f'{ftype}_{uuid.uuid4()}.{ftype}','wb') as f:
                f.write(data)
            files.append(f.name)

        print(f'{files = }')
        self.files = files


    def replace_file_server(self):
        if not self.files:
            return
        print("replacing files uri's....")
        found = re.findall(r'<[^>]+=[\'\"]\.\/download[^>]*>', self.html)
        print(found, self.files)
        for inst in zip(found, self.files): # inst for instance
            if inst[1].startswith('png_'):
                self.html = self.html.replace(inst[0], f"<img style=\"width: 100%; height: auto;\" src='http://{env.IMAGE_SERVER}/media/{inst[1]}'" )     
            elif inst[1].startswith('pdf_'):
                self.html = self.html.replace(inst[0], f"<a href='http://{env.IMAGE_SERVER}/media/{inst[1]}'>" )
            else:
                print("error in replacing file server")
                print(inst)
                exit()

    
    def scp_files(self):
        for f in self.files:
            os.system(f"scp {env.SCP_FLAGS} ./{f} {env.IMAGE_SERVER_USER}@{env.IMAGE_SERVER}:{env.SERVER_LOC}")
        

    def delete_files_n_attachments(self):
        for f in self.files:
            os.remove(f)
        for f in self.attachments:
            os.remove(f)


    def handle_attachemnts(self):
        print("handling attachments....")
        files = []
        found = re.findall(r'<a ?[^>]+=[\'\"]\.\/download[^<]*</a>', self.attachments_html)
        print(found)
        for inst in found: # inst for instance
            m = re.search(r'=[\"\']\.\/download[^>]+>', inst)
            namem = re.search(r'>[^<]+</a>', inst)

            if not (m or namem):
                message = f"No link/file name matched in the given url attachments {self.url}"
                with open('logs/no_attachments_re.txt','a') as f:
                    f.write(f"{datetime.now()}|{message}\n")
                return 

            l = m.group(0)[2:-2].replace("./", BASE+"/")
            print(l)
            print(namem.group(0)[1:-4])
            
            try:            
                data = requests.get(l, headers=env.COPIED_HEADERS).content
            except:
                message = f"file not found at {l}"
                with open('logs/no_attach_request.txt','a') as f:
                    f.write(f"{datetime.now()}|{message}\n") 
                continue
                
            with open(f'{namem.group(0)[1:-4].replace(" ","_")}','wb') as f:
                f.write(data)
            files.append(f.name)

        print(f"attachement {files = }")
        self.attachments = files

class ForumParser:
    forum_url = f"/viewforum.php"

    def __init__(self,forum_id:int) -> None:
        self.fid = forum_id
        self.update_page_start()
    
    def set_forum_url(self):
        url = BASE+f"{ForumParser.forum_url}?f={self.fid}&start={self.start}"
        self.url = url

    def update_page_start(self, start:int = 0):
        self.start = start
        self.set_forum_url()

    def get_url_list(self):
        response = requests.get(self.url,headers=env.COPIED_HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        target_element = soup.select("#page-body > div.forumbg > div > ul.topiclist.topics > li > dl > dt > div > a.topictitle ")

        stack = []
        for target in target_element:
            topic_url = BASE + target.get('href')[1:] # remove the first dot (.) in the href link
            
            if topic_url == env.LAST_NOTICE_URL: 
                break
            stack.append(topic_url)
            time.sleep(0.5)
        stack.reverse()

        return stack




#############   test    #############

if __name__ == "__main__":

    print("enter '1' for testing the test url ▶️ ", end = " ")

    ## test particular url
    if not input() == "1":
        print('exiting...')
        exit()
        
    print('testing out the test url')
    
    # test_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=6884' #image, and lots of newlines
    # test_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=7071' #drive
    # test_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=6955' #weird font font written
    # test_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=7211' # pdf link
    test_url = 'https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=7247' # docx file link

    # https://onboard.bits-pilani.ac.in/viewtopic.php?f=30&t=6811
    # https://onboard.bits-pilani.ac.in/viewtopic.php?f=26&t=6808
    # ^^ both these are same post

    print(test_url)
    parser = TopicParser(test_url)

    ## 🔽 attachemnts

    # parser.set_content()
    # parser.set_image_files()

    # ew = EmailWorker()
    # ew.send_test_email(subject = parser.topic, text = parser.html, files = parser.files)
    # ew.close_smtp() 
    # parser.delete_files()


    ## 🔽 scp

    parser.set_content()
    parser.set_files()
    parser.handle_attachemnts()
    parser.scp_files()
    parser.replace_file_server()

    ew = EmailWorker()
    ew.send_test_email(subject = parser.topic, text = parser.html, files = parser.attachments)
    ew.close_smtp()

    parser.delete_files_n_attachments()
