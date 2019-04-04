import requests, uuid, getpass, sys, json, time
import subprocess as sp
from colorama import Fore, init
init()

def clear():
    sp.call('clear', shell=True)

def login():
    clear()
    global myUUID, mySessionID, myCSRF, myMID, myDS_USER, myDS_USER_ID
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
            myCSRF = r.cookies['csrftoken']
            myDS_USER = r.cookies['ds_user']
            myDS_USER_ID = r.cookies['ds_user_id']
            mySessionID = r.cookies['sessionid']
            myMID = r.cookies['mid']
            time.sleep(1)
            getChats()
        elif "invalid_credentials" in decoded:
            print('Incorrect Login Information, Try Again.')
            time.sleep(1)
            login()
        elif "challenge_required" in r.decoded:
            print('Suspicious Login / Login Issue')
            sys.exit()
        else:
            print('Couldnt Login! Read Log.')
            print(decoded)
            sys.exit()
    except Exception as e:
        print(str(e))
        pass


myDMList = []
def getChats():
    clear()
    try:
        print('['+Fore.YELLOW+'!'+Fore.WHITE+']'+' Grabbing All Available Chats')
        paramsGet = {"persistentBadging":"true","use_unified_inbox":"true"}
        headers = {"Accept":"*/*","X-IG-Capabilities":"36r/dw==","User-Agent":"Instagram 82.0.0.14.178 (iPhone9,3; iOS 12_0; en_US; en-US; scale=2.00; gamut=wide; 750x1334) AppleWebKit/420+","Connection":"close","X-IG-ABR-Connection-Speed-KBPS":"0","X-IG-Connection-Speed":"14924kbps","Accept-Encoding":"gzip, deflate","Accept-Language":"en-US;q=1","X-IG-Connection-Type":"WiFi","X-IG-App-ID":"124024574287414"}
        cookies = {"ds_user":myDS_USER,"ds_user_id":myDS_USER_ID,"mid":myMID,"sessionid":mySessionID,"csrftoken":myCSRF,"rur":"ATN"}
        r = requests.get("https://i.instagram.com/api/v1/direct_v2/inbox/", params=paramsGet, headers=headers, cookies=cookies)

        DMCount = True
        myCounter = 0
        while DMCount:
            for i in r.content.decode('utf-8').split(':'):
                if "thread_id" in i:
                    myID = r.json()['inbox']['threads'][myCounter]['thread_id']
                    myCounter += 1
                    myDMList.append(myID)
                else:
                    '''Do nothing'''
            print('['+Fore.GREEN+'+'+Fore.WHITE+'] '+str(myCounter)+' Available Chats')
    except Exception as l:
        pass
    clearChats()
    DMCount = False

def updateChats():
    try:
        print('['+Fore.YELLOW+'!'+Fore.WHITE+']'+' Updating Chat List')
        paramsGet = {"persistentBadging":"true","use_unified_inbox":"true"}
        headers = {"Accept":"*/*","X-IG-Capabilities":"36r/dw==","User-Agent":"Instagram 82.0.0.14.178 (iPhone9,3; iOS 12_0; en_US; en-US; scale=2.00; gamut=wide; 750x1334) AppleWebKit/420+","Connection":"close","X-IG-ABR-Connection-Speed-KBPS":"0","X-IG-Connection-Speed":"14924kbps","Accept-Encoding":"gzip, deflate","Accept-Language":"en-US;q=1","X-IG-Connection-Type":"WiFi","X-IG-App-ID":"124024574287414"}
        cookies = {"ds_user":myDS_USER,"ds_user_id":myDS_USER_ID,"mid":myMID,"sessionid":mySessionID,"csrftoken":myCSRF,"rur":"ATN"}
        r = requests.get("https://i.instagram.com/api/v1/direct_v2/inbox/", params=paramsGet, headers=headers, cookies=cookies)

        DMCount = True
        myCounter = 0
        while DMCount:
            for i in r.content.decode('utf-8').split(':'):
                if "thread_id" in i:
                    myID = r.json()['inbox']['threads'][myCounter]['thread_id']
                    myCounter += 1
                    myDMList.append(myID)
                else:
                    '''Do Nothing'''
            print('['+Fore.GREEN+'+'+Fore.WHITE+'] '+str(myCounter)+' Available Chats')
            if myCounter == 0:
                sys.exit('Successfully Cleared DMs')
    except Exception as l:
        pass

def clearChats():
    deletedDMS = 0
    confirmClear = input('['+Fore.YELLOW+'!'+Fore.WHITE+']'+' Would You Like To Delete '+str(len(myDMList))+' Chat(s) [y/n]: ')
    if confirmClear.upper() == 'N' or confirmClear.upper() == "NO":
        sys.exit()
    else:
        clearDM = True
        while clearDM:
            for i in range(len(myDMList)):
                try:
                    paramsPost = {"_uuid":myUUID,"_csrftoken":myCSRF,"use_unified_inbox":"true"}
                    headers = {"Accept":"*/*","X-IG-Capabilities":"36r/dw==","User-Agent":"Instagram 82.0.0.14.178 (iPhone9,3; iOS 12_0; en_US; en-US; scale=2.00; gamut=wide; 750x1334) AppleWebKit/420+","Connection":"close","X-IG-ABR-Connection-Speed-KBPS":"0","X-IG-Connection-Speed":"471kbps","Accept-Encoding":"gzip, deflate","Accept-Language":"en-US;q=1","X-IG-Connection-Type":"WiFi","X-IG-App-ID":"124024574287414","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
                    cookies = {"urlgen":"\"{\\\"1.3.3.7\\\": 7922}:1hBpwV:rAqS0L7vKp0qUt1Mf-rcO8QwZ2w\"","ds_user":myDS_USER,"ds_user_id":myDS_USER_ID,"mid":myMID,"sessionid":mySessionID,"csrftoken":myCSRF,"rur":"ATN"}
                    r = requests.post("https://i.instagram.com/api/v1/direct_v2/threads/"+myDMList[i]+"/hide/", data=paramsPost, headers=headers, cookies=cookies)
                    if "Please wait a few minutes before you try again" r.content.decode('utf-8'):
                        print('Sleeping For 5 Minutes...')
                        time.sleep(300)
                    elif '{"status": "ok"}' in r.content.decode('utf-8'):
                        deletedDMS += 1
                        print('['+Fore.GREEN+'+'+Fore.WHITE+']'+' Deleted '+str(deletedDMS)+' Chat(s)')
                        myDMList.remove(myDMList[i])
                    else:
                        print('['+Fore.RED+'-'+Fore.WHITE+']'+' Couldnt Remove ID From List: '+str(myDMList[i]))
                    if len(myDMList) == 0:
                        updateChats()
                except Exception as f:
                    pass

if __name__ == '__main__':
    login()
