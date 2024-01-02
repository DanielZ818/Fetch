import time
from colorama import Fore
import Webkit



def get_url_from_file(url_file: str) -> [str]:
    """
    This function get url from file
    :param url_file:
    :return: list of url
    """
    file = open(url_file, 'r')
    url_list = file.read().split('\n')
    while "" in url_list:
        url_list.remove("")
    return url_list



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

FORUM = Webkit.Forum(cookie_file='cookie.txt', headers=header)

url_list = get_url_from_file('url.txt')

# Tracking variables
cur_on = 0
total_url = len(url_list)
start_time = time.perf_counter()
error = []

for url in url_list:

    if ' ' in url:
        url = url.split(' ')[0]

    if 'forum.php' not in url:
        url = 'https://FORUM_URL/forum.php?mod=viewthread&tid=' + url.split('-')[1]


    cur_on += 1

    # try:
    print(Fore.GREEN + "Current on:", cur_on, "/", total_url, Fore.RESET)


    post = Webkit.Post(url)
    print("Reply...")
    post.reply()


    # Got data
    # For my use case there are these datas
    # Modify to fit your needs!
    fetched_data = {
        'category': post.category,
        'title': post.title,
        'forumID': post.tid,
        'forumLINK': post.url,
        'forumREPLIED': post.replied,
        'forumREPLIEDTIME': post.replied_time,
        'panLINK': post.panlink,
        'panPWD': post.pwd,
        'panFILENAME': post.filename,
        'panFILESIZE': post.file_size,
        'panFILEMD5': post.file_md5,
        'panFETCHTIME': post.file_fetch_time
    }
    print(fetched_data)
    print('=====================================================================')
    