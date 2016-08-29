"""
    sainsbury webscrapper tool to scan Product Pages.
    Prints a json string of the parsed products:
    {
        'product_list': [{
            'title': <product title>,
            'unit_price': <product unit_price>,
            'size': <product url page size>,
            'description': <product description>
        }],
        'total_product_sum': <sum x.xx>
    }
"""

import json
import re
import sys
import requests
import logging

from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def parse_unit_price(inner_text):
    """
    :param inner_text: HTML inner text: '&pound5.50;/unit'
    :return: Unit price as float value or None
    """
    price_match_expr = re.search(r'\d+(.\d+)?', inner_text)
    if price_match_expr:
        return float(price_match_expr.group())
    return None

def parse_description(page_html):
    """
    :param html: page html data
    :return: Product description string of the first html element found
    """
    soup = BeautifulSoup(page_html, 'html.parser')
    description = soup.select('htmlcontent .productText')[0]
    description = description.get_text().strip()
    return description

def get_page_size(request):

    """
    :param request: page request header
    :return: Returns a string representing the size of the request body
            in kilo bytes.
    """

    content_length = request.headers.get('Content-Length')
    size = int(content_length)
    size = round(size / 1024, 1)
    return '{}kb'.format(size)

def parse_page_data(page):

    """
    :param page: page data to parse
    :return: iterator  Returns an iterator that yields a dictonary :
        {
            'url': <product page url >
            'title': <product title >
            'unit_price': <product unit price>
        }
    """
    if not page:
        raise ValueError('Bad request ')

    soup_data = BeautifulSoup(page, 'html.parser')
    product_list = soup_data.find('ul', attrs={'class': 'productLister'})

    if not product_list:
        raise ValueError('No html element with class \'productLister\'')

    for list_item in product_list.select('li'):
        list_item_title = None
        list_item_uri = None
        list_item_unit_price = None

        list_item_title_html_tag = list_item.select('.productInfo h3 a')
        list_item_price_html_tag = list_item.select('.pricePerUnit')

        if list_item_title_html_tag:
            list_item_title = list_item_title_html_tag[0].get_text().strip()
            list_item_uri = list_item_title_html_tag[0].get('href')

        if list_item_price_html_tag:
            list_item_unit_price = parse_unit_price(list_item_price_html_tag[0].get_text())

        yield {
            'title': list_item_title,
            'uri': list_item_uri,
            'unit_price': list_item_unit_price
        }


def parse_link(page_url):
    """
    :param page_url: url to parse source
    :return: return page request header of the url
    """

    response = requests.get(page_url)
    response.raise_for_status()

    return response


def product_list_to_dict(products):
    """
    :param products: product list
    :return:  - Returns a list of product dictonaries, each dictionary contains :
        {
            'title': <title>
            'unit_price': <unit_price>
            'size': <size>
            'description': <description>
        }
    """

    result = []
    for product in products:
        uri = product.get('uri')
        try:
            product_page_request = parse_link(uri)
        except HTTPError as e:
            logging.error('Bad request, error parsing page %s',e)

        else:
            size = get_page_size(product_page_request)
            description = parse_description(product_page_request.text)

            result.append({
                'title': product.get('title'),
                'unit_price': product.get('unit_price'),
                'size': size,
                'description': description
            })
    return result

def webscraper(url):
    """
    :param url: uri to scan
    :return: product list information and total price
    """

    try:
        response = parse_link(url)
    except HTTPError as e:
        logging.error('Bad request: Error reading the url %s',e)
        sys.exit('Bad Request')

    page_data = response.text

    try:
        product_list = list(parse_page_data(page_data))
    except HTTPError as e:
        logging.error('Error parsing page data %s',e)
        sys.exit('Bad request')

    total_cost = sum([product.get('unit_price') for product in product_list])
    total_cost = format(total_cost, '.2f')
    return {
        'product_list': product_list_to_dict(product_list),
        'total_product_sum': total_cost
    }


if __name__ == '__main__':

    args = sys.argv[1:]
    logging.info('Webscraper tool for argv[1]')

    if len(args) < 1:
        sys.exit('url missing , please specify the url')

    for arg in args:
        products = webscraper(arg)
	print(json.dumps(products))
