# NOTICE BOARD PARSER

**The parser, does the following, in this order :**

▶️ Go to BITS Pilani's online notice board, get the list of recent notices until the notice last seen
<br>
▶️ Download any images attached in the email, and upload to own server, and repalce image urls with the uploaded image
<br>
▶️ Send an email to all subscribed students

#### The 💖 of the code lies in v1/my_parser.py and v1/send_email.py 

#
#

# To run 🚀 locally
- in v1, make a dir named data and one named logs
    - in data, add files last_notice.txt and last_post.txt
- in v1, make a file named my_secrets.py and add the define variables there, you can find the template in v1/my_secrets_template.py

#
#

## Notes 📝

### /v1
logic from /v0, but arranged properly; _modularized_

### /v0
this was just some code in a single file, doing what was intended

#
#

## Going forth 🎯
* v0/alternate_main.py contains post logic, compared to forum and posts which is being used now

----

* can also update last as the first one this time, traverse next page using notice_start till last is found

---

* if use a cron, lets say every x mins, when getting the list of urls, i can check for the notices posted in last x+1 mins

--- 

* obtaining the session cookie can be automated, not required right now due to long life

#
#

# End of Life 🪦

* the primary purpose of this was to send emails to students, being more convenient, but that's not required anymore as the institute has continued sending notices over email as well

* the scripts, will still work, but not needed for now

# 

🌟 A good script nevethless, had fun building it