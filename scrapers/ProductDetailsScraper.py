import requests
from bs4 import BeautifulSoup


class ProductDetailsScraper:
    def __init__(self, url):
        self.url = url
        self.product = {}

    def __find_description(self, soup):
        # find the description of the product
        description = soup.find('div', {'id': 'tab-description'})
        return description.get_text() if description else None

    def __find_images(self, soup):
        # find the images of the product
        images = soup.find_all('img', {'class': 'product-image'})
        return [image.get('src') for image in images] if images else None

    def __find_price(self, soup):
        # find the price of the product
        price = soup.find('div', {'itemprop': 'price'})
        return price.get_text() if price else None

    def scrape_details(self):
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            print("Error getting the data from :", self.url, e)
            raise SystemExit(e)

        soup = None
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print("Error parsing the data from :", response.text, e)
            raise SystemExit(e)

        description = self.__find_description(soup)
        images = self.__find_images(soup)
        price = self.__find_price(soup)

        self.product = {
            "link": self.url,
            "description": description,
            "images": images,
        }
        return self.product

    def get_product(self):
        if (not self.product):
            self.get_details()
        return self.product
