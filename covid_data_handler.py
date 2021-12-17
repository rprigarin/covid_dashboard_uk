""" Covid Data Handler """
# Acquiring COVID data through API communication

# Ruslan Prigarin
# 71002810
# 03/11/2021


# Import useful modules

import time     # used with sched
import sched    # automatic updates
import logging
import requests # uk_covid19 API access
from uk_covid19 import Cov19API
from config_loading import get_config_data # loads config file

# Update scheduler
updater = sched.scheduler(time.time, time.sleep)

# Logging
logging.basicConfig(filename='logs/covid_dashboard.log', filemode='w', format='%(asctime)s, %(levelname)s - %(message)s')


def parse_csv_data(csv_filename) -> list:
    """ Parses CSV data using the sample file (testing purposes only) """

    # open the file specified
    data_file = open(csv_filename, "r", encoding="utf-8")

    csv_row_list = []
    csv_processed = data_file.readlines()

    for i in csv_processed:
        if i: # checks if row is empty
            csv_row_list.append(i.rstrip()) # append rows of data strings into list

    # return a list of strings for the rows in the file (test with nation_2021-10-28.csv)

    data_file.close() # close file first

    logging.info("(" + __name__ + ") The CSV file has been read.")

    return csv_row_list


def parse_csv_data_api(csv_filename) -> list:
    """ Parses of CSV data using API """

    csv_row_list = []
    csv_processed = csv_filename.split('\n')

    for i in csv_processed:
        if i: # checks if row is empty
            csv_row_list.append(i.rstrip()) # append rows of data strings into list

    # return a list of strings for the rows in the file (test with nation_2021-10-28.csv)

    return csv_row_list


def process_covid_csv_data(covid_csv_data) -> int:
    """ Processes of CSV data """

    # store input into a local variable
    csv_raw_data = covid_csv_data

    data_length = len(csv_raw_data)

    # segment rows of data
    csv_seg_data = []
    for i in range(len(csv_raw_data)):
        csv_seg_data.append(csv_raw_data[i].split(","))
        if i > 0: # if not first line
            if csv_seg_data[i][4]: # if not empty
                csv_seg_data[i][4] = int(csv_seg_data[i][4]) # convert type to int
            if csv_seg_data[i][5]:
                csv_seg_data[i][5] = int(csv_seg_data[i][5])
            if csv_seg_data[i][6]:
                csv_seg_data[i][6] = int(csv_seg_data[i][6])

    # variables to process then return
    num_cases_in_seven_days = 0
    num_cases_hospitalised = 0
    num_deaths = 0

    # get 7 days
    seven_day_counter = 0
    for i in range(data_length):
        if i == 2:
            continue # skip incomplete data
        if csv_seg_data[i][6] and i > 0:
            num_cases_in_seven_days += csv_seg_data[i][6]
            seven_day_counter += 1

        if seven_day_counter == 7:
            break

    # get hospitalised cases data (most recent)
    for i in range(data_length):
        if csv_seg_data[i][5] and i > 0:
            num_cases_hospitalised = csv_seg_data[i][5]
            break # leave after acquiring data

    # get deaths
    for i in range(data_length):
        if csv_seg_data[i][4] and i > 0:
            num_deaths = csv_seg_data[i][4]
            break

    # return the three vars
    return num_cases_in_seven_days, num_cases_hospitalised, num_deaths


def covid_API_request(location="Exeter", location_type="ltla") -> dict:
    """ Communicates with uk_covid19 API for data """

    # endpoint: https://api.coronavirus.data.gov.uk/v1/data

    uk_data = requests.get("https://api.coronavirus.data.gov.uk/v1/data")

    uk_data_filter = [                  # filter is list
        'areaType=' + location_type,
        'areaName=' + location
    ]

    uk_data_struct = {                  # structure is dictionary
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }

    # do API things
    uk_covid_api = Cov19API(filters=uk_data_filter, structure=uk_data_struct)

    # get stuff from API (CSV / JSON)
    #data_csv = uk_covid_api.get_csv()
    data_json = uk_covid_api.get_json()

    logging.info("(" + __name__ + ") Covid API connection successful.")

    # return COVID data
    return data_json # complying with assignment requirements


def covid_JSON_to_CSV(uk_covid_data_json) -> str:  # !! personal additional
    """ Attemptes conversion of provided data from JSON to CSV """

    # append to list
    json_row_list = []

    # complying with pylint :^)
    area_code = "areaCode,"
    area_name = "areaName,"
    area_type = "areaType,"
    date = "date,"
    deaths = "cumDailyNsoDeathsByDeathDate,"
    hosp = "hospitalCases,"
    spec = "newCasesBySpecimenDate"

    first_row = area_code + area_name + area_type + date + deaths + hosp + spec

    json_row_list.append(first_row) # first row

    cons_str = "" # consumable string (temporarily holds stuff)
    final_str = ""

    # process rows similarly to the CSV file
    for i in range(len(uk_covid_data_json["data"])):

        counter = 0
        for c in uk_covid_data_json["data"][i]:
            if uk_covid_data_json["data"][i][c] is not None:
                if counter != len(uk_covid_data_json["data"][i])-1:
                    cons_str = cons_str + str(uk_covid_data_json["data"][i][c]) + ","
                else:
                    cons_str = cons_str + str(uk_covid_data_json["data"][i][c])
            else:
                if counter != len(uk_covid_data_json["data"][i])-1:
                    cons_str = cons_str + ","

            counter += 1

        json_row_list.append(cons_str) # append process
        cons_str = "" # refresh string

    for i in range(len(json_row_list)):
        final_str += json_row_list[i]

        if i < len(json_row_list):
            final_str += "\n"

    return final_str


def schedule_covid_updates(update_interval, update_name):
    """ Schedules data updates (obsolete) """
    pass # :)


# additional getter functions
def get_covid_data_local() -> list:
    """ Gets local Covid data """

    location, type = get_config_data("data", 1)
    local_stuff = process_covid_csv_data(parse_csv_data_api(covid_JSON_to_CSV(covid_API_request(location, type))))

    return local_stuff


def get_covid_data_national() -> list:
    """ Gets national Covid data """

    location, type = get_config_data("data", 2)
    national_stuff = process_covid_csv_data(parse_csv_data_api(covid_JSON_to_CSV(covid_API_request(location, type))))

    return national_stuff
