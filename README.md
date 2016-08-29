# sns_Webscrapper

Clone the files and run locally:

Create a virtualenv with python 2.7

virtualenv webscrape

source webscrape/bin/activate

Install dependencies:

pip install -r webscraper_requirements.txt

Run script as below:

python webscraper.py http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html

Outputs a JSON string:
(webscrape)osboxes@osboxes:~/sns_webcrawl$ python webscraper.py http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html
{"total_product_sum": "15.10", "product_list": [{"size": "38.0kb", "description": "Apricots", "unit_price": 3.5, "title": "Sainsbury's Apricot Ripe & Ready x5"}, {"size": "38.0kb", "description": "Avocados", "unit_price": 1.5, "title": "Sainsbury's Avocado Ripe & Ready XL Loose 300g"}, {"size": "43.0kb", "description": "Avocados", "unit_price": 1.8, "title": "Sainsbury's Avocado, Ripe & Ready x2"}, {"size": "38.0kb", "description": "Avocados", "unit_price": 3.2, "title": "Sainsbury's Avocados, Ripe & Ready x4"}, {"size": "38.0kb", "description": "Conference", "unit_price": 1.5, "title": "Sainsbury's Conference Pears, Ripe & Ready x4 (minimum)"}, {"size": "38.0kb", "description": "Gold Kiwi", "unit_price": 1.8, "title": "Sainsbury's Golden Kiwi x4"}, {"size": "38.0kb", "description": "Kiwi", "unit_price": 1.8, "title": "Sainsbury's Kiwi Fruit, Ripe & Ready x4"}]}


Unit test:

py.test -v test_webscrapper.py
(webscrape)osboxes@osboxes:~/sns_webcrawl$ py.test -v test_webscraper.py 
=========================================================================================== test session starts ============================================================================================
platform linux2 -- Python 2.7.10, pytest-2.9.1, py-1.4.31, pluggy-0.3.1 -- /home/osboxes/webscrape/bin/python2
cachedir: .cache
rootdir: /home/osboxes/sns_webcrawl, inifile: 
collected 11 items 

test_webscraper.py::test_request_html PASSED
test_webscraper.py::test_get_page_size PASSED
test_webscraper.py::test_parse_description PASSED
test_webscraper.py::test_parse_input_price PASSED
test_webscraper.py::test_parse_product_list PASSED
test_webscraper.py::test_parse_product_page_with_no_list PASSED
test_webscraper.py::test_product_list_to_dict_desc PASSED
test_webscraper.py::test_product_list_to_dict_title PASSED
test_webscraper.py::test_product_list_to_dict_size PASSED
test_webscraper.py::test_webscraper_sum PASSED
test_webscraper.py::test_webscraper_product_list PASSED

======================================================================================== 11 passed in 0.32 seconds =========================================================================================

