import requests
import threading
from multiprocessing import Manager
import time

from bs4 import BeautifulSoup
import Parser
import Utils


class AmazonBot:
    URL = 'https://www.amazon.com'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
               'Accept-Encoding': 'gzip, deflate',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'DNT': '1', "Connection": 'close', 'Upgrade-Insecure-Requests': '1'}
    MAX_ATTEMPTS = 10

    def __init__(self):
        self.url = None

    def query(self, query, pages, limit, sort, ascending):
        self.url = AmazonBot.URL + '/s?k=' + query
        return self.get_products(pages, limit, sort, ascending)

    def retrieve(self, url, errors):
        return self.get_item(url, errors)

    @staticmethod
    def connect(url, errors, attempts):
        attempts += 1
        try:
            page = requests.get(url, headers=AmazonBot.HEADERS)
        except requests.exceptions.RequestException:
            errors.append('RequestError')
            return None

        page = BeautifulSoup(page.content, 'lxml')
        if Parser.captcha_check(page):
            errors.append('CAPTCHAError')
            if attempts < AmazonBot.MAX_ATTEMPTS:
                return AmazonBot.connect(url, errors, attempts)
            return None
        return page

    def get_products(self, pages, limit, sort, ascending):
        manager = Manager()
        queue = manager.Queue()
        threads = []
        errors = []

        start_time = time.time()
        for page in range(1, pages + 1):
            thread = threading.Thread(target=self.get_page,
                                      args=(errors, page, queue, limit))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
        total_time = int((time.time() - start_time) * 1000)

        if len(errors) > 0:
            if 'RequestError' in errors:
                print(f'Error: Unable to connect to {AmazonBot.URL}. Please check your connection.\n')
            if 'CAPTCHAError' in errors:
                print('Error: Unable to query due to CAPTCHA\n')
            if 'ValueError' in errors:
                print('Error: Unable to find item at URL. Please verify that the URL is valid.\n')
            return None
        elif queue.qsize() == 0:
            print('No results found for query\n')
            return None

        data = AmazonBot.extract_queue(queue)
        columns = ['NAME', 'LIST_PRICE', 'PRICE', 'RATING', 'REVIEWS', 'STOCK', 'PRIME', 'URL']
        df = Utils.create_df(data, columns)
        if 0 < limit < df.shape[0]:
            df = df.head(limit)
        df = Utils.clean_df(df, sort, ascending)

        msg = f'Retrieved {df.shape[0]} products from {pages} pages in {total_time}ms'
        if sort != 'NONE':
            order_str = 'ascending' if ascending else 'descending'
            msg += f', sorted by {sort.lower()} in {order_str} order'
        print(msg)
        return df

    def get_page(self, errors, page, queue, limit):
        url = self.url + '&page=' + str(page)
        page = AmazonBot.connect(url, errors, 0)
        if page is not None:
            norm_format = True
            items = page.findAll('div', attrs={
                'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 '
                         'sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'})
            if len(items) == 0:
                norm_format = False
                items = page.findAll('div', attrs={
                    'class': 'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item '
                             's-asin sg-col-4-of-28 sg-col-4-of-16 sg-col '
                             'sg-col-4-of-20 sg-col-4-of-32'})

            for item in items:
                try:
                    name = Parser.get_name(item) if norm_format else Parser.get_name_alt(item)
                    price, list_price = Parser.get_prices(item)
                    rating = Parser.get_rating(item)
                    reviews = Parser.get_reviews(item)
                    stock = Parser.get_stock(item)
                    is_prime = Parser.get_prime(item)
                    url = AmazonBot.URL + Parser.get_url(item)
                    queue.put([name, list_price, price, rating, reviews, stock, is_prime, url])
                except ValueError:
                    errors.append('ValueError')
                    return
                if queue.qsize() >= limit > 0:
                    return

    @staticmethod
    def get_item(url, errors):
        start_time = time.time()
        page = AmazonBot.connect(url, errors, 0)
        if len(errors) > 0:
            if 'RequestError' in errors:
                print(f'Error: Unable to connect to {url}.\n'
                      f'Check your connection and verify that the URL is valid.\n')
            if 'CAPTCHAError' in errors:
                print('Error: Unable to query due to CAPTCHA.\n')
            return None

        try:
            name = Parser.get_item_name(page)
            if name is None:
                raise ValueError
            list_price = Parser.get_list_price(page)
            price = Parser.get_item_price(page)
            availability = Parser.get_availability(page)
            total_time = int((time.time() - start_time) * 1000)
            print(f'Retrieved item information in {total_time}ms')
            return [name, list_price, price, availability]
        except ValueError:
            print('Error: Unable to find item at URL. Please verify that the URL is valid.\n')
            return None

    @staticmethod
    def extract_queue(queue):
        data = []
        while not queue.empty():
            data.append(queue.get())
        return data
