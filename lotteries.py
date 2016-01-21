import requests
import os
import re
import sqlite3
import calendar
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
from hashlib import md5
from .lottery import Lottery, LotteryDrawing

class LuckyForLife(Lottery):
    
    def __init__(self):
        super(LuckyForLife, self).__init__()
        self.name = "Lucky For Life"
        self.states_available = ["CT", "ME", "NH", "VT", "MA", "RI"]
        self.jackpot = "$1,000 A Day for Life"
        self.scrape_url = "http://www.luckyforlife.us/winning-numbers/search-winning-numbers"
    
    def get_drawings(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
        rawData = requests.post(self.scrape_url, data={"startdate": "2013-01-01", "enddate": "2030-12-31"}, headers=headers)
        soup = BeautifulSoup(rawData.text)
        
        winning_numbers_table = soup.findAll("table")[2]
        for i, row in enumerate(winning_numbers_table.findAll("tr")):
            if i == 0:
                continue
            cells = row.findAll("td")
            date = datetime.strptime(cells[0].text, "%m/%d/%Y")
            numbers = cells[1].text
            drawing = LotteryDrawing()
            drawing.date = date
            drawing.numbers = [int(i) for i in numbers.split('-')]
            drawing.special_numbers = [int(cells[2].text)]
            self._drawings.append(drawing)
        return self._drawings
    
    def get_jackpot(self):
        return '$1,000 A Day for Life'

    def has_drawing_today(self):
        today = datetime.today().weekday()
        if today in [calendar.MONDAY, calendar.THURSDAY]:
            return True
        else:
            return False

class HotLotto(Lottery):
    
    def __init__(self):
        super(HotLotto, self).__init__()
        self.name = "HotLotto"
        self.scrape_url = "http://www.powerball.com/hotlotto/winnums-text.txt"
        self.jackpot = "Unknown"
        self.states_available = ["DE", "DC", "ID", "IA", "KS", "ME", "MN", "MT", "NH", "NM", "ND", "SD", "TN", "WV"]
    
    def get_drawings(self):
        html = requests.get(self.scrape_url).text
        html = html.replace('Draw Date   WB1 WB2 WB3 WB4 WB5 HB  ', '')
        html = os.linesep.join([s for s in html.splitlines() if s])

        for line in html.splitlines():
            splitLine = line.split()
            drawing = LotteryDrawing()
            drawing.date = parse(splitLine[0])
            drawing.numbers = [int(splitLine[1]),
                               int(splitLine[2]),
                               int(splitLine[3]),
                               int(splitLine[4]),
                               int(splitLine[5])]
            drawing.special_numbers = [int(splitLine[6])]
            self._drawings.append(drawing)
        return self._drawings
    
    def get_jackpot(self):
        html = requests.get("http://www.powerball.com/hotlotto/hl_main.asp").text
        self.jackpot = re.search("\$\s?(\d+),?(\d+),?(\d+)", html).group(0).replace(' ', '')
        return self.jackpot

    def has_drawing_today(self):
        today = datetime.today().weekday()
        if today in [calendar.WEDNESDAY, calendar.SATURDAY]:
            return True
        else:
            return False
    
class Megamillions(Lottery):
    
    def __init__(self):
        super().__init__()
        self.name = "Megamillions"
        self.scrape_url = "http://www.ialottery.com/Results/MM.txt"
        self.jackpot = "Unknown"
        self.states_available = ["WA", "OR", "CA", "ID", "MT", "WY", "CO", "AZ", "NM", "ND",
                                 "SD", "NE", "KS", "OK", "TX", "MN", "IA", "MO", "AR", "LA",
                                 "WI", "IL", "IN", "KY", "TN", "MI", "OH", "ME", "VT", "NH",
                                 "MA", "RI", "CT", "PA", "NJ", "WV", "VA", "NC", "SC", "GA",
                                 "FL", "DE", "MD", "DC", "VI"]
        
    def get_drawings(self):
        html = requests.get(self.scrape_url)
        html.encoding = 'utf-16'
        html = html.text
        html = '\n'.join([s for s in html.splitlines() if len(s) > 0]) #remove blank lines
        html = '\n'.join(html.split('\n')[1:]) #remove first line

        drawings = []
        for line in html.splitlines():
                if len(line) > 1:
                        drawing = LotteryDrawing()
                        splitLine = line.split()
                        drawing.date = parse(splitLine[0].replace("-", "/"))
                        drawing.numbers = [int(splitLine[1]),
                                           int(splitLine[2]),
                                           int(splitLine[3]),
                                           int(splitLine[4]),
                                           int(splitLine[5])]
                        drawing.special_numbers = [int(splitLine[6]), int(splitLine[7])]
                        self._drawings.append(drawing)
        return self._drawings
    
    def get_jackpot(self):
        megamillionsHTML = requests.get("http://megamillions.com/").text
        megamillionsJackpotAmount = None
        soup = BeautifulSoup(megamillionsHTML)
        megamillionsJackpotAmount = "$" + soup.find_all('div', class_="home-next-drawing-estimated-jackpot-dollar-amount")[0].get_text() + " Million"
        self.jackpot = megamillionsJackpotAmount.replace(' Million', ',000,000')
        return self.jackpot

    def has_drawing_today(self):
        today = datetime.today().weekday()
        if today in [calendar.TUESDAY, calendar.FRIDAY]:
            return True
        else:
            return False
    
class Powerball(Lottery):
    
    def __init__(self):
        super(Powerball, self).__init__()
        self.name = "Powerball"
        self.scrape_url = "http://www.powerball.com/powerball/winnums-text.txt"
        self.jackpot = "Unknown"
        self.states_available = ["WA", "OR", "CA", "ID", "MT", "WY", "CO", "AZ", "NM", "ND",
                                 "SD", "NE", "KS", "OK", "TX", "MN", "IA", "MO", "AR", "LA",
                                 "WI", "IL", "IN", "KY", "TN", "MI", "OH", "ME", "VT", "NH",
                                 "MA", "RI", "CT", "PA", "NJ", "WV", "VA", "NC", "SC", "GA",
                                 "FL", "DE", "MD", "DC", "VI"]
        
    def get_drawings(self):
        html = requests.get(self.scrape_url).text
        html = html.replace('Draw Date   ', '')
        html = html.replace('WB1 WB2 WB3 WB4 WB5 PB  PP', '')
        html = os.linesep.join([s for s in html.splitlines() if s])

        drawings = []
        for line in html.splitlines():
                splitLine = line.split()
                drawing = LotteryDrawing()
                drawing.date = parse(splitLine[0])
                drawing.numbers = [int(splitLine[1]),
                                   int(splitLine[2]),
                                   int(splitLine[3]),
                                   int(splitLine[4]),
                                   int(splitLine[5])]
                try:
                    drawing.special_numbers = [int(splitLine[6]), int(splitLine[7])]
                except IndexError:
                    drawing.special_numbers = [int(splitLine[6])]
                    
                self._drawings.append(drawing)
        return self._drawings
    
    def get_jackpot(self):
        html = requests.get("http://www.powerball.com/").text
        self.jackpot = re.search("\$\s?(\d+) Million", html).group(0).replace(' Million', ',000,000')
        return self.jackpot

    def has_drawing_today(self):
        today = datetime.today().weekday()
        if today in [calendar.WEDNESDAY, calendar.SATURDAY]:
            return True
        else:
            return False
    
class LotteryManager:
    
    def __init__(self):
        self.lotteries = []
        self.db_conn = sqlite3.connect("lottery_data.sqlite3")
        self.db = self.db_conn.cursor()
        self.__create_structure()
        
    def __create_structure(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS lottery_drawings
                         (
                             date DATETIME,
                             numbers TEXT,
                             hash TEXT UNIQUE,
                             lottery_name TEXT
                         )
                        """)
        
    def add_lottery(self, lottery):
        if not isinstance(lottery, Lottery):
            return
        
        self.lotteries.append(lottery)
    
    def run(self):
        for lottery in self.lotteries:
            drawings = lottery.get_drawings()
            self.store(drawings, lottery.name)
            print("Retrieved {} drawings for {}".format(len(drawings), lottery.name))
            
    def store(self, drawings, lotteryName):
        self.db.execute("BEGIN TRANSACTION")
        for drawing in drawings:
            self.db.execute("INSERT OR IGNORE INTO lottery_drawings VALUES (?, ?, ?, ?)", (drawing.date,
                                                                                 drawing.number_string(),
                                                                                 drawing.hash(),
                                                                                 lotteryName))
        self.db_conn.commit()

LOTTERIES = [LuckyForLife, HotLotto, Megamillions, Powerball]
