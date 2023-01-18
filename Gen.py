import json, httpx, base64, json, sys, string, ssl, time, os, ctypes, threading, random;
from colorama import Fore, init
import ssl; from datetime import datetime;


init();

generated = 0; errors = 0; failed = 0;

 
with open('config.json') as file: config = json.loads(file.read());
with open(config["generator"]["proxy"]["input"]) as file: proxies = file.readlines();

class Logger:
    def CenterText(var:str, space:int=None): # From Pycenter
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())
    
    def Success(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] ({Fore.LIGHTGREEN_EX}+{Fore.WHITE}) {text}')
        lock.release()
    
    def Error(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] ({Fore.RED}-{Fore.WHITE}) {text}')
        lock.release()
    
    def Question(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] ({Fore.YELLOW}?{Fore.WHITE}) {text}')
        lock.release()
    
    def Debug(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] [DEBUG] ({Fore.LIGHTBLUE_EX}*{Fore.WHITE}) {text}')
        lock.release()

if config["generator"]["proxy"]["enabled"]:
    if len(proxies) == 0:
        Logger.Error('Please Input Some Proxies, Then Run The Program...')
        exit()

class Utils(object):
    @staticmethod
    def GenerateBornDate():
        year=str(random.randint(1997,2001));month=str(random.randint(1,12));day=str(random.randint(1,28))
        if len(month)==1:month='0'+month
        if len(day)==1:day='0'+day
        return year+'-'+month+'-'+day
    
    @staticmethod
    def RandomCharacter(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))
    
    @staticmethod
    def GetUsername():
        return httpx.get(f'https://apis.kahoot.it/namerator').json()['name']
    
    @staticmethod
    def GetMail():
        return Utils.RandomCharacter(7) + random.choice(config['account']['emails'])

class CreateAccount():
    def __init__(self):
        global generated, errors, failed

        self.information = {
            "birth_date": Utils.GenerateBornDate(),
            "user_name": Utils.GetUsername(),
            "email": Utils.GetMail(),
            "gender": random.choice([1, 2])
        }

        if config["generator"]["proxy"]["enabled"]:
            self.proxies = "http://" + random.choice(proxies).strip()
        else:
            self.proxies = None
        
        self.session = httpx.Client(proxies=self.proxies, timeout=None, http2=True);

        try:
            self.cookies = self.session.get("https://www.spotify.com/uk/signup/?forward_url=https://accounts.spotify.com/en/status&sp_t_counter=1").cookies
        except:
            self.cookies = None

        
        self.session.headers = {
            'Accept' : '*/*',
            'Accept-Encoding' : 'gzip, deflate',
            'Accept-Language' : 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type' : 'application/json',
            'Host' : 'spclient.wg.spotify.com',
            'Origin' : 'https://www.spotify.com',
            'Referer' : 'https://www.spotify.com',
            'sec-ch-ua' : '" Not A;Brand";v="99", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile' : '?0',
            'sec-ch-ua-platform' : '"Windows"',
            'Sec-Fetch-Dest' : 'empty',
            'Sec-Fetch-Mode' : 'same-site',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        create_account = self.create_account()
        
        if create_account != False:
            access_token = self.get_access_token();
            self.save_account(access_token)
        
        ctypes.windll.kernel32.SetConsoleTitleW(f'[Spotify Generator] - Generated : {generated} | Failed : {failed} | Errors : {errors} | Proxy Enabled : {config["generator"]["proxy"]["enabled"]} | By void.#4848')


    def create_account(self):
        global generated, errors, failed
        try:
            payload = {
                "account_details" : {
                    "birthdate" : self.information['birth_date'],
                    "consent_flags" : {
                        "eula_agreed" : 'true',
                        "send_email" : 'true',
                        "third_party_email" : 'false'
                    },
                    "display_name" : self.information['user_name'],
                    "email_and_password_identifier" : {
                        "email" : self.information['email'],
                        "password" : config['account']['password']
                    },
                    "gender" : str(self.information['gender'])
                },
                "callback_uri" : "https://www.spotify.com/signup/challenge?locale=in-en",
                    "client_info" : {
                    "api_key" : "a1e486e2729f46d6bb368d6b2bcda326",
                    "app_version" : "v2",
                    "capabilities" : [ 1 ],
                    "installation_id" : "fc1e5e8c-1482-450e-b6f3-bd880944c1f3",
                    "platform" : "www"
                   },
                "tracking" : {
                    "creation_flow" : "",
                    "creation_point" : "https://www.spotify.com/in-en/free/?utm_source=in-en_brand_contextual_text&utm_medium=paidsearch&utm_campaign=alwayson_asia_in_premiumbusiness_core_brand_neev+contextual+in-en+google",
                    "referrer" : ""
                }
            }

            response = self.session.post('https://spclient.wg.spotify.com/signup/public/v2/account/create', json=payload, cookies=self.cookies)
        
            if 'success' in response.text:
                Logger.Success(f'Created Account : {self.information["email"]}:{config["account"]["password"]} ({response.json()["success"]["login_token"]})')
                
                self.session.headers['Host'] = 'www.spotify.com';
                self.session.post("https://www.spotify.com/api/signup/authenticate", data=f'splot={response.json()["success"]["login_token"]}')
                return True
            else:
                failed += 1
                Logger.Error(f'Failed To Create Account : {response.status_code}')
                return False
        except Exception as e:
            Logger.Error(e)
            errors += 1
            return False
    
    def get_access_token(self):
        global generated, errors, failed
        try:
            self.session.headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "accept-language": "en",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                "spotify-app-version": "1.1.52.204.ge43bc405",
                "app-platform": "WebPlayer",
                "Host": "open.spotify.com",
                "Referer": "https://open.spotify.com/"
            }

            response = self.session.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player")
            if response.status_code in (200, 201, 204):
                Logger.Debug(f'Access Token : {response.json()["accessToken"][:30]}...')
                return response.json()["accessToken"]
            else:
                failed += 1
                return None
        except Exception:
            return None
    
    def save_account(self, access_token):
        global generated, errors, failed
        with open(config['account']['output'], 'a') as file:
            file.write(f'{self.information["email"]}:{config["account"]["password"]}:{access_token}\n')
            generated += 1
    
def start_thread():
    while True:
        CreateAccount()

for i in range(config['generator']['threads']):
    threading.Thread(target=start_thread).start()