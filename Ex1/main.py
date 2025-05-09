import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from init_player import Player
from init_player import Player_Manager
Player_manager = Player_Manager()

def to_float(n):
    if n == '': return "N/a"
    return float(n)

def CrawlDataFunction(url, XP, Data_Name):
    driver = webdriver.Chrome()
    driver.get(url)

    resultPlayerData = []
    try:
        time.sleep(5)
        table2 = driver.find_element(By.XPATH, XP)
        rows2 = table2.find_elements(By.TAG_NAME, 'tr')

        for row in rows2:
            cols = row.find_elements(By.TAG_NAME, 'td')
            data = []
            for id, play in enumerate(cols[:-1]):
                if id == 1:
                    a = play.text.strip().split()
                    if len(a) == 2:
                        data.append(a[1])
                    else:
                        data.append(play.text.strip())
                else:
                    s = play.text.strip()
                    if id >= 4:
                        s = s.split("-")[0]
                        s = s.replace(",", "")
                        s = to_float(s)
                    data.append(s)
            if len(data) != 0: resultPlayerData.append(data)
    finally:
        driver.quit()
        print("Finish Page " + Data_Name)
    return resultPlayerData


def crawl_data_standard():
    url = "https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats"
    XP = '//*[@id="stats_standard"]'
    DataName = "Standard"
    list_player = CrawlDataFunction(url, XP, DataName)

    print("list_player", list_player)
    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p is None:
            new_player = Player(i[0], i[1], i[2], i[3], i[4])
            new_player.setPlaying_time(i[6:9])
            new_player.setPerformance([i[13], i[14], i[11], i[16], i[17]])
            new_player.setExpected(i[18:21])
            new_player.setProgression(i[22:25])
            new_player.setPer90(i[25:])
            Player_manager.add(new_player)

    Player_manager.filtering()

def crawl_data_goalkeeping():
    url = 'https://fbref.com/en/comps/9/2024-2025/keepers/2024-2025-Premier-League-Stats'
    XP = '//*[@id="stats_keeper"]'
    DataName = "Goalkeeping"
    list_player = CrawlDataFunction(url, XP, DataName)

    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p:
            p.setGoalkeeping(i[10:20], i[20:])

def crawl_data_shooting():
    url = 'https://fbref.com/en/comps/9/2024-2025/shooting/2024-2025-Premier-League-Stats'
    XP = '//*[@id="stats_shooting"]'
    DataName = "Shooting"
    list_player = CrawlDataFunction(url, XP, DataName)

    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p:
            p.setShooting(i[7:19])

def crawl_data_passing():
    url = 'https://fbref.com/en/comps/9/2024-2025/passing/2024-2025-Premier-League-Stats'
    XP = '//*[@id="stats_passing"]'
    DataName = "Passing"
    list_player = CrawlDataFunction(url, XP, DataName)

    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p:
            p.setPassing(i[7:12], i[12:15], i[15:18], i[18:21], i[21:])


def crawl_data_gca():
    url = 'https://fbref.com/en/comps/9/2024-2025/gca/2024-2025-Premier-League-Stats'
    XP = '//*[@id="stats_gca"]'
    DataName = "Goal and Shot Creation"
    list_player = CrawlDataFunction(url, XP, DataName)

    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p:
            p.setGoalShotCreation(i[7:9], i[15:17])

def crawl_data_defense():
    url = 'https://fbref.com/en/comps/9/2024-2025/defense/2024-2025-Premier-League-Stats'
    XP = '//*[@id="stats_defense"]'
    DataName = "Defensive Actions"
    list_player = CrawlDataFunction(url, XP, DataName)

    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p:
            p.setDefensiveActions(i[7:12], i[12:16], i[16:23])

def crawl_data_possession():
    url = 'https://fbref.com/en/comps/9/2024-2025/possession/2024-2025-Premier-League-Stats'
    XP = '//*[@id="stats_possession"]'
    DataName = "Possession"
    list_player = CrawlDataFunction(url, XP, DataName)

    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p:
            p.setPossession(i[7:14], i[14:19], i[19:27], i[27:29])


def crawl_data_misc():
    url = 'https://fbref.com/en/comps/9/2024-2025/misc/2024-2025-Premier-League-Stats'
    XP = '//*[@id="stats_misc"]'
    DataName = "Miscellaneous"
    list_player = CrawlDataFunction(url, XP, DataName)

    for i in list_player:
        p = Player_manager.find(i[0], i[3])
        if p:
            p.setMiscStats(i[10:14] + i[18:20], i[20:23])

def run_all_crawlers():
    crawl_data_standard()
    crawl_data_goalkeeping()
    crawl_data_shooting()
    crawl_data_passing()
    crawl_data_gca()
    crawl_data_defense()
    crawl_data_possession()
    crawl_data_misc()
    Player_manager.sort()


run_all_crawlers()


import csv
from init_player import header_player, row_player
with open('../results/result.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header_player)
    for player in Player_manager.list_player:
        r = row_player(player)
        writer.writerow(r)