import httpx, time, json, random, string , itertools
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from lib.mail import TempMail
from lib.console import Console
from lib.captcha import fCaptcha

class Rxddit:
    def __init__(self):
        self.config = json.load(open("./data/config.json", "r+"))
        self.proxies = itertools.cycle(open("./data/proxies.txt").read().splitlines())
        self.temp_mail = TempMail(f"http://{next(self.proxies)}" if self.config['use_proxy'] else None)
        self.email = self.temp_mail.get_mail()
        self.password = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    
    def create_account(self):
        self.options = Options()
        self.options.add_argument("--incognito")
        self.options.add_argument('--start-maximized')
        if self.config["use_proxy"]: 
            self.options.add_argument("--proxy-server=%s" % next(self.proxies))
        if self.config["headless"]:
            self.options.headless = True

        self.browser = uc.Chrome(options=self.options)
        
        try:
            self.browser.get("http://reddit.com/account/register/")
            time.sleep(random.randint(1,5))
            self.browser.find_element(By.ID,'regEmail').send_keys(f"{self.email}")
            self.browser.find_element(By.CSS_SELECTOR, "button.AnimatedForm__submitButton:nth-child(1)").click() 
            time.sleep(random.randint(1,5))
            self.browser.find_element(By.CSS_SELECTOR, "a.Onboarding__usernameSuggestion:nth-child(1)").click() 
            time.sleep(random.randint(1,5))
            self.browser.find_element(By.ID, "regPassword").send_keys(f"{self.password}")
            
            self.browser.find_element(By.CSS_SELECTOR, "button.AnimatedForm__submitButton:nth-child(3)" ).click()
            
            fCaptcha_client = fCaptcha(self.browser, f"http://{next(self.proxies)}" if self.config['use_proxy'] else None)
            fCaptcha_client.solve()
        except Exception as e:
            Console.debug(f"[+] {e}")
            quit()
        
        self.browser.find_element(By.CSS_SELECTOR, "button.AnimatedForm__submitButton:nth-child(3)" ).click()
        with open("./data/account.txt","a", encoding="utf-8") as fp:
            fp.write(f"{self.browser.find_element(By.CLASS_NAME, 'Onboarding__usernameSuggestion').text}:{self.password}\n")
            Console.printf("[+] Account created") 
                    
    def verify_user(self):
        try:
            while True:
                for message in self.temp_mail.load_inbox():
                    if message['from']['address'] == 'noreply@reddit.com':
                        content = self.temp_mail.get_message_content(message['id'])
                        url = f"https://www.reddit.com/api/v1/verify_email/{content.split('https://www.reddit.com/verification/')[1]}"
                        return url
        except Exception as e:
            Console.debug(f"[+] {e}")
            self.verify_user()
               
if __name__ == "__main__":
    client = Rxddit()
    Console.print_logo()
    while True:
        client.create_account()
        httpx.post(client.verify_user(), proxies=f"http://{next(client.proxies)}" if client.config['use_proxy'] else None)
        Console.printf("[>] Email verified")
