""" Config file loading """

# Ruslan Prigarin
# 710002810
# 16/12/2021

import logging

CONFIG_FILE = "config.json"

logging.basicConfig(filename='logs/covid_dashboard.log', filemode='w', level=logging.INFO, format='%(asctime)s, %(levelname)s - %(message)s')


def __process_config_data(config_data: str) -> str:
    """ Processes config-related data in __set_config_data_news() """

    new_data = ""

    counter = 0
    for c in range(len(config_data)):
        if counter > config_data.index('"') and counter < config_data.rindex('"'):
            new_data += config_data[counter]
        counter += 1

    return new_data


def __set_config_data_news(mode = 0) -> str:
    """ Sets out info and mode specifications for config news data """

    final_news_parameters = []
    backup_news_parameters = ['Covid COVID-19 coronavirus', 'health', 'en'] # in case of exceptions
    final_data = ""

    # open config file
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
            for i, line in enumerate(config_file):
                if i == 5:
                    config_data = line
                    final_news_parameters.append(__process_config_data(config_data)) # NEWS_TERMS
                if i == 6:
                    config_data = line
                    final_news_parameters.append(__process_config_data(config_data)) # NEWS_CATEGORY
                if i == 7:
                    config_data = line
                    final_news_parameters.append(__process_config_data(config_data)) # NEWS_LANGUAGE

    # raise exception if missing
    except FileNotFoundError:
        logging.error("(" + __name__ + ") Config file not found! Using default news parameters...")
        final_news_parameters = backup_news_parameters
    # default exception (shouldn't get this)

    except:
        logging.error("(" + __name__ + ") Unknown error!")
        final_news_parameters = backup_news_parameters

    if mode == 0: # terms only (test requirement)
        return final_news_parameters[0]
    if mode == 1: # category and language only
        return final_news_parameters[1], final_news_parameters[2]
    if mode == 2: # return all
        return final_news_parameters[0], final_news_parameters[1], final_news_parameters[2]


def __set_config_data_covid(mode = 0) -> str:
    """ Sets out info and mode specifications for config covid data """

    final_covid_parameters = []
    backup_covid_parameters = ['Exeter', 'ltla', 'England', 'nation'] # in case of exceptions
    final_data = ""

    # open config file
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
            for i, line in enumerate(config_file):
                if i == 0:
                    config_data = line
                    final_covid_parameters.append(__process_config_data(config_data)) # DATA_LOCAL_AREA
                if i == 1:
                    config_data = line
                    final_covid_parameters.append(__process_config_data(config_data)) # DATA_LOCAL_TYPE
                if i == 2:
                    config_data = line
                    final_covid_parameters.append(__process_config_data(config_data)) # DATA_NATION_AREA
                if i == 3:
                    config_data = line
                    final_covid_parameters.append(__process_config_data(config_data)) # DATA_NATION_TYPE

    # raise exception if missing
    except FileNotFoundError:
        logging.error("(" + __name__ + ") Config file not found! Using default news parameters...")
        final_covid_parameters = backup_covid_parameters
    # default exception (shouldn't get this)

    except:
        logging.error("(" + __name__ + ") Unknown error!")
        final_covid_parameters = backup_covid_parameters

    if mode == 0: # return all
        return final_covid_parameters[0], final_covid_parameters[1], final_covid_parameters[2], final_covid_parameters[3]
    if mode == 1: # return local
        return final_covid_parameters[0], final_covid_parameters[1]
    if mode == 2: # return nation
        return final_covid_parameters[2], final_covid_parameters[3]
    if mode == 3: # return local name only
        return final_covid_parameters[0]
    if mode == 4: # return nation name only
        return final_covid_parameters[2]


def get_config_data(config_index = "", mode = 0) -> str:
    """ Gets config data """

    if config_index == "data":
        return __set_config_data_covid(mode)
    if config_index == "news":
        return __set_config_data_news(mode)

def get_location(location_scope = "local") -> str:
    """ Gets location names """

    # scope 0 is local (default)
    if location_scope == "local":
        return __set_config_data_covid(3)
    
    # scope 1 is national
    elif location_scope == "national":
        return __set_config_data_covid(4)
        
    else:
        logging.warning("(" + __name__ + ") Unknown parameter for location! Using default location scope...")
        return __set_config_data_covid(3)

def get_repeat_interval() -> int:
    """ Gets update repeat parameter (24 hours by default) """

    backup_update = 86400
    final_update = 0

    try:
        with open("config.txt", "r", encoding="utf-8") as config_file:
            for i, line in enumerate(config_file):
                if i == 9:
                    temp_update = line
                    final_update = int(__process_config_data(temp_update)) # UPDATE_REPEAT_INTERVAL

    # raise exception if missing
    except FileNotFoundError:
        logging.error("(" + __name__ + ") Config file not found! Using default news parameters...")
        final_update = backup_update

    # default exception (shouldn't get this)
    except:
        logging.error("(" + __name__ + ") Unknown error!")
        final_update = backup_update

    return final_update
