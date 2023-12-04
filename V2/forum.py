"""
Second version of getting hidden content of a thread on Discuz! Forum
Simulate view thread and reply response
Did not use a sqlite3 to store but a json (meant for short term storage)
The hidden content was a baidupan link for the specific forum I was fetching
Summary of V2 Flow:
Get thread html -> Get hidden content (a shared link) -> add to queue
read from queue -> process each shared link (download and rename to the name on thread)
Discontinued!
"""
import time
import requests
from bs4 import BeautifulSoup


def set_cookie(cookie_list):
    """
    This function return a json formatted cookie
    :param cookie_list  ->  formatted like cookie_name=value
    Example: P6Pf_2132_saltkey=b3AsDyf07; P6Pf_2132_lastvisit=1689129528
    """
    cookies = {}
    cookie_list = cookie_list.split("; ")
    for i in cookie_list:
        i.split("=")
        cookies[i.split('=')[0]] = i.split('=')[1]
    return cookies


def set_header(header_list):
    """
    This function return a json formatted header
    :param header_list  ->  formatted like cookie_name=value, seperate by new line (\n)
    Example: P6Pf_2132_saltkey=b4AzDy07; P6Pf_2132_lastvisit=1683129528
    """
    header_list = header_list.split("\n")
    headers = {}
    for i in header_list:
        headers[i.split(": ")[0]] = i.split(": ")[1]
    return headers


def get_response_cookie(response_header):
    """
    This function fetch the cookies in the response header
    :param response_header: dict/json
    :return: a list of tuple [(cookie, val)]
    """
    response_cookie_unformat = response_header['Set-Cookie'].split('; ')
    response_cookie = []
    for i in response_cookie_unformat:
        i = i.replace("secure, ", '')
        if 'P6Pf' in i:
            response_cookie.append((i.split('=')[0], i.split('=')[1]))
    return response_cookie


def get_response_cookie_expiration(response_header):
    """
    This function fetch the expiration time of response cookie
    :param response_header: dict/json
    :return: a list of expiration time in string
    """
    cookie_expire_unformat = response_header['Set-Cookie'].split('; ')
    cookie_expire = []
    for i in cookie_expire_unformat:
        if "expire" in i:
            cookie_expire.append(i.replace('expires=', ''))
    return cookie_expire


def update_cookie(response_cookie, cookies):
    """
    This function update cookies dict
    :param response_cookie: list of tuple [(cookie name, val)]
    :param cookies: cookie dict wants update
    :return: none
    """
    for i in response_cookie:
        cookie_name = i[0]
        cookie_val = i[1]
        cookies[cookie_name] = cookie_val


def get_page(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    response_header = response.headers
    response_cookie = get_response_cookie(response_header)
    response_cookie_expiration = get_response_cookie_expiration(response_header)
    expiration = response_cookie_expiration
    print(expiration)
    update_cookie(response_cookie, cookies)
    html = response.text
    return BeautifulSoup(html, features='html.parser')


def parse_pan_link(page):
    pan_link = None
    try:
        for a in page.find_all('a', href=True):
            if 'pan.baidu' in a['href']:
                pan_link = a['href']
                break
    except:
        print("Error when parsing pan link")
    return pan_link


def parse_pan_password(page):
    password = None
    try:
        showhide = page.find("div", class_="showhide")
        password = showhide.text[-4:]
    except:
        print("Error when parsing password")
    return password


def reply(tid):
    fid = '37'
    url = "FORUM_URL" + fid + "&extra=&tid=" + str(
        tid) + "&replysubmit=yes&inajax=1"
    data = {'formhash': '9393ced2',
            'handlekey': 'reply',
            'noticeauthor': '',
            'noticetrimstr': '',
            'noticeauthormsg': '',
            'usesig': '0',
            'subject': '',
            'message': '123456789123456789'
            }
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    response_header = response.headers
    response_cookie = get_response_cookie(response_header)
    response_cookie_expiration = get_response_cookie(response_header)
    update_cookie(response_cookie, cookies)


def parse_title(page):
    title = page.find("h1", class_="ts").text.replace('\n', '').replace(']', '] ')
    return title


def get_saved_cookie():
    saved_cookie = open("Saved_data/cookie.txt", "r")
    cookie = saved_cookie.read().replace('\n', '')
    saved_cookie.close()
    cookies = set_cookie(cookie)
    return cookies


def save_cookie(cookies):
    line = ''
    for key in cookies:
        line += key + "=" + cookies[key] + "; "
    line = line[:-2]
    saved_cookie = open("Saved_data/cookie.txt", "w")
    saved_cookie.write(line)
    saved_cookie.close()


def reply_and_get(tid, REPLY=False):
    page = get_page(url)
    title = parse_title(page)
    did_reply = False
    if REPLY and not viewable(page):
        reply(tid)
        did_reply = True
        page = get_page(url)
    if not viewable(page):
        return (title, "Pan Link Error", did_reply)
    else:
        pan_link = parse_pan_link(page)
        password = parse_pan_password(page)
        pan_link += '?pwd=' + password
        save_cookie(cookies)
        return title, pan_link, did_reply


def parse_url_into_tid():
    file = open('url.txt', 'r')
    url = file.read().split('\n')
    while "" in url:
        url.remove("")
    tid = []
    for i in url:
        for x in i.split("&"):
            if 'tid' in x:
                cur_tid = x[4::]
                tid.append(cur_tid)
    return tid


def viewable(page):
    if "查看本帖隐藏内容请" in str(page):
        return False
    return True


global url, cookies

header = '''accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding: gzip, deflate, br
accept-language: en
cache-control: max-age=0
sec-ch-ua: "Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'''
headers = set_header(header)

tid = parse_url_into_tid()
for i in tid:
    cookies = get_saved_cookie()
    url = "https://url/thread-" + str(i) + "-1-1.html"

    title, pan_link, did_reply = reply_and_get(i, REPLY=True)
    print(title)
    if pan_link == 'Pan Link Error':
        print("Pan Link Error")
        continue
    print(pan_link)
    print()
    if did_reply:
        time.sleep(15)
