#!/usr/bin/env python3 

# version apanel
VERSION = '1.0'

# modules
import argparse, time, requests, re
from json import loads
from packaging import version
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# argparse
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, help='do scan admin panel')
parser.add_argument('--update', action='store_true', help='check update')
args = parser.parse_args()

# class Apanel
class Apanel:

    # auto run the banner
    def __init__(self) -> None:
        self.Banner()

    # banner apanel
    def Banner(self):
        print("""
                                  .__
_____  ___________    ____   ____ |  |
\__  \ \____ \__  \  /    \_/ __ \|  |
 / __ \|  |_> > __ \|   |  \  ___/|  |__
(____  /   __(____  /___|  /\___  >____/
     \/|__|       \/     \/     \/      
        """)


    # function to validate URL
    def isValidURL(self,str):
    
        # Regex to check valid URL
        regex = ("((http|https)://)(www.)?" +
                "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                "{2,256}\\.[a-z]" +
                "{2,6}\\b([-a-zA-Z0-9@:%" +
                "._\\+~#?&//=]*)")
        
        # Compile the ReGex
        p = re.compile(regex)
    
        # If the string is empty
        if (str == None):
            # return false
            return False
    
        # Return if the string
        # matched the ReGex
        if(re.search(p, str)):
            return True
        else:
            return False

    # this is main function
    def Main(self):
        # check if user do scan admin panel
        if args.url:

            # open the file.txt
            f = open('file.txt', 'r')

            # make variabel url
            url = args.url

            # print starting scanning
            print('\n')
            print("[+]=====STARTING SCANNING=====[+]")
            time.sleep(1)
            print('\n')

            # this mean for starting scanning
            start = time.time()

            # looping the results
            while True:
                try:
                    # read the file.txt
                    panel = f.readline()

                    # if the results has been end
                    if not panel:
                        end = time.time()
                        # give alert
                        print(f'[!] Time taken {end-start:.2f} seconds')
                        break

                    # make variabel req_url 
                    req_url = f"https://{url}/{panel}"

                    # check if URL is valid
                    if(self.isValidURL(req_url) == True):
                        # make request
                        req = Request(req_url)
                        response = urlopen(req)

                        # print the results
                        print(f"[+] {req_url}")

                    # if not valid
                    else:
                        # give alert
                        print("[-] The URL not valid")
                        break

                # this when the results not from file.txt
                # you will see a blank result in the terminal
                except URLError:
                    continue

                # this when user do CTRL-C 
                except KeyboardInterrupt:
                    print("^C")
                    break

        # check if user want to update this tool
        elif args.update:
            # take meta url on github
            META_URL = 'https://raw.githubusercontent.com/galihap76/apanel/main/metadata.json'
            req_meta = requests.get(META_URL, timeout=5)

            # check if status code is 200 that mean success
            if req_meta.status_code == 200:
                # take the version on JSON file
                metadata = req_meta.text
                json_data = loads(metadata)
                version_apanel = json_data['version']

                # if version is new
                if version.parse(version_apanel) > version.parse(VERSION):
                    # give alert
                    print(f'[!] New update available : {version_apanel}')

                    # ask update for user
                    ask_update = input('[!] Do you want to update?[y/n]: ')

                    # if user enter (y) that mean yes
                    if ask_update.lower() == 'y':
                        # give update
                        newVersion = requests.get("https://raw.githubusercontent.com/galihap76/apanel/main/main.py")
                        open("main.py", "wb").write(newVersion.content)
                        print("[+] New version downloaded")
                        print('[!] Apanel will be restarting in 5 seconds...')

                        # and quit in waiting 5 seconds
                        time.sleep(5)
                        quit()

                    # this mean if user not enter (y) 
                    else:
                        pass

                # this mean the tool already up to date
                else:
                    print('[+] Already up to date') 

# run the terminal
if __name__ == '__main__':
    RUN = Apanel()
    RUN.Main()
