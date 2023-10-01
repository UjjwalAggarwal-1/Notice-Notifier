from my_secrets import NEW_LIST, NO_BOLDIA, YES_BOLDIA

if __name__ == "__main__":

    from my_secrets import *

    print("total list :",len(NEW_LIST),'\n')

    for i in NEW_LIST:
        if not len(i) == len(NEW_LIST[0]):
            print(i, "is not of same length")
            break
    else:
        print('all are of same length\n')


    print("no's :",len(set(NO_BOLDIA)), len(NO_BOLDIA), set(NEW_LIST).intersection(NO_BOLDIA))
    print("yes's :",len(set(YES_BOLDIA)),len(YES_BOLDIA), len(set(NEW_LIST).intersection(set(YES_BOLDIA))))
    print()
    # d = {}
    # for i in YES_BOLDIA:
    #     d[i] = d.get(i, 0) + 1
    # print(d)

    NEW_LIST_2 = list(set(NEW_LIST) - (set(STUDENT_LIST) - set(NO_BOLDIA)))
    print(len(NEW_LIST_2))

    # print(len(set(STUDENT_LIST)), len(STUDENT_LIST))

    # with open ('temp.txt', 'w') as f:
    #     for i in NEW_LIST_2:
    #         f.write(i+'\n')


    # from send_email import EmailWorker
    # NEW_LIST_2 = [
    #     'f20212427@pilani.bits-pilani.ac.in', #me
    # ]

    # ew = EmailWorker()
    # for p in NEW_LIST_2:
    #     ew.send_email(send_to=p, subject="Notice Board Notices' Email", text="""
    # Hello there,

    # I am planning to send emails from the student section of the notice board to everyone, for the convenience of it. Hope you received sample emails just now.

    # I would love it if you could leave a feedback.

    # In case you wish to receive more emails such as this, please reply to the email or mention it in the form.

    # https://forms.gle/rizq81bBCLhMfxKG6
    # """)
        
    # ew.close_smtp()