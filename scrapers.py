import requests, logging, re, os, random
from models import Amazon #, Adealsweden, Swedroid
from bs4 import BeautifulSoup
from collections import deque
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


AMAZON_LINK = 'AMAZON_LINK'
ADEALSWEDEN = 'https://www.adealsweden.com/deals/'
SWEDROID_USERNAME = 'SWEDROID_USERNAME'
SWEDROID_PASSWORD = 'SWEDROID_PASSWORD'
SWEDROID_LOGIN = 'https://swedroid.se/forum/login/login'
SWEDROID = 'https://swedroid.se/forum/threads/fyndtipstraden-amazon-se-inga-diskussioner.186347/'
PROXY_USERNAME = 'PROXY_USERNAME'
PROXY_PASSWORD = 'PROXY_PASSWORD'
PROXY_HOSTS = ['se.socks.nordhold.net', 'stockholm.se.socks.nordhold.net']
HAGGLEZON = 'https://www.hagglezon.com/en/s/'

HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'})


PROXIES = {
    'http': f'socks5://{{PROXY_USERNAME}}:{{PROXY_PASSWORD}}@{{PROXY_HOST}}:1080'
}


class Scrapers():

    def __init__(self):
        self.logger = logging.getLogger('discord')
        self.adealsweden = []
        self.adealsweden_old = None
        self.swedroid = []
        self.swedroid_old = None
        self.amazon = []
        self.amazon_old = deque(maxlen=300)

    # def scrape_adealsweden(self):
    #     self.logger.info('Scraping adealsweden')
    #     self.adealsweden.clear()
    #     options = uc.ChromeOptions()
    #     options.add_argument("--headless")
    #     options.add_argument("--no-sandbox")
    #     options.add_argument("--disable-dev-shm-usage")
    #     options.add_argument("--disable-gpu")
    #     driver = uc.Chrome(options=options)
    #     driver.get(ADEALSWEDEN)
    #     WebDriverWait(driver, 10).until(EC.title_contains("Active Deals - Adealsweden"))
    #     response = driver.page_source
    #     driver.quit()
    #     response_text = response
    #     name_pattern = r'<a\shref\=\"https\:\/\/www\.adealsweden\.com\/[\w\S]+\/\d+\/\"\starget.*>(.*)<'
    #     price_pattern = r'\<em\>(.*)\<\/em\>\<\/strong\>(.*)\<\/p\>'
    #     url_pattern = r'(?<!>)https://amzn\.to/[^\s"]+'
    #     name_matches = re.findall(name_pattern, response_text, re.MULTILINE)
    #     prices_matches = re.findall(price_pattern, response_text, re.MULTILINE)
    #     url_matches = re.findall(url_pattern, response_text, re.MULTILINE)
    #     print(url_matches[0])
    #     if name_matches and prices_matches and url_matches:
    #         if self.adealsweden_old:
    #             tmp = None
    #             for i, n in enumerate(name_matches):
    #                 try:
    #                     real_url = requests.get(url_matches[i], timeout=8).url.split('?')[0]
    #                     if real_url == 'https://www.amazon.se/s':
    #                         real_url = requests.get(url_matches[i]).url
    #                     name_match = n
    #                     if '&#8211;' in name_match:
    #                         name_match = name_match.replace('&#8211;', '-')
    #                     ad = Adealsweden(name_match, ''.join(prices_matches[i]).strip(), real_url)
    #                     if i == 0:
    #                         tmp = ad
    #                     if self.adealsweden_old.name == name_match:
    #                         break
    #                     self.adealsweden.append(ad)
    #                 except:
    #                     self.logger.info("Adealsweden url_matches timeout")
    #             self.adealsweden_old = tmp
    #         else:
    #             real_url = requests.get(url_matches[0]).url.split('?')[0]
    #             if real_url == 'https://www.amazon.se/s':
    #                 real_url = requests.get(url_matches[0]).url
    #             name_match = name_matches[0]
    #             if '&#8211;' in name_match:
    #                 name_match = name_match.replace('&#8211;', '-')
    #             ad = Adealsweden(name_match, ''.join(prices_matches[0]).strip(), real_url)
    #             self.adealsweden_old = ad
    #     self.logger.info(f'Scraped adealsweden.com: {self.adealsweden}')
    #     return self.adealsweden

    # def scrape_swedroid(self):
    #     self.logger.info('Scraping swedroid')
    #     self.swedroid.clear()
    #     proxies = {k: v.format(PROXY_USERNAME=os.getenv(PROXY_USERNAME), PROXY_PASSWORD=os.getenv(PROXY_PASSWORD), PROXY_HOST=random.choice(PROXY_HOSTS)) for k, v in PROXIES.items()}
    #     session = requests.Session()
    #     session.proxies = proxies
    #     session.headers = random.choice(HEADERS)
    #     response = session.get(SWEDROID_LOGIN, timeout=8)
    #     response = session.post(SWEDROID_LOGIN, timeout=8, data={
    #         'login': os.getenv(SWEDROID_USERNAME),
    #         'password': os.getenv(SWEDROID_PASSWORD),
    #         'remember': '1',
    #         'cookie_check': '1',
    #         'redirect': 'https://swedroid.se/forum/'
    #     })
    #     response = session.get(SWEDROID, timeout=8)
    #     response_text = response.text
    #     last_pattern = r'data\-last\=\"(\d+)\"'
    #     last_matches = re.findall(last_pattern, response_text, re.MULTILINE)
    #     if last_matches:
    #         response = session.get(SWEDROID + f'page-{last_matches[0]}')
    #         response_text = response.text
    #         url_pattern = r'\<a\shref\=\"(https://www\.amazon\.se.*)\"\starget'
    #         url_matches = re.findall(url_pattern, response_text, re.MULTILINE)
    #         if url_matches:
    #             if self.swedroid_old:
    #                 tmp = None
    #                 for i, u in reversed(list(enumerate(url_matches))):
    #                     droid = Swedroid(url=url_matches[i])
    #                     if i == len(url_matches)-1:
    #                         tmp = droid
    #                     if self.swedroid_old.url == u:
    #                         break
    #                     self.swedroid.append(droid)
    #                 self.swedroid_old = tmp
    #             else:
    #                 droid = Swedroid(url=url_matches[-1])
    #                 self.swedroid_old = droid
    #     self.logger.info(f'Scraped swedroid.se: {self.swedroid}')
    #     return self.swedroid

    def scrape_amazon(self):
        self.logger.info('Scraping amazon')
        self.amazon.clear() 
        proxies = {k: v.format(PROXY_USERNAME=os.getenv(PROXY_USERNAME), PROXY_PASSWORD=os.getenv(PROXY_PASSWORD), PROXY_HOST=random.choice(PROXY_HOSTS)) for k, v in PROXIES.items()}
        response = requests.get(os.getenv(AMAZON_LINK), proxies=proxies, headers=random.choice(HEADERS), timeout=8)
        soup = BeautifulSoup(response.text, 'html.parser')
        data_asin_list = [div["data-asin"] for div in soup.select('.s-result-item[data-asin]')]
        asin_list = [x for x in data_asin_list if x]
        url_matches = []
        self.logger.info(soup)
        for div in soup.select('.s-result-item[data-asin]'):
            anchor_tag = div.find('a', class_='a-link-normal s-no-outline')
            if anchor_tag:
                href_link = anchor_tag.get('href')
                clean_url = href_link.split('/ref=')[0]
                url_matches.append(f'https://www.amazon.se{clean_url}')
        if url_matches:
            if self.amazon_old:
                new_urls = []
                for i, u in enumerate(url_matches):
                    try:
                        deal_price = soup.find('div', {'data-asin': asin_list[i]}).find(attrs={"class":"a-price"}).findAll('span')[0].text
                        if '\xa0' in deal_price:
                            deal_price = deal_price.replace('\xa0', ' ')
                    except:
                        deal_price = None
                    try:
                        deal_title = soup.find('div', {'data-asin': asin_list[i]}).find(attrs={"class":"s-title-instructions-style"}).find('h2').text
                    except:
                        deal_title = None
                    amaz = Amazon(deal_title, deal_price, u, None)
                    if amaz.url not in [x.url for x in self.amazon_old]:
                        product_asin = amaz.url.split("/")[-1]
                        try:
                            response = requests.get(f'{HAGGLEZON}{product_asin}', proxies=proxies, headers=random.choice(HEADERS), timeout=8)
                            try:
                                soup = BeautifulSoup(response.text, 'html.parser')
                                list_prices = soup.find(attrs={"class":"search-results-container"}).find(attrs={"class":"list-prices"})
                                country_list = [f.find('img')['alt'] for f in list_prices.findAll('figure', {'class': 'flag'})]
                                price_list = [price.find('span', class_='price-value').text.replace('\xa0', ' ') for price in list_prices]
                                combined_list = [f'amazon.{country} {price}' for country, price in zip(country_list, price_list)]
                                hagglezon_result = '\n'.join(combined_list)
                            except:
                                hagglezon_result = 'ASIN was not found on hagglezon'
                        except:
                            hagglezon_result = 'Could not reach hagglezon'
                        
                        if amaz.price == None or amaz.name == None:
                            return
                        else:
                            new_amaz = Amazon(amaz.name, amaz.price, amaz.url, hagglezon_result)
                            new_urls.append(new_amaz)
                            self.amazon_old.append(new_amaz)
                        
                if len(new_urls) > 6:
                    self.logger.info("New products bug")
                    new_urls = []
                elif new_urls:
                    self.logger.info("Found new deals!")
                    self.amazon = new_urls
            else:
                response_page2 = requests.get(f'{os.getenv(AMAZON_LINK)}&page=2', proxies=proxies, headers=random.choice(HEADERS), timeout=8)
                soup_page2 = BeautifulSoup(response_page2.text, 'html.parser')
                data_asin_list = [div["data-asin"] for div in soup_page2.select('.s-result-item[data-asin]')]
                asin_list = [x for x in data_asin_list if x]
                page2_urls = []
                for div in soup_page2.select('.s-result-item[data-asin]'):
                    anchor_tag = div.find('a', class_='a-link-normal s-no-outline')
                    if anchor_tag:
                        href_link = anchor_tag.get('href')
                        clean_url = href_link.split('/ref=')[0]
                        page2_urls.append(f'https://www.amazon.se{clean_url}')
                for i, u in enumerate(page2_urls):
                    try:
                        deal_price = soup.find('div', {'data-asin': asin_list[i]}).find(attrs={"class":"a-price"}).findAll('span')[0].text
                    except:
                        deal_price = None
                    try:
                        deal_title = soup.find('div', {'data-asin': asin_list[i]}).find(attrs={"class":"s-title-instructions-style"}).find('h2').text
                    except:
                        deal_title = None
                    amaz = Amazon(deal_title, deal_price, u, None)
                    self.amazon_old.append(amaz)
                for i, u in enumerate(url_matches):
                    try:
                        deal_price = soup.find('div', {'data-asin': asin_list[i]}).find(attrs={"class":"a-price"}).findAll('span')[0].text
                    except:
                        deal_price = None
                    try:
                        deal_title = soup.find('div', {'data-asin': asin_list[i]}).find(attrs={"class":"s-title-instructions-style"}).find('h2').text
                    except:
                        deal_title = None
                    amaz = Amazon(deal_title, deal_price, u, None)
                    self.amazon_old.append(amaz)
        self.logger.info(f'Scraped amazon.se: {self.amazon}')
        return self.amazon
