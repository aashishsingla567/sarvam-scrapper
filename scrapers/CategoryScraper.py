import requests
from bs4 import BeautifulSoup


class CategoryScraper:
    def __init__(self, url):
        self.url = url
        self.categories = []

    def __find_categories(self, soup):
        megamenu = soup.find('ul', {'class': 'megamenu'})
        menuitems = megamenu.find_all('li')
        return menuitems

    def get_categories(self):
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

        categories = self.__find_categories(soup)

        for category in categories:
            # find the links to the category pages
            link = category.find('a').get('href')
            # find the name of the category
            name = category.find('a').get_text()
            name = name.strip()
            self.categories.append({
                'name': name,
                'link': link
            })
        return self.categories

    def get_category_links(self):
        if (len(self.categories) == 0):
            self.get_categories()
        return [category['link'] for category in self.categories]
