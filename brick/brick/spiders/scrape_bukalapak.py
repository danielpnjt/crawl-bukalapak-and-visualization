import scrapy
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from ..items import BrickItem

class DemoSpider(scrapy.Spider):
    name = 'bukalapak_spider'
    start_urls = ['https://www.bukalapak.com/']

    def parse(self, response, **kwargs):
        item = BrickItem()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        urls = ['https://www.bukalapak.com/c/fashion-pria/sepatu-169/boots',
                'https://www.bukalapak.com/c/fashion-pria/sepatu-169/sneaker-pria',
                'https://www.bukalapak.com/c/fashion-pria/kaos-165',
                'https://www.bukalapak.com/c/fashion-pria/celana-299/celana-panjang',
                'https://www.bukalapak.com/c/fashion-pria/tas-pria/selempang']
        for url in urls:
            driver.get(url)
            # assumption 1 page is 50 data, so if 500 data need 10 pages, so i give the last page is 12
            last_page = 25
            lp = int(last_page)-2
            count = 0
            for i in range(lp):
                driver.execute_script("window.scrollTo(0, 1000);")
                time.sleep(0.5)

                all_link = []
                link_elements = driver.find_elements_by_xpath('//*[@class="bl-flex-item mb-8"]/div/div/div[2]/div[1]/p/a')
                for link in link_elements:
                    href = link.get_attribute("href")
                    all_link.append(href)

                for link in all_link:
                    driver.get(link)
                    try:
                        name_product = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/h1').text
                    except NoSuchElementException:
                        name_product = '-'
                    try:
                        category = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/a').text
                    except NoSuchElementException:
                        category = '-'
                    try:
                        rating = driver.find_element_by_xpath('//*[@id="section-ulasan-barang"]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/span').text
                    except NoSuchElementException:
                        rating = '-'
                    try:
                        name_store = driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[1]/div[1]/h3/a').text
                    except NoSuchElementException:
                        name_store = '-'
                    try:
                        price = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[2]/div/div/div[2]/div/span').text
                    except NoSuchElementException:
                        price = '-'
                    
                    item['name'] = name_product
                    item['category'] = category
                    item['rating'] = rating
                    item['name_store'] = name_store
                    item['price'] = price
                    yield item

                driver.get(url + '?page=' + str(i+2))