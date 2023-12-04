"""
Match each baidupan shared link to the actual filename
This contains the first version of pankit (convert url -> file properties)
Problem: Simulate human requests using selenium and is slow because of the js which leads to timeout
Discontinued!
"""
import datetime
import time
import json
from colorama import Fore
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service


class stored_data:
    def __init__(self, json_file):
        self.json_file = json_file

    def write(self, data):
        """
        This function write data into json file
        :param data: dictionary or list of dictionary
        :return: None
        """
        with open(self.json_file, 'w') as f:
            json.dump(data, f)

    def read(self):
        """
        This function get the data from JSON file
        :return: dictionary or list of dictionary
        """
        with open(self.json_file, 'r') as f:
            data = json.load(f)
        return data


copied_links = []
while True:
    # Get existing file names
    saved_pan = stored_data('Saved_data/pan_url.json')
    saved_pan_url = saved_pan.read()

    # Open queue
    file = open('Saved_data/pan_url.txt', 'r')
    data = file.read()
    file.close()
    file = open('Saved_data/pan_url.txt', 'w')  # Clear queue after getting them
    file.close()
    data = data.split('\n')
    data = data[0:-1]
    queue = data

    # Tracking Variables
    total_file = len(queue)
    cur_file = 0

    # Browser Setup
    ser = Service(r"browser_driver_path")
    op = webdriver.ChromeOptions()
    #op.add_argument('headless')  # Hide browser window
    prefs = {"profile.managed_default_content_settings.images": 2}  # Disable media
    op.add_experimental_option("prefs", prefs)
    caps = DesiredCapabilities().CHROME
    # caps["pageLoadStrategy"] = "normal"  # complete
    # Below option didn't work -> Cannot login
    # caps["pageLoadStrategy"] = "eager"  #  interactive
    # caps["pageLoadStrategy"] = "none"
    if len(queue) != 0:
        browser = webdriver.Chrome(service=ser, options=op, desired_capabilities=caps)
        browser.set_page_load_timeout(35)

    for i in queue:
        # MOVED TO FLOW
        # Copy URL to 解析
        # if i not in copied_links:
        #     copied_links.append(i)
        #     pyperclip.copy(i)

        # Tracking
        start = time.time()
        cur_file += 1
        print(Fore.GREEN + 'Current on:', cur_file)
        print(Fore.RESET + "Total File:", total_file)

        # Get title (file name)
        try:
            url = i
            browser.get(url)
            file_name = browser.title.split('_')[0]
            print(file_name)
        except:
            file_name = None
            print(Fore.RED + "Time Out!" + Fore.RESET)
            file = open('Saved_data/pan_url.txt', 'a')
            file.write(url + "\n")
            file.close()

        if file_name is not None and '提取' in file_name:
            print(Fore.RED + "Page didn't finish loading!" + Fore.RESET)
            file_name = None
            file = open('Saved_data/pan_url.txt', 'a')
            file.write(url + "\n")
            file.close()

        # Update dictionary to bind
        if url not in saved_pan_url.keys():
            saved_pan_url[url] = file_name
        elif saved_pan_url[url] is None:
            saved_pan_url[url] = file_name

        print("Finish!")
        print(Fore.BLUE + "Time took:", str(round(time.time() - start, 2)) + 's')

        # Save
        saved_pan.write(saved_pan_url)
        print(Fore.GREEN + "Saved")
        print(Fore.RESET + "====================================")

    if len(queue) == 0:
        print(datetime.datetime.now(), "No new file found! Awaiting for new link!")

    time.sleep(2)
