import requests
from colorama import Fore, init
init()

reqLink = input('Enter RAW Pastebin URL: ')

gayUsers = []

with open('gayUsers.txt', 'r') as f:
    for line in f:
        for user in line.split():
            gayUsers.append(user)

def gayAuth():
    print('Welcome To Gay Auth')
    print('-'*20)

    r = requests.get(reqLink)
    for i in r.content.decode('utf-8').split():
        if i in gayUsers:
            print('['+Fore.GREEN+'+'+Fore.WHITE+']'+' Authenticated Gay User')
        else:
            print('['+Fore.RED+'-'+Fore.WHITE+']'+' Failed To Authenticate Gay User')

if __name__ == '__main__':
    gayAuth()
#I had to do it if all the other C+P Auth turbo people were doing it
