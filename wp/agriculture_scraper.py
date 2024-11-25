import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

class AgricultureSpider(scrapy.Spider):
    name = "Agriculture_spider"
    start_urls = [
        "https://search.rakuten.co.jp/search/mall/%E8%9C%82%E5%B1%8B%E6%9F%BF%E8%8B%97/",
    ]

    def parse(self, response):
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 複数のカードを取得 (dui-cards searchresultitemsを含むdivを検索)
        cards = soup.find_all("div", class_="searchresultitem")  # こちらのクラス名に変更する

        for card in cards:
            # 商品名を取得
            product_name_tag = card.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2")
            product_name = product_name_tag.get_text(strip=True) if product_name_tag else "商品名不明"

            # 価格を取得
            product_price_tag = card.find("div", class_="price--OX_YW")
            product_price = product_price_tag.get_text(strip=True) if product_price_tag else "価格不明"

            # 結果を表示
            print(f"商品名: {product_name}")
            print(f"価格: {product_price}")

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(AgricultureSpider)
    process.start()
