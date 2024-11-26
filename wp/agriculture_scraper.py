import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

class AgricultureSpider(scrapy.Spider):
    name = "Agriculture_spider"
    start_urls = [
        "https://search.rakuten.co.jp/search/mall/%E8%9C%82%E5%B1%8B%E6%9F%BF%E8%8B%97/",  # rakuten
        "https://shopping.yahoo.co.jp/search/%E5%B9%B2%E3%81%97%E6%9F%BF+%E8%9C%82%E5%B1%8B%E6%9F%BF/38289/",#yahoo
    ]
#サイトの判別
    def parse(self, response):
        if "rakuten" in response.url:
            self.parse_rakuten(response)
        elif "yahoo" in response.url:
            self.parse_yahoo(response)
        #elif "サイト名" in response.url:
            #self.parse_サイト名.url:

#サイトにごとの処理の関数
    def parse_rakuten(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="searchresultitem")  # 楽天の検索結果カード

        for card in cards:
            product_name_tag = card.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2")
            product_name = product_name_tag.get_text(strip=True) if product_name_tag else "商品名不明"

            product_price_tag = card.find("div", class_="price--OX_YW")
            product_price = product_price_tag.get_text(strip=True) if product_price_tag else "価格不明"

            print(f"[楽天市場] 商品名: {product_name}")
            print(f"価格: {product_price}")

    def parse_yahoo(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("li", class_="LoopList__item")  # yahooの検索結果カード

        for card in cards:
            product_name_tag = card.find("p", class_="SearchResultItemTitle_SearchResultItemTitle__itemNameRow__zMYfj")
            product_name = product_name_tag.get_text(strip=True) if product_name_tag else "商品名不明"

            product_price_tag = card.find("span", class_="SearchResultItemPrice_SearchResultItemPrice__value__G8pQV")
            product_price = product_price_tag.get_text(strip=True) if product_price_tag else "価格不明"

            print(f"[Yahoo] 商品名: {product_name}")
            print(f"価格: {product_price}")
            
    #def parse_サイト名(self,response):
        #soup = BeautifulSoup(response.text, "html.parser")
        #以降サイトごとに書く

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(AgricultureSpider)
    process.start()
