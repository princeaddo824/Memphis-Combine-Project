# The goal of this class is to provide functions that will scrape, clean, and organize a workable dataset for the final website

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd


class WebScraper:

    def __init__(self):
        self.service = service = Service("/Users/princeaddo/Desktop/Development/chromedriver")

    def scrape_anthrometric_data(self):
        # This function scrapes the anthrometric data on the NBA's anthrometric draft page route when called
        # After the data is scraped, it is cleaned, organized and converted into a csv file

        driver = webdriver.Chrome(service=self.service)
        driver.get(r"https://www.nba.com/stats/draft/combine-anthro?dir=A&sort=PLAYER_NAME")
        src = driver.page_source
        parser = BeautifulSoup(src, 'lxml')
        table = parser.find("div", attrs={"class": "Crom_container__C45Ti"})
        headers = table.findAll('th')
        headerList = [h.text.strip() for h in headers]
        rows = table.findAll('tr')[1:]
        player_data = [[td.getText().strip() for td in rows[i].findAll('td')] for i in range(len(rows))]
        stats = pd.DataFrame(player_data, columns=headerList)
        pd.DataFrame.to_csv(stats, f"data/anthrometric.csv")
        driver.quit
        return stats

    def scrape_strength_agility_data(self):
        # This function scrapes the strength and agility data on the NBA's strength and agility draft page route when called
        # After the data is scraped, it is cleaned, organized and converted into a csv file

        driver = webdriver.Chrome(service=self.service)
        driver.get(r"https://www.nba.com/stats/draft/combine-strength-agility?dir=D&sort=PLAYER_NAME")
        src = driver.page_source
        parser = BeautifulSoup(src, 'lxml')
        table = parser.find("div", attrs={"class": "Crom_container__C45Ti"})
        headers = table.findAll('th')[2:]
        headerList = [h.text.strip() for h in headers]
        rows = table.findAll('tr')[1:]
        player_data = [[td.getText().strip() for td in rows[i].findAll('td')[2:]] for i in range(len(rows))]
        stats = pd.DataFrame(player_data, columns=headerList)
        pd.DataFrame.to_csv(stats, f"data/strength_agility.csv")
        driver.quit()
        return stats

    def merge_combine_data(self):
        # This function combines the two different data sets into one big dataset

        anthro = pd.read_csv("anthrometric.csv", index_col=0)
        agility = pd.read_csv("strength_agility.csv", index_col=0)
        combine_data = pd.merge(anthro, agility, how='outer', left_index=True, right_index=True)
        pd.DataFrame.to_csv(combine_data, 'data/combine_data.csv')

    def test(self):
        # A test to confirm that this class is functional
        print("testing")
