import requests
from bs4 import BeautifulSoup
import my_secrets as env

def check():
    print("\n>>>>>>")
    print("starting checker...")

    response = requests.get(env.ONBOARD_BASE+"/index.php",headers=env.COPIED_HEADERS)
    print(f'{response.status_code = }')
    soup = BeautifulSoup(response.text, "html.parser")

    target_element = soup.select("#page-body")

    if not target_element:
        print(f"\033[92m Funny, no page-body found at index \033[00m")
        return False
    
    text = target_element[0].text

    login_message = 'To view the Notices, please login through your BITS Email ID.'
    if login_message in text:
        print("\033[91m\033[45m HOLY SHIT login again \033[00m")
        return False
    
    print('\033[93m\033[44m checks passed \033[00m')
    return True

if __name__ == "__main__":
    check()