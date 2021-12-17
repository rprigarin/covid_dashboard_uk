""" Covid News Handling """
# Acquiring news articles through API communication

# Ruslan Prigarin
# 710002810
# 03/11/2021

import logging
from newsapi import NewsApiClient
from config_loading import get_config_data # loads config file
from api_key import get_api_key # !! include your own news API key here

# Logging
logging.basicConfig(filename='logs/covid_dashboard.log', filemode='w', format='%(asctime)s, %(levelname)s - %(message)s')

# Init
newsapi = NewsApiClient(api_key=get_api_key())

# /v2/top-headlines/sources
# sources = newsapi.get_sources()

def news_API_request(covid_terms = get_config_data("news")) -> dict:
    """ Communicates with newsapi to obtain Covid-related news articles """

    try:
        cat, lan = get_config_data("news", 1)

        # /v2/top-headlines
        top_headlines = newsapi.get_top_headlines(q=covid_terms,
                                            category=cat,
                                            language=lan)

        logging.info("(" + __name__ + ") News API connection successful.")

        return top_headlines # returns a dictionary

    except:
        logging.error("(" + __name__ + ") No API key found! Your application will not run as expected. Please refer to the README on how to add the API key.")
        return {'articles': {}} # return empty dictionary if API doesn't work


def update_news(name = "test"):
    """ Updates news (obsolete) """

    pass # :)


def get_max_articles(news = news_API_request()) -> int:
    """ Obtains maximum articles available """

    news_article_count = 0

    if news['articles']:
        for entry in news['articles']:
            news_article_count += 1

    return news_article_count


# Use this function to acquire news
def get_news(i = 0) -> str:
    """ Obtains specific values from the news API articles """

    news = news_API_request()
    total_entries = get_max_articles(news)
    new_i = i # new_i will be modified

    # check that articles exist
    if news['articles']:
        if i >= total_entries:
            new_i = 0

        # if title and content exist
        if(news['articles'][new_i]['title'] and news['articles'][new_i]['content']):
            return news['articles'][new_i]['title'], news['articles'][new_i]['content']

        # if content does not exist, check for title
        elif(news['articles'][new_i]['title']):
            return news['articles'][new_i]['title'], '-'

        # if none of these things exist, return "nothing"
        else:
            return '-', '-'

    # in case articles do not exist...
    else:
        return '-', '-'
