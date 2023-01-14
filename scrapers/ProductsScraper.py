import requests
from bs4 import BeautifulSoup


class ProductsScraper:
    def __init__(self, url):
        self.url = url
        self.products = []

    def __find_product_link_element(self, soup):
        # find all elements that contains the product details
        # if the product is a product, the element is a 'div' with class 'product'
        return soup.find('div', {'class': 'product-image-container'})

    def __find_products(self, soup):
        return soup.find_all('div', {'class': 'product-item-container'})

    def __find_description(self, soup):
        # find the description of the product
        description = soup.find('div', {'class': 'description'}).find('p')
        return description.get_text()

    def __find_price(self, soup):
        # find the price of the product
        price = soup.find('div', {'class': 'price'})
        return price.get_text()

    def scrape_products(self):
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

        product_items = self.__find_products(soup)
        for item in product_items:
            # find the link to the product details page
            link_element = self.__find_product_link_element(item)
            description = self.__find_description(item).strip()
            price = self.__find_price(item).strip()
            image = link_element.find('img').get('src')
            link = link_element.find('a').get('href')
            name = link_element.find('img').get('alt').strip()
            self.products.append({
                'name': name,
                'link': link,
                'image': image,
                'description': description,
                'price': price,
                'images': [image]
            })
        return self.products

    def get_products(self):
        if (len(self.products) == 0):
            self.get_products()
        return self.products

    def get_products_links(self):
        if (len(self.products) == 0):
            self.get_products()
        return [product['link'] for product in self.products]
