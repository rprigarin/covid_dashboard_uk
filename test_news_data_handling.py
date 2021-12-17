""" Tests for covid_news_handling.py """

import logging
from covid_news_handling import news_API_request
from covid_news_handling import update_news

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

    logging.info("(" + __name__ + ") \"test_news_API_request\" passed.")

def test_update_news():
    update_news('test')

    logging.info("(" + __name__ + ") \"test_update_news\" passed.")


test_news_API_request()
test_update_news()