"""
The very first version to fetch hidden data in Discuz! Forum and insert into a database
Archived and discontinued!
First wrote it with minimum comment :(
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import Data as d
import time
import datetime
from file_class import *


def find_title():
    return browser.find_elements(by=By.ID, value="thread_subject")[0].text


def Category():
    return browser.find_element(by=By.CLASS_NAME, value="ts").text


def thread_locked():
    # return true for locked, false for unlocked
    return len(browser.find_elements(by=By.CLASS_NAME, value="locked")) >= 2


def Error_Cat1(error, errInRoll, err):
    if len(error) >= 1:
        errInRoll += 1
        err += 1
        print("Error id:", i)
        print()
        f = d.File('ERROR_UPON_PROVING', i, address, 'NULL', 'NULL')
        d.insert_file(f)
        time.sleep(0.1)
        return True
    else:
        return False


def Check_Publisher(Publish, Name, Fid, Link, author="绳瘾者"):
    if Publish[1].text != author:
        print(Publish[1].text)
        print("Id:", i)
        print("Not a valid thread")
        dl = "Not a valid thread"
        dp = "N/A"
        f = d.File(Name, Fid, Link, dl, dp)
        d.insert_file(f)
        return False
    else:
        return True


def r2(n):
    return "{0:.2f}".format(n)


showTitle = True
if int(input("Show title (0/1): ")) == 0:
    showTitle = False

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

BASE_URL = "https://FORUMURL.com"
PATH = "brower_driver_path"
browser = webdriver.Chrome(chrome_options=options, executable_path=PATH)

browser.get(BASE_URL)

elem = browser.find_elements(by=By.CLASS_NAME, value="fastlg_l")

print(elem[1].text)
elem[1].click()

input("\nEnter after complete login..")

# minimum is 13
# Save links

#Seems like cannot use coin to buy so lock logic gate is wrong
current_id = 36770
end_id = 36822
miss = False
# Set miss to True if want to proceed the missing list
missing = []
# for i in missing:
Descend = False
proving = []
prove = False

'''
for i in missing:
    d.remove_file_by_id(i)
'''

while True:
    browser.minimize_window()
    print(datetime.datetime.now())
    start = time.time()
    itemCount = 1
    reply, replied, add, err, errInRoll = 0, 0, 0, 0, 0

    if miss:
        Que = missing
    else:
        if prove:
            Que = proving
        elif Descend:
            Que = []
            for i in range(current_id, end_id, -1):
                Que.append(i)
        else:
            Que = []
            for i in range(current_id - 1, end_id + 1):
                Que.append(i)

    for i in Que:
        """        
        if errInRoll >= 5:
            print()
            print(f"{bcolors.WARNING}Warning: Error in roll exceed limits{bcolors.ENDC}")
            print()
            break
        """
        address = BASE_URL + "/forum.php?mod=viewthread&tid=" + str(i)
        browser.get(address)
        waited = 0
        view = False
        try:
            error = browser.find_elements(by=By.CLASS_NAME, value="alert_error")
            if not Error_Cat1(error, errInRoll, err):

                publish = browser.find_elements(by=By.CLASS_NAME, value="xw1")
                if Check_Publisher(publish, Category(), i, address):

                    category = Category()
                    title = find_title()
                    if showTitle:
                        print(title)
                    print("Id:", i)

                    Add = False
                    Reply = False

                    l = browser.page_source
                    # print("本帖隐藏的内容" in l)

                    if "以下内容需要积分高于 1000 才可浏览" in l:
                        view = True
                        print("Don't need to reply")
                        Reply = False
                        if not len(d.get_file_by_id(i)) > 0:  # if not contained in sql
                            Add = True
                    elif "本帖隐藏的内容" in l:
                        print("Don't need to reply")
                        Reply = False
                        if not len(d.get_file_by_id(i)) > 0:  # if not contained in sql
                            Add = True
                    else:
                        Reply = True
                        Add = True
                        print("Need reply")


                    if Reply:
                        reply += 1
                        textBox = browser.find_elements(by=By.ID, value="fastpostmessage")
                        textBox[0].send_keys("1111111111111111111111")
                        replyButton = browser.find_element(by=By.ID, value="fastpostsubmit")
                        replyButton.click()
                        print("Replied")
                        time.sleep(0.2)
                        browser.get(address)
                    waited = -1
                    time.sleep(0.1)
                    name = category
                    fid = i
                    link = address
                    if view:
                        index = l.find("链接：")
                        container = l[index:index+1000]
                        container = container.split("：")
                        print(container)
                        dLink = container[1].split('"')[1]
                        dPass = container[2].split("<")[0]
                        print()
                        print(dLink)
                        print(dPass)
                        print()
                    else:
                        container = browser.find_elements(by=By.CLASS_NAME, value="t_f")[0].text
                        if len(browser.find_elements(by=By.CLASS_NAME, value="pstatus")) >= 1:
                            dLink = container[container.find("接") + 1:container.find(" ")]
                        else:
                            dLink = container.split("：")[1]
                        # print("---")
                        # print(container)
                        # print("---")
                        # print(dLink)
                        dPass = browser.find_elements(by=By.CLASS_NAME, value="showhide")[0]
                        print(dPass.text)
                        dPass = dPass.text[dPass.text.find("码") + 2:]

                    if Add:
                        print("Added")
                        File = d.File(name, fid, link, dLink, dPass)
                        d.insert_file(File)
                        add += 1

                    if Reply:
                        print("Wait for cool down")
                        time.sleep(15.1)
                        waited = 1
                        print("CD done", flush=True)
                    print("Done")
                    itemCount += 1

                errInRoll = 0
                end = time.time()
                print("Current on", itemCount, "out of", len(Que))
                print("Avg time (sec):", r2((end - start) / itemCount))
                print("Time elapsed (min):", r2((end - start) / 60))
                print()

        except Exception:
            if waited == -1:
                time.sleep(15)
            err += 1
            errInRoll += 1
            print(f"{bcolors.WARNING}Error id2:{bcolors.ENDC}", i)
            File = d.File('ERROR_UPON_PROVING_ID2', i, address, 'NULL', 'NULL')
            d.insert_file(File)
            print()

    end = time.time()
    print("\nDone!\n" + str(datetime.datetime.now()) + "\n\n")
    print("==============STATICS==============")
    print("Finished:", itemCount)
    print("Time elapsed (min):", r2(end - start))
    print("Replied:", reply)
    print("Has replied already:", replied)
    print("Added:", add)
    print("Error:", err)
    print("===================================\n\n\n")
    # break
    if not missing:
        if input("Continue (0/1): ") == "1":
            In = input("Start id: ")
            if input("Descend (0/1): ") == "1":
                Descend = True
            else:
                Descend = False
            if int(In) < 0:
                current_id = end_id
                end_id = current_id + int(In)
            else:
                current_id = int(In)
                end_id = int(input("End id: "))
                print("\n\n")
