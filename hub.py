import firebase_simple.database_fire as db
from colorama import Fore, Back, Style, init

DATABASE = db.Db("https://chatroom-multiuser.firebaseio.com/", "key.json")
DEVMODE = True


def error_print(*args):
    result = ""
    for arg in args:
        result += " " + arg
    print(Fore.RED, result.strip(), Fore.RESET)


def success_print(*args):
    result = ""
    for arg in args:
        result += " " + arg
    print(Fore.GREEN, result.strip(), Fore.RESET)


def debug_print(*args):
    if DEVMODE:
        result = ""
        for arg in args:
            result += " " + str(arg)
        print(Fore.CYAN, result.strip(), Fore.RESET)
