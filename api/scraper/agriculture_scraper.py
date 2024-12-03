import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import re
from collections import defaultdict


class AgricultureSpider(scrapy.Spider):
    name = "Agriculture_spider"

    urls_with_metadata = [  # {"id":"","url":"","category":""},コピー元
        # かき
        {
            "id": "persimmon",
            "url": "https://search.rakuten.co.jp/search/mall/%E8%9C%82%E5%B1%8B%E6%9F%BF%E8%8B%97/",
            "category": "蜂屋柿苗",
        },
        {
            "id": "persimmon",
            "url": "https://shopping.yahoo.co.jp/search/%E5%B9%B2%E3%81%97%E6%9F%BF+%E8%9C%82%E5%B1%8B%E6%9F%BF/38289/",
            "category": "蜂屋柿苗",
        },
        {
            "id": "persimmon_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E6%9F%BF+%E3%81%AE+%E8%82%A5%E6%96%99/",
            "category": "蜂屋柿苗-肥料",
        },
        # いちご
        {
            "id": "strawberry",
            "url": "https://www.kokkaen-ec.jp/products/list?category_id=162",
            "category": "いちご",
        },
        {
            "id": "strawberry",
            "url": "https://shop.takii.co.jp/category/00006212",
            "category": "いちご"
        },
        {
            "id": "fertilizer_1",
            "url": "https://shop.takii.co.jp/category/00010115",
            "category": "いちご-肥料"
        },
        # インゲン
        {
            "id": "greenbeans",
            "url": "https://shop.takii.co.jp/category/00007799",
            "category": "インゲン",
        },
        {
            "id": "greenbeans",
            "url": "https://search.kakaku.com/%E7%A8%AE%20%E3%82%A4%E3%83%B3%E3%82%B2%E3%83%B3/",
            "category": "インゲン",
        },
        {
            "id": "greenbeans_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E8%B1%86%E8%82%A5%E6%96%99/",
            "category": "インゲン-肥料",
        },
        # きゅうり
        {
            "id": "cucumber",
            "url": "https://shop.takii.co.jp/category/00003415",
            "category": "きゅうり",
        },
        {
            "id": "cucumber",
            "url": "https://www.matsuonouen.net/?mode=cate&cbid=2262850&csid=0",
            "category": "きゅうり",
        },
        {
            "id":"cucumber_f",
            "url":"https://shop.takii.co.jp/product/catalog/kw/%E3%81%8D%E3%82%85%E3%81%86%E3%82%8A%E3%81%AE%E8%82%A5%E6%96%99",
            "category":"きゅうり-肥料"
        },
        {
            "id": "cucumber_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%81%8D%E3%82%85%E3%81%86%E3%82%8A+%E8%82%A5%E6%96%99/",
            "category": "きゅうり",
        },
        # さやえんどう
        {
            "id": "Snowpeas",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%81%95%E3%82%84%E3%81%88%E3%82%93%E3%81%A9%E3%81%86+%E7%A8%AE/",
            "category": "さやえんどう",
        },
        {
            "id":"Snowpeas",
            "url":"https://shop.takii.co.jp/product/catalog/s/default/n/25/t/category/ca/00003435/es/1#a1",
            "category":"さやえんどう"
        },
        {
            "id": "Snowpeas_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%81%88%E3%82%93%E3%81%A9%E3%81%86+%E8%82%A5%E6%96%99/",
            "category": "さやえんどう-肥料",
        },
        # しいたけ
        {
            "id": "Shiitake",
            "url": "https://search.kakaku.com/%E7%A8%AE%20%E3%81%97%E3%81%84%E3%81%9F%E3%81%91%20%E8%8F%8C/",
            "category": "しいたけ",
        },
        # 春菊
        {
            "id": "Shungiku",
            "url": "https://www.kobayashi-seed.com/view/category/ct32",
            "category": "春菊",
        },
        {
            "id": "Shungiku",
            "url": "https://shop.takii.co.jp/category/00003461",
            "category": "春菊",
        },
        {
            "id": "Shungiku_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E5%8C%96%E6%88%90%E8%82%A5%E6%96%99+%E5%9C%92%E8%8A%B8+%E3%81%8A%E3%81%99%E3%81%99%E3%82%81/",
            "category": "春菊-肥料",
        },
        # 西洋なし
        {
            "id": "westernpear",
            "url": "https://search.kakaku.com/%E8%8B%97%20%E8%A5%BF%E6%B4%8B%E6%A2%A8/",
            "category": "西洋なし",
        },
        {
            "id":"westernpear_f",
            "url":"https://shop.takii.co.jp/product/catalog/kw/%E6%9E%9C%E6%A8%B9%E5%AE%9F%E7%89%A9%E5%B0%82%E7%94%A8%E8%82%A5%E6%96%99",
            "category":"西洋なし-肥料"
        },
        # にら
        {
            "id": "Chinesechive",
            "url": "https://www.tanehyo.jp/view/category/ct27",
            "category": "にら",
        },
        {
            "id": "Chinesechive",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%83%8B%E3%83%A9+%E7%A8%AE/",
            "category": "にら",
        },
        {
            "id": "Chinesechive_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%83%8B%E3%83%A9+%E6%A0%BD%E5%9F%B9+%E8%82%A5%E6%96%99/",
            "category": "にら-肥料",
        },
        # 花わさび
        {
            "id": "flowerwasabi",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%82%8F%E3%81%95%E3%81%B3+%E7%A8%AE/100012/",
            "category": "花わさび",
        },
        # ピーマン
        {
            "id": "greenpepper",
            "url": "https://shop.takii.co.jp/category/00008407",
            "category": "ピーマン",
        },
        {
            "id": "greenpepper",
            "url": "https://search.rakuten.co.jp/search/mall/%E7%A8%AE+%E3%83%94%E3%83%BC%E3%83%9E%E3%83%B3/",
            "category": "ピーマン",
        },
        {
            "id": "greenpepper_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%83%94%E3%83%BC%E3%83%9E%E3%83%B3+%E8%82%A5%E6%96%99/",
            "category": "ピーマン-肥料",
        },
        # ぶどう
        {
            "id": "grapes",
            "url": "https://shop.takii.co.jp/category/00004057",
            "category": "ぶどう",
        },
        {
            "id": "grapes",
            "url": "https://search.kakaku.com/%E3%83%96%E3%83%89%E3%82%A6%20%E8%8B%97/",
            "category": "ぶどう",
        },
        {
            "id": "grapes_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%81%B6%E3%81%A9%E3%81%86+%E8%82%A5%E6%96%99/",
            "category": "ぶどう-肥料",
        },
        # もも
        {
            "id": "peach",
            "url": "https://shop.takii.co.jp/category/00004064",
            "category": "もも",
        },
        {
            "id": "peach",
            "url": "https://www.hanahiroba.com/c/0000000100/0000000101/0000000128?srsltid=AfmBOopfZ-Nwg6CuLyy_Llcwf3L2lKbFNdXlspLt5iWYNxMAx4KVLzls",
            "category": "もも",
        },
        {
            "id": "peach_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E6%A1%83+%E8%82%A5%E6%96%99/",
            "category": "もも-肥料",
        },
        # りんご
        {
            "id": "apple",
            "url": "https://shop.takii.co.jp/category/00004069",
            "category": "りんご",
        },
        {
            "id": "apple",
            "url": "https://www.hanahiroba.com/c/0000000100/0000000135/0000000146?srsltid=AfmBOoow1SiZxqgbJ-SLjuxgAeUdBu1WDq8YUTqy5tF_NM70NDKGTfMa",
            "category": "りんご",
        },
        {
            "id": "apple_f",
            "url": "https://search.rakuten.co.jp/search/mall/%E3%82%8A%E3%82%93%E3%81%94%E8%82%A5%E6%96%99/",
            "category": "りんご-肥料",
        },
    ]
    prices_by_id = defaultdict(list)

    # サイトの判別
    def start_requests(self):
        for url_info in self.urls_with_metadata:
            yield scrapy.Request(
                url=url_info["url"],
                callback=self.parse,
                meta={"id": url_info["id"], "category": url_info["category"]},
            )

    def parse(self, response):
        # メタデータを取得
        url_id = response.meta.get("id")
        category = response.meta.get("category")

        if "rakuten" in response.url:
            prices = self.parse_rakuten(response)
        elif "nogyoya" in response.url:
            prices = self.parse_nogyoya(response)
        elif "kokkaen-ec" in response.url:
            prices = self.parse_kokkaen_ec(response)
        elif "monotaro" in response.url:
            prices = self.parse_monotaro(response)
        elif "yahoo" in response.url:
            prices = self.parse_yahoo(response)
        elif "takii" in response.url:
            prices = self.parse_takii(response)
        elif "kakaku" in response.url:
            prices = self.parse_kakaku(response)
        elif "matsuonouen" in response.url:
            prices = self.parse_matsuonouen(response)
        elif "kobayashi" in response.url:
            prices = self.parse_kobayashi(response)
        elif "tanehyo" in response.url:
            prices = self.parse_tanehyo(response)
        elif "hanahiroba" in response.url:
            prices = self.parse_hanahiroba(response)
        else:
            prices = []
        self.prices_by_id[url_id].extend(prices)  # type: ignore

    # サイトにごとの処理の関数
    def parse_kokkaen_ec(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("li", class_="ec-shelfGrid__item")

        prices = []
        for card in cards:
            product_price_tag = card.find("p", class_="price02-default")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_rakuten(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="searchresultitem")

        prices = []  # 価格を格納するリスト

        for card in cards:
            product_price_tag = card.find("div", class_="price--OX_YW")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_nogyoya(self, response):  # カードのどっかが読み取れてない
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all(
            "article", class_="fs-c-productList__list__item fs-c-productListItem"
        )

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find("sapn", class_="fs-c-price__value")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_yahoo(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("li", class_="LoopList__item")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find(
                "span",
                class_="SearchResultItemPrice_SearchResultItemPrice__value__G8pQV",
            )
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_takii(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="image_only clearfix")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find("span", class_="selling_price")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_kakaku(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="p-result_list_wrap")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find("em", class_="p-item_priceNum")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_matsuonouen(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("ul", class_="product")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find("dd", class_="price pf14")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_kobayashi(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("ul", class_="c-grid -xs-15 -l-20")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find("span", class_="p-product-item__price-number")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_monotaro(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="Section u-MarginBottom--24")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find("sapn", class_="Price__EnMark--Md")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_tanehyo(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("ul", class_="product-list")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find("div", class_="product-caption-wrap")
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def parse_hanahiroba(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="fs-c-productList__list")

        prices = []  # 価格を格納するリスト
        for card in cards:
            product_price_tag = card.find(
                "div", class_="fs-c-productPrice fs-c-productPrice--selling"
            )
            if product_price_tag:
                price_text = product_price_tag.get_text(strip=True)
                price_match = re.search(r"\d+", price_text.replace(",", ""))
                if price_match:
                    prices.append(
                        int(price_match.group())
                    )  # 数値型に変換してリストに追加
        return prices

    def closed(self, reason):
        # スクレイピング終了後、平均価格を計算して出力
        for url_id, prices in self.prices_by_id.items():
            if prices:
                average_price = sum(prices) / len(prices)
                print(f"ID: {url_id}, 平均価格: {average_price:.2f}円")
            else:
                print(f"ID: {url_id}, 価格情報が見つかりませんでした。")


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "ERROR",
        }
    )
    process.crawl(AgricultureSpider)
    process.start()
