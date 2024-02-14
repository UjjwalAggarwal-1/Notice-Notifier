from full_list import NEW_LIST

SENDER_EMAIL = 'mail.aadmi@gmail.com'
APP_PASSWORD = "your app password here"

ME_LIST = ['f20212427@pilani.bits-pilani.ac.in']

TEST_EMAILS = [
    'f20212427@pilani.bits-pilani.ac.in', #me
]

STUDENT_LIST = [
    'f20212427@pilani.bits-pilani.ac.in', #me
]


SID ='704ab8139a93729779f335c3a8ac0d20' # session cookie for website

COPIED_HEADERS = {
    "Cookie":f"phpbb3_qyzj5_sid={SID}",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

ONBOARD_BASE = 'https://onboard.bits-pilani.ac.in'

IMAGE_SERVER_USER = "" # ubuntu, aws-user, root, etc.

IMAGE_SERVER = '' # ip or domain

SCP_FLAGS = '' # scp flag, like -i key.pem, -P 22, etc.

SERVER_LOC = '~/v1/media' # location on server

with open('data/last_notice.txt','r') as f:
    LAST_NOTICE_URL = f.read()

with open('data/last_post.txt','r') as f:
    LAST_PID = int(f.read())


YES_BOLDIA = [ # people who have responded YES on the google form
"first@pilani.bits-pilani.ac.in",
"second@pilani.bits-pilani.ac.in",
"third@pilani.bits-pilani.ac.in",
]

NO_BOLDIA = [ # people who have responded NO on the google form
"another_first@pilani.bits-pilani.ac.in",
"another_second@pilani.bits-pilani.ac.in",
]

temp_list = list(set(NEW_LIST)-set(NO_BOLDIA)) 
