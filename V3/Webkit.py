"""
A libaray with classes to make request to the Discuz! Forum
"""

import time
import urllib.parse
import pyperclip
from bs4 import BeautifulSoup
import requests
from colorama import Fore
import PanKit # Same as https://github.com/DanielZ818/Baidu-Pan-Shared-Link/blob/main/PanKit.py

def parse_response_cookie(response_header):
    """
    This function will get response cookie from header
    :param response_header: BeautifulSoup Object.headers
    :return: list of cookie [(cookie1_name, cookie1_val), (cookie2_name, cookie2_val)]
    """
    response_cookie_raw = response_header['Set-Cookie'].split('; ')
    response_cookie = []
    for i in response_cookie_raw:
        i = i.replace("secure, ", '')
        if 'P6Pf' in i:
            response_cookie.append((i.split('=')[0], i.split('=')[1]))
    return response_cookie


def parse_url_into_tid(url):
    for x in url.split('&'):
        if 'tid' in x:
            return x[4::]


class Forum:
    def __init__(self, cookie_file, headers):
        self.cookie_expire = None
        self.error = []
        # Initialize cookie data
        self.cookie_file = cookie_file
        cookie_file = open(cookie_file, 'r')
        cookie_list = cookie_file.read()
        cookie_file.close()
        self.cookies = {}
        cookie_list = cookie_list.split("; ")
        for i in cookie_list:
            i.split("=")
            self.cookies[i.split('=')[0]] = i.split('=')[1]

        # Set global headers
        headers = headers.split("\n")
        self.headers = {}
        for i in headers:
            self.headers[i.split(": ")[0]] = i.split(": ")[1]

    def save_cookie(self):
        """
        This function will write cookie dictionary into cookie.txt
        :return: none
        """
        cookie_raw = ''
        for key in self.cookies:
            cookie_raw += key + "=" + self.cookies[key] + "; "
        cookie_raw = cookie_raw[:-2]
        cookie_file = open(self.cookie_file, "w")
        cookie_file.write(cookie_raw)
        cookie_file.close()

    def update_cur_cookie(self):
        """
        This function will combine and update the current cookie dict with stored ones
        :return: None
        """
        cookie_file = open(self.cookie_file, 'r')
        cookie_list = cookie_file.read()
        cookie_file.close()
        cookie_list = cookie_list.split("; ")
        for i in cookie_list:
            i.split("=")
            self.cookies[i.split('=')[0]] = i.split('=')[1]

    def write_to_current_cookie(self, cookie_list):
        """
        This function will combine cookie_list into cookie dict
        :param cookie_list: [(cookie1_name, cookie1_val), (cookie2_name, cookie2_val)]
        :return: None
        """
        for i in cookie_list:
            cookie_name = i[0]
            cookie_val = i[1]
            self.cookies[cookie_name] = cookie_val

    def get_page(self, url) -> BeautifulSoup:
        """
        This returns the html of the url
        :param url:
        :return: Beautiful Soup Object
        """
        # Update self.cookie using cookie.txt
        self.update_cur_cookie()

        # Request the page
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        response_header = response.headers
        html = response.content.decode('utf-8')

        # Get response cookie
        response_cookie_list = parse_response_cookie(response_header)

        # Update cookie dictionary
        self.write_to_current_cookie(response_cookie_list)

        # Update cookie.txt with response cookie added
        self.save_cookie()

        # Get cookie expiration
        cookie_expire_unformat = response_header['Set-Cookie'].split('; ')
        cookie_expire = []
        for i in cookie_expire_unformat:
            if "expire" in i:
                cookie_expire.append(i.replace('expires=', ''))
        self.cookie_expire = cookie_expire
        # Expiration Stored in cookie_expire

        return BeautifulSoup(html, features='html.parser')

    def reply(self, tid):
        """
        Reply to post
        :param tid: int: ex 42136
        :return: none
        """
        fid = '37'
        url = "https://FORUM_URL/forum.php"
        data = {
                'mod': 'post',
                'infloat': 'yes',
                'action': 'reply',
                'fid': '37',
                'extra': '',
                'tid': str(tid),
                'replysubmit': 'yes',
                'inajax': '1',
                }
        form_data = {
            'formhash': '93cba78e',
            'handlekey': 'reply',
            'noticeauthor': '',
            'noticetrimstr': '',
            'noticeauthormsg': '',
            'usesig': '0',
            'subject': '',
            'message': '123456789123456789'
        }

        self.update_cur_cookie()

        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        r_cookie_list = parse_response_cookie(r.headers)
        self.write_to_current_cookie(r_cookie_list)
        self.save_cookie()
        self.update_cur_cookie()

        response = requests.post(url, headers=self.headers, params=data, cookies=self.cookies, data=form_data)
        print(response.text)
        response_header = response.headers
        response_cookie_list = parse_response_cookie(response_header)
        self.write_to_current_cookie(response_cookie_list)
        self.save_cookie()
        # response_cookie_expiration = xxx


class Image:
    def __init__(self, forum_title: str,  title: str, id: str, src: str, within_post: str, forum_id: int, raw: bytes):
        self.forum_title = forum_title
        self.title = title
        self.id = id
        self.src = src
        self.within_post = within_post
        self.forum_id = forum_id
        self.raw = raw

class Page:
    def __init__(self, page: BeautifulSoup):
        """
        Initialize
        :param page: Beautiful Soup Object
        """
        self.page = page
        self.error = []

    def get_category(self) -> str:
        return self.get_title().split(']')[0][1:]

    def get_title(self) -> str:
        """
        This function finds the title
        :return: title
        """
        title = self.page.find("h1", class_="ts").text.replace('\n', '').replace(']', '] ')
        return title

    def get_imgs(self, forum_title: str, within_post: str, forum_id: int) -> [Image]:
        img = self.page.find_all("div", class_="mbn savephotop")
        print()
        imgs = []
        for i in img:
            i = i.find('img')
            title = i['title']
            id = i['id']
            src = 'https://FORUM_URL/' + i['file']

            raw = requests.get(src).content

            imgs.append(Image(forum_title, title, id, src, within_post, forum_id, raw))
        return imgs

    def get_pan_link_and_pwd(self):
        """
        This function finds the pan link
        :return: {"panlink", "pwd"}
        :return: None if not found
        """
        pan_link = None
        password = None

        # Find pan link
        for a in self.page.find_all('a', href=True):
            if 'pan.baidu' in a['href']:
                pan_link = a['href']
                break
        if pan_link is None:
            self.error.append("Error when parsing pan link")
            return None

        # Try to find password
        try:
            showhide = self.page.find("div", class_="showhide")
            password = showhide.text[-4:]
        except:
            self.error.append("Password not found!")
            if not self.replied():
                self.error.append("Not replied!")
                # print(Fore.RED + "Not replied!" + Fore.RESET)

        if password is None:
            return pan_link
        else:
            return {'panlink': pan_link, 'pwd': password}

    def replied(self):
        if "查看本帖隐藏内容请" in str(self.page):
            return False
        return True


class Post:
    def __init__(self, url: str):

        url = url.split('&')
        for x in url:
            if 'tid' in x:
                self.tid = int(x.split('=')[1])
        self.url = 'https://FORUM_URL/forum.php?mod=viewthread&tid=' + str(self.tid)
        self.url = urllib.parse.quote(self.url, safe='/:?=&')

        print("Requesting page")
        response = FORUM.get_page(self.url)
        print("Parsing page")
        self.page = Page(response)
        self.replied = self.page.replied()
        self.title = self.page.get_title()
        self.category = self.title.split(']')[0][1:]
        self.images = self.page.get_imgs(self.title, self.url, self.tid)

        # Current NULL Data
        self.replied_time = None
        self.just_replied = False
        self.panlink = None
        self.pwd = None
        self.filename = None
        self.file_size = None
        self.file_md5 = None
        self.file_fetch_time = None

        self.update()

    def reply(self):
        if not self.replied:
            FORUM.reply(tid=self.tid)
            self.just_replied = True
            self.replied_time = time.time()
            self.replied = True
            self.update()
            print(Fore.YELLOW + "Reply cool down..." + Fore.RESET)

            time.sleep(1.7)

    def update(self):
        # Update attributes
        if self.replied:

            print("Requesting page")
            response = FORUM.get_page(self.url)
            print("Parsing page")

            self.page = Page(response)
            self.panlink = self.page.get_pan_link_and_pwd()['panlink']
            self.pwd = self.page.get_pan_link_and_pwd()['pwd']

            pan = PanKit.get_list(shorten_url=PanKit.to_surl(self.panlink), password=self.pwd)
            self.filename = pan['filename']
            self.file_size = pan['size']
            self.file_md5 = pan['md5']
            self.file_fetch_time = time.time()

            print(Fore.CYAN + self.title + Fore.RESET)
            print(self.panlink + "?pwd=" + self.pwd)
            print(self.filename)

    def copy(self):
        pyperclip.copy(self.panlink + "?pwd=" + self.pwd)



header = '''accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding: gzip, deflate, br
accept-language: en
cache-control: max-age=0
referer: https://FORUM_URL/
sec-ch-ua: "Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'''
FORUM = Forum(cookie_file='cookie.txt', headers=header)

