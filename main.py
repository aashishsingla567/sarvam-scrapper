# a bot to scrape data from sarvamsafety.com

# custom imports
from constants import *
from scrapers import *
from files import *

data = {
    "categories": [{
        "products": [{
        }]
    }]
}


def scrape_product_details(product):
    """
        Get the details of a product
    """
    scraper = ProductDetailsScraper(product['link'])
    return scraper.scrape_details()


def scrape_products(category):
    """
        Get the list of all the products in a category
    """
    scraper = ProductsScraper(category['link'])
    return scraper.scrape_products()


def scrape_categories():
    """
        Get the list of all the categories
    """
    scraper = CategoryScraper(SARVAM_URL)
    return scraper.get_categories()


def main():
    """
        STEPS :-
            1. Get the list of all the categories
            2. Get the list of all the products in each category (links)
            3. Get the details of each product (name, price, description, images, etc)
    """
    global data
    # get the list of all the categories

    print('Scraping categories...')
    data['categories'] = scrape_categories()

    # get the list of all the products in each category
    print('Scraping products...')
    for category in data['categories']:
        category['products'] = scrape_products(category)

    print('Saving data to "scraped_data.json"...')
    scraped_data_json = JSONFile("scraped_data.json")
    scraped_data_json.make_pretty(indent=2)
    scraped_data_json.update(data)


if __name__ == '__main__':
    main()
