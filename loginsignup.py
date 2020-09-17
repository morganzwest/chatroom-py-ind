import re
import requests
import socket
import stdiomask
from colorama import init

import firebase_simple.database_fire as db
from hub import DEVMODE, success_print, error_print, DATABASE, debug_print

init()


class Login:
    def __init__(self):
        self.collation = []
        self.usp = ""
        self.usn = ""
        self.match_path = []

    def login_user_email(self):
        while True:
            self.usn = input("Username or Email: ").strip()
            if len(self.usn) > 0:
                break
            else:
                error_print("Invalid: Blank Field")
        return self.usn

    def login_password(self):
        while True:
            if DEVMODE:
                self.usp = input("Password: ").strip()
            else:
                self.usp = stdiomask.getpass(prompt = "Password: ").strip()
            if len(self.usp) > 0:
                break
            else:
                error_print("Invalid: Blank Field")
        return self.usp

    def login_check(self, username_email, password):
        passwords = []
        # Username check
        data, usernames = DATABASE.load("/users/").get(), []
        match_count = 0

        # Username check explanation
        for userstring in data:
            a = userstring.split(":")
            b = (a[0][:-4], a[0][-4:], a[1], userstring)
            usernames.append(b)

        for user in usernames:
            if user[0] == username_email:
                match_count += 1
                self.match_path.append("/users/"+user[3])

        if len(self.match_path) == 0:  # Input Email
            for userstring in data:
                if userstring.split(":")[1] == db.Db.hash_password(username_email)[:15]:

                    cip = requests.get('https://api.ipify.org').text
                    for ip in DATABASE.load("/variables/ip-banned").get():
                        if ip == cip:
                            return False

                    return True
            return False
        elif len(self.match_path) == 1:  # Only one account with the username
            passwords.append(
                DATABASE.load(
                    self.match_path[0] + "/password"
                ).get())

            return db.Db.check_password(passwords[0], password)
        else:  # Multiple of the same username
            error_print("Please retry with your email instead.")
            self.run()

    def run(self):
        email_username = self.login_user_email()
        password = self.login_password()
        valid = self.login_check(email_username, password)

        self.collation = self.match_path[0] if valid else "Empty path"
        debug_print(self.collation)
        debug_print("Valid:", valid)
        debug_print("Match_path:", self.match_path)

        return self.collation if valid else ""


class Signup:
    def __init__(self):
        self.i = 0
        self.banned = False
        self.username = ""
        self.valid = False
        self.uid = ""

    def signup_email(self, tests = False, raising = True):
        self.i = 0
        while True:
            self.i = 0
            usemail = input("Email: ").strip().lower()
            if len(usemail) > 0:
                self.i += 1
                if usemail[-1] != ".": self.i += 1
            if "@" in usemail: self.i += 1
            if "." in usemail: self.i += 1

            if self.i < 4:
                if tests or raising:
                    raise ValueError("Invalid Email")
                error_print("Invalid Email")
                continue

            for email in DATABASE.load("/variables/emails").get():
                if email == usemail:
                    if tests:
                        raise ValueError("Account already created with the same email.")
                    error_print("Account already created with the same email.")

            break
        return usemail

    def signup_username(self, tests = False):
        while True:
            self.username = input("Username: ").strip()
            if len(self.username) > 0:
                break
            else:
                if tests: raise ValueError("Invalid: Blank Field")
                error_print("Invalid: Blank Field")
        return self.username

    def signup_password(self, tests = False):
        """
        get password from user
        :param tests: unit test skip returns
        :return: str
        """
        fl = 0
        while True:
            if DEVMODE or tests:
                self.uspass = input("Password: ").strip()
            else:
                self.uspass = stdiomask.getpass(prompt = "Password: ").strip()

            fl, error = 0, ""
            if len(self.uspass) < 6:
                fl, error = -1, "Password must be 6 chars or longer."
            if not re.search("[a-z]", self.uspass):
                fl, error = -1, "Password must include a lowercase chars."
            if not re.search("[A-Z]", self.uspass):
                fl, error = -1, "Password must include a capital letter."
            if not re.search("[0-9]", self.uspass):
                fl, error = -1, "Password should include a digit"
            if fl == 0: break
            if fl == -1:
                if tests:
                    raise ValueError("Invalid Password")
                error_print("Invalid Password:", error)
        self.valid = True
        return self.uspass

    def signup_checks(self, cip = ""):
        self.uid = DATABASE.load("/constants/account_count").get()

        if len(str(self.uid)) < 4:
            self.uid = ("0" * (4 - len(str(self.uid)))) + str(self.uid + 1)

        if len(cip) == 0:
            cip = requests.get('https://api.ipify.org').text

        for ip in DATABASE.load("/variables/ip-banned").get():
            self.banned = True if ip == cip else False

        return [self.banned, self.uid]

    def signup_post(self, uid, username, usemail, uspass, banned):
        # DATABASE UPDATE #
        DATABASE.update("/users/" + username + uid + ':' + db.Db.hash_password(usemail)[:15], {
            "uid": uid,
            "identifier": db.Db.hash_password(username + uid + ':' + db.Db.hash_password(usemail)[:15])[:45],
            "username": username,
            "email": usemail,
            "password": db.Db.hash_password(uspass),
            "other-data": {
                "over-banned": banned,
                "local-ip": socket.gethostbyname(socket.gethostname()),
                "external-ip": requests.get('https://api.ipify.org').text,
                "hostname": socket.gethostname()
            }
        })
        DATABASE.update("/constants/", {
            "account_count": int(uid),
            "version": DATABASE.load("/constants/version").get()
        })

        email_list = [usemail]
        for email in DATABASE.load("/variables/emails").get():
            email_list.append(email)

        DATABASE.update("/variables/", {
            "emails": email_list
        })

        success_print("Signed Up Successfully!")

        if banned:
            error_print("IP:", requests.get('https://api.ipify.org').text, "is permanently banned from our service.")
            quit(-5)

    def run(self):
        email = self.signup_email()
        username = self.signup_username()
        password = self.signup_password()
        coll = self.signup_checks()
        banned = coll[0]
        uid = coll[1]

        self.signup_post(uid, username, email, password, banned)