import requests, logging, re, os, random
from models import Adealsweden, Swedroid, Amazon
from bs4 import BeautifulSoup
from collections import deque


AMAZON_LINK = 'AMAZON_LINK'
ADEALSWEDEN = 'https://www.adealsweden.com/deals/8/'
SWEDROID_USERNAME = 'SWEDROID_USERNAME'
SWEDROID_PASSWORD = 'SWEDROID_PASSWORD'
SWEDROID_LOGIN = 'https://swedroid.se/forum/login/login'
SWEDROID = 'https://swedroid.se/forum/threads/fyndtipstraden-amazon-se-inga-diskussioner.186347/'
PROXY_USERNAME = 'PROXY_USERNAME'
PROXY_PASSWORD = 'PROXY_PASSWORD'
PROXY_HOSTS = ['se.socks.nordhold.net', 'stockholm.se.socks.nordhold.net']

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

    def scrape_adealsweden(self):
        self.logger.info('Scraping adealsweden')
        self.adealsweden.clear()
        response = requests.get(ADEALSWEDEN, timeout=5)
        response_text = response.text
        name_pattern = r'<a\shref\=\"https\:\/\/www\.adealsweden\.com\/[\w\S]+\/\d+\/\"\starget.*>(.*)<'
        price_pattern = r'\<em\>(.*)\<\/em\>\<\/strong\>(.*)\<\/p\>'
        url_pattern = r'\"(https://amzn\.to.*)\"\s'
        name_matches = re.findall(name_pattern, response_text, re.MULTILINE)
        prices_matches = re.findall(price_pattern, response_text, re.MULTILINE)
        url_matches = re.findall(url_pattern, response_text, re.MULTILINE)
        if name_matches and prices_matches and url_matches:
            if self.adealsweden_old:
                tmp = None
                for i, n in enumerate(name_matches):
                    real_url = requests.get(url_matches[i]).url.split('?')[0]
                    if real_url == 'https://www.amazon.se/s':
                        real_url = requests.get(url_matches[i]).url
                    name_match = name_matches[i]
                    if '&#038;' in name_match:
                        name_match = name_match.replace('&#038;', '&')
                    ad = Adealsweden(name_match, ''.join(prices_matches[i]).strip(), real_url)
                    if i == 0:
                        tmp = ad
                    if self.adealsweden_old.name == n:
                        break
                    self.adealsweden.append(ad)
                self.adealsweden_old = tmp
            else:
                real_url = requests.get(url_matches[0]).url.split('?')[0]
                if real_url == 'https://www.amazon.se/s':
                    real_url = requests.get(url_matches[0]).url
                name_match = name_matches[0]
                if '&#038;' in name_match:
                    name_match = name_match.replace('&#038;', '&')
                ad = Adealsweden(name_match, ''.join(prices_matches[0]).strip(), real_url)
                self.adealsweden_old = ad
        self.logger.info(f'Scraped adealsweden.com: {self.adealsweden}')
        return self.adealsweden

    def scrape_swedroid(self):
        self.logger.info('Scraping swedroid')
        self.swedroid.clear()
        proxies = {k: v.format(PROXY_USERNAME=os.getenv(PROXY_USERNAME), PROXY_PASSWORD=os.getenv(PROXY_PASSWORD), PROXY_HOST=random.choice(PROXY_HOSTS)) for k, v in PROXIES.items()}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        session = requests.Session()
        session.get('https://swedroid.se/forum/login')
        response = session.post(url=SWEDROID_LOGIN, proxies=proxies, timeout=5, headers=headers, data=f'login={os.getenv(SWEDROID_USERNAME)}&register=0&password={os.getenv(SWEDROID_PASSWORD)}&remember=1&cookie_check=1&_xfToken=&redirect=https%3A%2F%2Fswedroid.se%2Fforum%2F')
        response = session.get(SWEDROID, timeout=5)
        response_text = response.text
        last_pattern = r'data\-last\=\"(\d+)\"'
        last_matches = re.findall(last_pattern, response_text, re.MULTILINE)
        if last_matches:
            response = session.get(SWEDROID + f'page-{last_matches[0]}')
            response_text = response.text
            url_pattern = r'\<a\shref\=\"(https://www\.amazon\.se.*)\"\starget'
            url_matches = re.findall(url_pattern, response_text, re.MULTILINE)
            if url_matches:
                if self.swedroid_old:
                    tmp = None
                    for i, u in reversed(list(enumerate(url_matches))):
                        droid = Swedroid(url=url_matches[i])
                        if i == len(url_matches)-1:
                            tmp = droid
                        if self.swedroid_old.url == u:
                            break
                        self.swedroid.append(droid)
                    self.swedroid_old = tmp
                else:
                    droid = Swedroid(url=url_matches[-1])
                    self.swedroid_old = droid
        self.logger.info(f'Scraped swedroid.se: {self.swedroid}')
        return self.swedroid

    def scrape_amazon(self):
        self.logger.info('Scraping amazon')
        self.amazon.clear()
        proxies = {k: v.format(PROXY_USERNAME=os.getenv(PROXY_USERNAME), PROXY_PASSWORD=os.getenv(PROXY_PASSWORD), PROXY_HOST=random.choice(PROXY_HOSTS)) for k, v in PROXIES.items()}
        HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
        ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
        ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'}), 
        ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5', 'DNT': '1'})
        response = requests.get(os.getenv(AMAZON_LINK), proxies=proxies, headers=random.choice(HEADERS), timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find(attrs={"class":"s-main-slot"}).findAll(attrs={"class":"s-result-item"})
        data_asin_list = [div["data-asin"] for div in divs if "data-asin" in div.attrs]
        url_matches = [x for x in data_asin_list if x]
        url_matches = list(dict.fromkeys(url_matches))
        url_matches = [f'https://www.amazon.se/dp/{url}' for url in url_matches]
        if url_matches:
            if self.amazon_old:
                new_urls = []
                for i, u in enumerate(url_matches):
                    deal_price = soup.findAll(attrs={"class":"a-price"})[i].findAll('span')[0].text
                    deal_title = soup.findAll(attrs={"class":"s-title-instructions-style"})[i].find('h2').text
                    amaz = Amazon(deal_title, deal_price, u)
                    if amaz not in self.amazon_old:
                        new_urls.append(amaz)
                        self.amazon_old.append(amaz)

                if len(new_urls) > 3:
                    self.logger.info("New products bug")
                    new_urls = []
                elif new_urls:
                    self.logger.info("Found new deals!")
                    self.amazon = new_urls
            else:
                for i, u in enumerate(url_matches):
                    deal_price = soup.findAll(attrs={"class":"a-price"})[i].findAll('span')[0].text
                    deal_title = soup.findAll(attrs={"class":"s-title-instructions-style"})[i].find('h2').text
                    amaz = Amazon(deal_title, deal_price, u)
                    self.amazon_old.append(amaz)
        self.logger.info(f'Scraped amazon.se: {self.amazon}')
        return self.amazon
    

# detailBullets_feature_div ID for asin location
