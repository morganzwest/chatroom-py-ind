import time, os
from colorama import init, Fore
# Internal Modules
import loginsignup
from hub import DATABASE, DEVMODE, success_print, error_print

PREFIX = "/"
ROOM = None

init()  # Coloured Prompt


class Connection:
    def __init__(self, user_id: str, username: str, email):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.identifier = DATABASE.Db.hash_password(self.username + self.user_id + ':' + db.Db.hash_password(self.email)[:15])[:45]
        self.user_path = "/users/" + self.username + self.user_id + ':' + DATABASE.Db.hash_password(self.email)[:15]

    def connect(self):
        pass


class Hub:
    def __init__(self):
        self.logged = False

    @staticmethod
    def _getdate():
        return time.strftime("%d/%m/%Y", time.localtime())

    @staticmethod
    def _gettime():
        return time.strftime("%H:%M", time.localtime())

    @staticmethod
    def clear():
        os.system("cls")


class Menu:
    @staticmethod
    def loginmenu():
        Hub.clear()
        print(Fore.MAGENTA + "-" * 16, Fore.RESET + "LOGIN MENU" + Fore.MAGENTA, "-" * 16,Fore.RESET)
        print(" " * 16, f"{Fore.GREEN}1.{Fore.RESET}  LOGIN")
        print(" " * 16, f"{Fore.GREEN}2.{Fore.RESET}  SIGNUP")
        print(" " * 16, f"{Fore.GREEN}3.{Fore.RESET}  QUIT")

        while True:
            choice = input("  > ")
            if choice == "1":
                class_ = loginsignup.Login()
                class_.run()
                break
            elif choice == "2":
                class_ = loginsignup.Signup()
                class_.run()
                break
            elif choice == "3": quit(0)
            else:
                error_print("Invalid choice.")


p = Hub()
Menu.loginmenu()
