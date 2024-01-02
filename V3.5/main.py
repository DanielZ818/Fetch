"""
Mostly the same as V3, but changed to use selenium instead of request to avoid reply check sum problem
Cookies.txt is replaced by session.pkl (You need to first download the session after login)
"""

import pickle
import re
import time
from typing import List
from colorama import Fore
import PanKit # https://github.com/DanielZ818/Baidu-Pan-Shared-Link/blob/main/PanKit.py
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


class Image:
    def __init__(self, forum_title: str, title: str, id: str, src: str, within_post: str, forum_id: int, raw: bytes):
        self.forum_title = forum_title
        self.title = title
        self.id = id
        self.src = src
        self.within_post = within_post
        self.forum_id = forum_id
        self.raw = raw


def create_driver(headless=False):
    service = Service()
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values': {'images': 2, 'javascript': 2,
                                                        'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications': 2, 'auto_select_certificate': 2,
                                                        'fullscreen': 2,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2,
                                                        'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2,
                                                        'site_engagement': 2,
                                                        'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--disable-extensions")
    if headless:
        options.add_argument('--headless')  # To run the browser in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    return driver


class Driver:
    def __init__(self, domain, session_file, headless=False):
        self.driver = create_driver(headless)
        self.driver.set_page_load_timeout(20)
        self._domain = domain
        self._session_file = session_file
        self._cookie_session = self._load_cookie_session()
        self._load_cookie_to_driver()

    def _load_cookie_session(self):
        # Load cookies from the pickle file
        with open(self._session_file, 'rb') as file:
            saved_session = pickle.load(file)
        return saved_session

    def _load_cookie_to_driver(self):
        # Add cookies to the domain
        self.driver.get(self._domain)
        for cookie in self._cookie_session.cookies.get_dict():
            self.driver.add_cookie({'name': cookie, 'value': self._cookie_session.cookies.get_dict()[cookie]})

    def _save_cookie(self):
        cookies_from_selenium = self.driver.get_cookies()
        for cookie in cookies_from_selenium:
            self._cookie_session.cookies.set(cookie['name'], cookie['value'])  # Update cookies in the session
        with open(self._session_file, 'wb') as file:
            pickle.dump(self._cookie_session, file)

    def get_page(self, url):
        try:
            self.driver.get(url)  # Navigate to a specific page
        except Exception as e:
            print(Fore.RED + "Error: " + str(e).replace('\n', ''))
            print(Fore.RED + "Retrying..." + Fore.RESET)
            self.get_page(url)
        self._save_cookie()

    def find_element(self, by, path):
        return self.driver.find_element(by, path)


class Forum:
    def __init__(self, driver):
        self.driver = driver


    def get_thread(self, tid, reply=False):
        url = f'https://FORUM_URL/thread-{str(tid)}-1-1.html'

        self.driver.get_page(url)
        page = BeautifulSoup(self.driver.driver.page_source, features='html.parser')

        # Free Access Data
        category_xpath = '//*[@id="postlist"]/table[1]/tbody/tr/td[2]/h1/a'
        category = self.driver.find_element(By.XPATH, category_xpath).text

        subject_xpath = '//*[@id="thread_subject"]'
        subject = self.driver.find_element(By.XPATH, subject_xpath).text

        panLink = None
        for a in page.find_all('a', href=True):
            if 'pan.baidu' in a['href']:
                panLink = a['href']
                break

        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        panLink = re.findall(url_regex, panLink)[0][0]

        img = page.find_all("div", class_="mbn savephotop")
        imgs = []
        for i in img:
            i = i.find('img')
            title = i['title']
            id = i['id']
            src = 'https://FORUM_URL/' + i['file']
            raw = requests.get(src).content
            imgs.append(Image(subject, title, id, src, url, tid, raw))

        # Hidden Data
        panPwd = panFileName = panFileSize = panFileMd5 = ''
        panReplied = False
        forumRepliedTime = panFetchTime = -1

        if self.replied(tid):
            print("Already Replied!")
            panReplied = True

            showhide = page.find("div", class_="showhide").text
            panPwd = showhide[-4:]

            panData = PanKit.get_list(PanKit.to_surl(panLink), panPwd)
            panFileName = panData['filename']
            panFileMd5 = panData['md5']
            panFileSize = panData['size']
            panFetchTime = time.time()

        else:
            print("Have not yet replied!")
            if reply:
                message_box_xpath = '//*[@id="fastpostmessage"]'
                message_box_elem = self.driver.find_element(By.XPATH, message_box_xpath)
                message_box_elem.click()
                message_box_elem.send_keys('123456789123456789')

                submit_button_xpath = '//*[@id="fastpostsubmit"]'
                submit_button = self.driver.find_element(By.XPATH, submit_button_xpath)
                submit_button.click()
                forumRepliedTime = time.time()
                print("Replied!")
                time.sleep(2)

                # Go back to main level
                self.driver.driver.refresh()
                time.sleep(1)
                page = BeautifulSoup(self.driver.driver.page_source, features='html.parser')

                showhide = page.find("div", class_="showhide").text
                panPwd = showhide[-4:]
                panReplied = True
                panData = PanKit.get_list(PanKit.to_surl(panLink), panPwd)
                panFileName = panData['filename']
                panFileMd5 = panData['md5']
                panFileSize = panData['size']
                panFetchTime = time.time()

        fetched_data = {
            'category': category,
            'title': category + " " + subject,
            'forumID': tid,
            'forumLINK': url,
            'forumREPLIED': panReplied,
            'forumREPLIEDTIME': forumRepliedTime,
            'panLINK': panLink,
            'panPWD': panPwd,
            'panFILENAME': panFileName,
            'panFILESIZE': panFileSize,
            'panFILEMD5': panFileMd5,
            'panFETCHTIME': panFetchTime,
            'downloaded': False,
            'downloadTIME': None
        }
        return fetched_data, imgs

    def replied(self, tid):
        if str(tid) not in self.driver.driver.current_url:
            url = f'https://FORUM_URL/thread-{str(tid)}-1-1.html'
            self.driver.get_page(url)
        if '查看本帖隐藏内容请' in self.driver.driver.page_source:
            return False
        return True


def process(tid, engine):
    data, imgs = engine.get_thread(tid, reply=True)
    add_entry(data, imgs)
    category, title, panlink, pwd, filename = data['category'], data['title'], data['panLINK'], data['panPWD'], data['panFILENAME']
    print(Fore.CYAN + title + Fore.RESET)
    print(panlink + "?pwd=" + pwd)
    print(filename)
    replied_time = data['forumREPLIEDTIME']
    if time.time() < replied_time + 15:
        print("Reply Cool Down!")
    while time.time() < replied_time + 15:
        pass


def load_url(url_file) -> List[str]:
    """
    :type url_file: file
    :return url_lst: a List[str] of url contained in the file
    """
    file = open(url_file, 'r')
    url_lst = file.read().split('\n')
    while url_lst.count('') != 0:
        url_lst.remove('')
    return url_lst


def to_tid(url_lst):
    tid = []
    for i in url_lst:
        if 'thread-' in i:
            tid.append(str(i).split('-')[1])
        elif 'tid' in i:
            for j in str(i).split('&'):
                if 'tid' in j:
                    tid.append(j.split('=')[1])
    return tid

def main():
    d = Driver("https://FORUM_URL", 'session.pkl', headless=True)
    engine = Forum(d)
    url_lst = load_url('url.txt')
    tid_lst = to_tid(url_lst)
    cur_on = 1
    for tid in tid_lst:
        print(Fore.GREEN + "Current on:", cur_on, "/", len(tid_lst), Fore.RESET)
        process(tid, engine)
        cur_on += 1
        print('=============================================================')


if __name__ == "__main__":
    main()
