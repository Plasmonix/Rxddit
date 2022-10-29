import httpx, time, random, subprocess
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .console import Console

class fCaptcha:
    def __init__(self, browser, proxy: str=None, timeout: int=10):
        self.browser = browser
        self.client = httpx.Client(timeout=timeout, proxies=proxy)
        
    def download_audio(self, url, file_name):
        bytes = self.client.get(url).content
        with open(f"audio/{file_name}.mp3", "wb") as f:
            f.write(bytes)
        time.sleep(2)
        self.convert_mp3_to_wav(file_name)
        audio_text = self.speech_recognition(file_name)
        return audio_text
    
    def speech_recognition(self, file_name):
        r = sr.Recognizer()
        with sr.AudioFile(f"audio/{file_name}.wav") as source:
            audio = r.record(source)
        try:
            s = r.recognize_google(audio)
            return s
        except Exception as e:
            Console.debug("[~] Error Decoding Audio")
            quit()
    
    def convert_mp3_to_wav(self, file_name=None):
        try:
            subprocess.call(['ffmpeg', '-i', f"audio/{file_name}.mp3", f"audio/{file_name}.wav"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            Console.debug("[~] ffmpeg is not installed")
            quit() 
        
    def solve(self):
        try:
            WebDriverWait(self.browser, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='reCAPTCHA']")))
            WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
            self.browser.switch_to.default_content()
        except Exception as e:
            Console.debug("[~] Error Locating Recaptcha")
            quit() 
        try:
            self.browser.switch_to.frame(self.browser.find_elements(By.XPATH, "/html/body/div[2]/div[4]/iframe")[0])
            WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button'))).click()
            download_link = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[7]/a'))).get_attribute('href')
            Console.printf(f"[*] Retrieved Recaptcha Audio Challenge")
        except Exception as e:
            Console.debug("[~] Ratelimited")
            quit() 
        try:
            audio_text = self.download_audio(download_link, f"recaptcha{random.randint(1, 500000)}{download_link[len(download_link)-15]}")
            WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[6]/input'))).send_keys(audio_text)
            WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[8]/div[2]/div[1]/div[2]/button'))).click()
            self.browser.switch_to.default_content()
            Console.printf(f"[~] Solved Recaptcha")
        except Exception as e:
            Console.debug("[~] Error Sumbitting Recaptcha Answer")
            quit()
        return None
