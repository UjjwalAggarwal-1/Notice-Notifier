from my_parser import ForumParser, TopicParser
from send_email import EmailWorker
from check import check
import my_secrets as env
from datetime import datetime


if __name__ == "__main__":

    the_recepient_list_being_used = env.ME_LIST

    if not check():
        # error printed through check function
        exit()
    
    fid = 26 # students forum
    # fid = 30 # third year forum

    print("\n>>>>>>")
    print("starting parser at forum ", fid)
    fpar = ForumParser(fid)
    stack = fpar.get_url_list()
    
    if not stack:
        print('\033[92m no new notices \033[00m')
        exit()
    
    print(stack)
    print(f"{len(stack)} new notices found")
    
    print('\n>>>>>>')
    print(f"type yes to send emails to {len(the_recepient_list_being_used)} recepients:", end = " ")
    if input().lower() != "yes":
        print("exiting...")
        exit()
    print("are you sure?", end = " ")
    if input().lower() == "no":
        print("exiting...")
        exit()

    with open('data/last_notice.txt','r') as f:
        last_notice = f.read()
        print(f"{last_notice = }\n")
    with open('data/last_notice.txt','w') as f:
        f.write(stack[-1])

    ew = EmailWorker()

    for topic_url in stack:
        tpar = TopicParser(topic_url)
        tpar.set_content()
        tpar.set_files()
        tpar.handle_attachemnts()
        tpar.scp_files()
        tpar.replace_file_server()
        
        for i in range(len(the_recepient_list_being_used)//100 + 1):
            try:
                ew.send_email(subject = tpar.topic, text = tpar.html, files = tpar.attachments,
                            send_to=the_recepient_list_being_used[i*100:(i+1)*100])
            except Exception as e:
                print(e)
                with open('logs/driver_send_email.txt','a'):
                    f.write(f"{datetime.now()}|{str(e)}\n")

        tpar.delete_files_n_attachments()

    ew.close_smtp()