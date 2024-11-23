import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup

class AgricultureSpider(scrapy.Spider):
    name = "Agriculture_spider"
    start_urls = [
        "https://www.kobayashi-seed.com/view/item/000000009278", #サンプル
        "https://www.kobayashi-seed.com/view/item/000000009279",
        "https://www.kobayashi-seed.com/view/item/000000009280",
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # 商品名と価格を取得
        product_name = soup.find("h1", class_="p-product-head__title").get_text(strip=True)  #サイトのclassによって変わる
        product_price = soup.find("span", class_="p-product-content__price-number").get_text(strip=True) #同上

        # 結果を表示
        print(f"URL: {response.url}")
        print(f"商品名: {product_name}")
        print(f"価格: {product_price}")

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(AgricultureSpider)
    process.start()