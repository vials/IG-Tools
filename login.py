#Python3
import requests, uuid, getpass, sys, time
import subprocess as sp
from colorama import Fore, init
init()

def clear():
    sp.call('clear', shell=True)

def login():
    clear()
    myUUID = str(uuid.uuid4())

    nUsername = input('Enter Username: ')
    nPassword = getpass.getpass('Enter Password: ')

    try:
        paramsPost = {"ig_sig_key_version":"5","signed_body":"fa61f4be32e827c7152e38a075e36142d8313ba582d6437f07539b00a03f454e.{\"reg_login\":\"0\",\"password\":\""+nPassword+"\",\"device_id\":\""+myUUID+"\",\"username\":\""+nUsername+"\",\"adid\":\"FE4FD084-9DCB-481A-A248-57E0E32E25ED\",\"login_attempt_count\":\"0\",\"phone_id\":\""+myUUID+"\"}"}
        headers = {"Accept":"*/*","X-IG-Capabilities":"36r/Vw==","User-Agent":"Instagram 82.0.0.17.95 (iPhone9,3; iOS 12_0; en_US; en-US; scale=2.00; gamut=wide; 750x1334) AppleWebKit/420+","Connection":"close","X-IG-ABR-Connection-Speed-KBPS":"0","X-IG-Connection-Speed":"-1kbps","Accept-Encoding":"gzip, deflate","Accept-Language":"en-US;q=1","X-IG-Connection-Type":"WiFi","X-IG-App-ID":"124024574287414","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
        r = requests.post("https://i.instagram.com/api/v1/accounts/login/", data=paramsPost, headers=headers)
        decoded = r.content.decode('utf-8')
        if "logged_in_user" in decoded:
            print('['+Fore.GREEN+'+'+Fore.WHITE+']'+' Successfully Logged In!')
            time.sleep(1)
        elif "invalid_credentials" in decoded:
            print('['+Fore.RED+'-'+Fore.WHITE+']'+' Incorrect Login Information, Try Again.')
            time.sleep(1)
            login()
        elif "challenge_required" in r.decoded:
            print('['+Fore.YELLOW+'!'+Fore.WHITE+']'+' Suspicious Login / Login Issue')
        else:
            print('Couldnt Login! Read Log.')
            print(decoded)
    except Exception as e:
        print(str(e))
        pass
    sys.exit('Successfully Exiting Script.')

if __name__ == '__main__':
    login()
