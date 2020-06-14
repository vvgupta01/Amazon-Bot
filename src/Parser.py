def captcha_check(page):
    return page.title.string == 'Robot Check'


def get_name(item):
    return to_text(item.find('span', class_='a-size-medium a-color-base a-text-normal'))


def get_name_alt(item):
    return to_text(item.find('span', class_='a-size-base-plus a-color-base a-text-normal'))


def get_prices(item):
    prices = item.find_all('span', class_='a-offscreen')
    if len(prices) > 0:
        price = float(to_text(prices[0])[1:].replace(',', ''))
        list_price = float(to_text(prices[1])[1:].replace(',', '')) \
            if len(prices) == 2 else None
        return price, list_price
    return None, None


def get_rating(item):
    rating = to_text(item.find('span', class_='a-icon-alt'))
    if rating is not None:
        return float(rating[:3])
    return None


def get_reviews(item):
    reviews = to_text(item.find(lambda tag: tag.name == 'span'
                                and tag.get('class') == ['a-size-base']))
    if reviews is not None:
        return int(reviews.replace(',', ''))
    return 0


def get_stock(item):
    stock = to_text(item.find('span', class_='a-color-price'))
    if stock is not None:
        return int(stock[5:-28])
    return None


def get_prime(item):
    prime = item.find('span', class_='aok-relative s-icon-text-medium s-prime')
    prime = True if prime is not None else False
    return prime


def get_url(item):
    return item.find('a', class_='a-link-normal a-text-normal')['href']


def get_item_name(page):
    name = get_element(page, 'productTitle')
    if name is not None:
        return name
    return None


def get_item_price(page):
    price = get_element(page, 'priceblock_ourprice')
    if price is None:
        price = get_element(page, 'priceblock_saleprice')
    if price is None:
        price = get_element(page, 'priceblock_dealprice')
    if price is not None:
        return float(price[1:])
    return None


def get_list_price(page):
    price = to_text(page.find('span', class_='priceBlockStrikePriceString a-text-strike'))
    if price is not None:
        return float(price[1:])
    return None


def get_availability(page):
    return get_element(page, 'availability')


def to_text(element):
    if element is None:
        return None
    return element.text.strip()


def get_element(page, element_id):
    return to_text(page.find(id=element_id))
