import time, os
from colorama import init, Fore
# Internal Modules
import loginsignup
from hub import *

PREFIX = "/"
ROOM = None
connections = []

init()  # Coloured Prompt


class Connection:
    def __init__(self, path: str):
        self.path = path
        self.identifier = DATABASE.load(self.path + "/identifier").get()
        self.username = DATABASE.load(self.path + "/username").get()
        self.email = DATABASE.load(self.path + "/email").get()
        self.user_id = self.path.split("/")[-1].split(":")[0][-4:]

        a = [self.identifier, self.username, self.email, self.user_id, self.path]
        for i, v in enumerate(a):
            debug_print(i, ":", v)

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
    def loginmenu(connection):
        Hub.clear()
        print(Fore.MAGENTA + "-" * 16, Fore.RESET + "LOGIN MENU" + Fore.MAGENTA, "-" * 16,Fore.RESET)
        print(" " * 16, f"{Fore.GREEN}1.{Fore.RESET}  LOGIN")
        print(" " * 16, f"{Fore.GREEN}2.{Fore.RESET}  SIGNUP")
        print(" " * 16, f"{Fore.GREEN}3.{Fore.RESET}  QUIT")

        while True:
            choice = input("  > ")
            if choice == "1":
                class_ = loginsignup.Login()
                login = class_.run()
                debug_print("Login:", login)
                if login != "":
                    connection.append(Connection(login))
                else:
                    error_print("Invalid Login")
                    Menu.loginmenu(connections)
                break
            elif choice == "2":
                class_ = loginsignup.Signup()
                class_.run()
                break
            elif choice == "3":
                quit(0)
            else:
                error_print("Invalid choice.")


p = Hub()
Menu.loginmenu(connections)
debug_print(connections)
