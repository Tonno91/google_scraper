
__all__ = ()

from bs4 import BeautifulSoup
from tkinter import END
from threading import Thread

from datetime import datetime
import requests
import re
import random
import time

import app_gui, mongo_db, proxies


class c_thread(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        while True:
            if window.start.status_click is True:
                window.start.status_click = False
                web_scraping()


def soup_scraper(url, database, website, key_word, ):
    try:
        response = requests.get(url)
        print(response, " ", end='')

    except:
        print("Skipping. Connnection error")
        return "", database

    soup = BeautifulSoup(response.content, 'html.parser')
    contents = soup.find_all(class_='ZINbbc xpd O9g5cc uUPGi')
    for content in contents:
        try:
            title = content.find_all(class_='BNeawe vvjwJb AP7Wnd')[0].get_text()
            description = content.find_all(class_='BNeawe s3v9rd AP7Wnd')[0].get_text()
            try:
                description = description.find_all(class_='BNeawe s3v9rd AP7Wnd')[0]
            except:
                description = description
            link = content.find_all(href=re.compile("/url\?q="))[0]
            link_text = re.search(r"\/url\?q=(\S+)&amp;sa", link.prettify()).group(1)
            link_base = re.search(r"(https?:\/\/\S+?)\/", link_text).group(1)
        except:
            continue

        db = {
            "website": website,
            "keyword": key_word,
            "timestamp": datetime.utcnow(),
            "position": 0,
            "actual_score": 0,
            "total_score": 0,
            "medium": 0,
            "weight": 0,
            "title": title,
            "description": description,
            "base_link": link_base,
            "full_link": link_text
              }
        database.append(db)

    nexts = soup.find_all(class_='nBDE1b G5eFlf')
    if len(nexts) == 1:
        next = nexts[0].attrs['href']
    else:
        next = nexts[1].attrs['href']

    return next, database


def web_scraping():
    # Getting the value insert in the GUI
    website = window.website.box.get()
    rep_time = window.rep_time.get_value()
    rep_limit = window.rep_limit.get_value()
    result_num = window.result_num.get_value()
    key_word = window.key_words.get_value().replace(" ", "+")

    url_website = web_search_site[website]

    for repeat_index in range(rep_limit):
        database = []
        index = 0
        url = url_website[0] + key_word

        for page_num in range(result_num):
            # Calling for scraping the Web, then print the results
            url, database = soup_scraper(url, database, website, key_word)
            url = url_website[1] + url

            for index, data in enumerate(database):
                if index >= result_num: break
                if data["position"] == 0:
                    print("{}.\tLink: {} # ".format(index+1, data["base_link"]), end='')
                    data["position"] = index+1

            database = database[:result_num]
            # prog_bar = int((len(database)/result_num)*100)
            window.start_bar.bar_step(int((len(database)/result_num)*100))
            if index >= result_num: break
            if window.stop.status_click is True:
                print("STOP SCRAPING2")
                window.stop.status_click = False
                window.start_bar.bar_step(0)
                return database

            delay = (random.randint(300, 800)) / 100
            print("Delay: {}".format(delay))
            time.sleep(delay)

        # Load to DATABASE
        DB_address = "localhost"
        DB_port = "27017"
        mongo_db.load_dict_to_db(address=DB_address, port=DB_port, array=database)
        window.start_bar.bar_step(0)

        # DELAY FOR THE NEXT LOOP
        print("Countdown: ", end='')
        for i in range(int(rep_time/5)):
            print("{} ".format(rep_time-5*i), end='')
            time.sleep(5)
            if window.stop.status_click is True:
                print("STOP SCRAPING3")
                window.stop.status_click = False
                return database

        print("Loop number: {}".format(repeat_index+1))
    return database


def gui_panel():
    """GUI User Panel main window"""
    global window
    window = app_gui.MainApplication()

    # Default value in the Panel
    window.website.box.insert(END, "Google")
    window.rep_time.box.insert(END, 10)
    window.rep_limit.box.insert(END, 3)
    window.key_words.box.insert(END, "NASA")
    window.result_num.box.insert(END, 5)

    # Parallel thread to launch the scraping
    control_thread1 = c_thread()
    control_thread1.start()

    window.mainloop()


def main():
    global web_search_site
    web_search_site = {
        "Google": ["https://www.google.com//search?client=firefox-b-d&q=", "https://www.google.it"],
        "Amazon": ["https://www.bing.com/search?form=MOZLBR&pc=MOZI&q=", "https://www.amazon.com"]
    }

    gui_panel()
