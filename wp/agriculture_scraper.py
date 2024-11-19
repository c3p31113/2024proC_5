import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import sqlite3

class AgricultureSpider(scrapy.Spider):
    name = "agriculture_spider"
    start_urls = [
        'https://www.monotaro.com/s/q-%E3%81%95%E3%82%84%E3%81%88%E3%82%93%E3%81%A9%E3%81%86%20%E7%A8%AE/?cq_plt=bp&cq_net=o&utm_source=bing&utm_medium=cpc&utm_campaign=180698424_424835292&utm_content=1353500415386533&utm_term=b_84594245979131_dat-2336393490013977:loc-96&msclkid=9c1777a78762155f0ff2109b82074057',  # 農業情報サイト1
        'http://example2.com/crops',  # 農業情報サイト2
        # 他のサイトを追加
    ]

    def __init__(self, crop, area, workers, *args, **kwargs):
        super(AgricultureSpider, self).__init__(*args, **kwargs)
        self.crop = crop
        self.area = area
        self.workers = workers

    def parse(self, response):
        # Beautiful Soupを使用してHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        crops = []
        for crop_div in soup.find_all('div', class_='crop'):
            name = crop_div.find('h2').text
            fertilizer = crop_div.find('span', class_='fertilizer').text
            pesticide = crop_div.find('span', class_='pesticide').text
            growing_season = crop_div.find('span', class_='season').text
            crops.append({
                'name': name,
                'fertilizer': fertilizer,
                'pesticide': pesticide,
                'growing_season': growing_season,
            })
        self.save_to_db(crops)

    def save_to_db(self, crops):
        conn = sqlite3.connect('probc_sd5.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS crops
                     (name text, fertilizer text, pesticide text, growing_season text)''')
        for crop in crops:
            c.execute("INSERT INTO crops VALUES (?, ?, ?, ?)",
                      (crop['name'], crop['fertilizer'], crop['pesticide'], crop['growing_season']))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    crop = sys.argv[1]
    area = sys.argv[2]
    workers = sys.argv[3]

    process = CrawlerProcess()
    process.crawl(AgricultureSpider, crop=crop, area=area, workers=workers)
    process.start()