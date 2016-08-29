import sys

from mock import Mock
from mock import patch

import pytest
import requests

import webscraper as scraper


@patch('requests.get')
def test_request_html(mock_get):
    uri = 'http://shopping_site.com/b'
    requests_mock = Mock()
    mock_get.return_value = requests_mock

    res = scraper.parse_link(uri)

    requests.get.assert_called_once_with(uri)
    requests_mock.raise_for_status.assert_called_once_with()
    assert res == requests_mock

def test_get_page_size():
    mock_request = Mock()
    mock_request.headers = {
        'Content-Length': 2048
    }
    assert scraper.get_page_size(mock_request) == '2.0kb'


def test_parse_description():
    description = 'a product description'
    html = """
        <div>
            <htmlcontent>
                <div></div>
                <div class='productText'><p>{}</p>\n\t<p></p></div>
                <div class='productText'><p>Sainsbury Apple</p>\n\t<p></p></div>
            </htmlcontent>
        </div>
    """
    html = html.format(description)
    assert scraper.parse_description(html) == description

def test_parse_input_price():
    assert scraper.parse_unit_price('&pound3.50;/unit') == 3.50
    assert scraper.parse_unit_price('&pound4.abc;/unit') == 4.0
    assert scraper.parse_unit_price('&pound;/unit') is None


def test_parse_product_list():
    href_1 = 'http://shopping_site1.com'
    title_1 = 'product_1 title'
    price_1 = 1.85
    href_2 = 'http://shopping_site2.com'
    title_2 = 'product_2 title'
    price_2 = 3.25
    html = """
        <ul class="productLister">
            <li>
                <div class="productInfo">
                    <h3>
                        <a href="{href_1}">
                            {title_1}
                        </a>
                    </h3>
                </div>
                <div class="pricePerUnit"><p>'&pound{price_1};/unit'</p></div>
            </li>
            <li>
                <div class="productInfo">
                    <h3>
                        <a href="{href_2}">
                            {title_2}
                        </a>
                    </h3>
                </div>
                <div class="pricePerUnit"><p>'&pound{price_2};/unit'</p></div>
            </li>
        </ul>
    """
    html = html.format(
        href_1=href_1,
        title_1=title_1,
        price_1=price_1,
        href_2=href_2,
        title_2=title_2,
        price_2=price_2
        )
    product_list = scraper.parse_page_data(html)
    res = next(product_list)
    assert res.get('title') == title_1
    assert res.get('uri') == href_1
    assert res.get('unit_price') == price_1
    res = next(product_list)
    assert res.get('title') == title_2
    assert res.get('uri') == href_2
    assert res.get('unit_price') == price_2

def test_parse_product_page_with_no_list():
    html = '<ul class="productLister"></ul>'
    product_list = scraper.parse_page_data(html)
    assert list(product_list) == []

@patch('webscraper.parse_link')
@patch('webscraper.get_page_size')
@patch('webscraper.parse_description')
def test_product_list_to_dict_desc(desc_mock, size_mock, req_mock):
    products = [{'uri': ''}, {'uri': ''}]
    desc_mock.side_effect = ['description1', 'description2']
    res = scraper.product_list_to_dict(products)
    assert desc_mock.call_count == 2
    assert res[0]['description'] == 'description1'
    assert res[1]['description'] == 'description2'

@patch('webscraper.parse_link')
@patch('webscraper.get_page_size')
@patch('webscraper.parse_description')
def test_product_list_to_dict_title(desc_mock, size_mock, req_mock):
    products = [{'title': 'title1'}, {'title': 'title2'}]
    res = scraper.product_list_to_dict(products)
    assert res[0]['title'] == 'title1'
    assert res[1]['title'] == 'title2'

@patch('webscraper.parse_link')
@patch('webscraper.get_page_size')
@patch('webscraper.parse_description')
def test_product_list_to_dict_size(desc_mock, size_mock, req_mock):
    products = [{'uri': ''}, {'uri': ''}, {'uri':''}]
    size_mock.side_effect = ['3kb', '7kb', '1kb']
    res = scraper.product_list_to_dict(products)

    assert size_mock.call_count == 3
    assert res[0]['size'] == '3kb'
    assert res[1]['size'] == '7kb'
    assert res[2]['size'] == '1kb'

@patch('webscraper.product_list_to_dict')
@patch('webscraper.parse_page_data')
@patch('webscraper.parse_link')
def test_webscraper_sum(req_mock, prod_list_mock, construct_list_mock):
    prod_list_mock.return_value = [{'unit_price': 2.0}, {'unit_price': 2.0}]
    res = scraper.webscraper('')
    assert res.get('total_product_sum') == '4.00'

@patch('webscraper.product_list_to_dict')
@patch('webscraper.parse_page_data')
@patch('webscraper.parse_link')
def test_webscraper_product_list(req_mock, prod_list_mock, construct_list_mock):
    prod_list = [{'title': 'test'}, {'title': 'test2'}]
    construct_list_mock.return_value = prod_list
    res = scraper.webscraper('')
    assert res.get('product_list') == prod_list

