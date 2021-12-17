""" Covid dashboard web page module """

# Ruslan Prigarin
# 710002810
# 25/11/2021

# Miscellaneous
import logging
import time
import sched

# Web functionality
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

# Config loading
from config_loading import get_location
from config_loading import get_repeat_interval

# Main functions
from covid_data_handler import get_covid_data_local
from covid_data_handler import get_covid_data_national
from covid_news_handling import get_max_articles

# News and updates
from covid_news_handling import get_news

# Time conversion for updates
from time_conversion_to_seconds import schedule_time


# =================================================================

# Apply API search results (dictionary) to local and global variables
LOCAL_DATA = get_covid_data_local()
NATIONAL_DATA = get_covid_data_national()

# Initialise Flask and sched
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)

# Initialise other things
my_news = ([
            #{
            #    "title": "Article Title",
            #    "content": "Insert content here"
            #}

        ]) # end

my_updates = ([
            #{
            #    "title": "Update Title",
            #    "content": "Update contents I guess"
            #}

        ]) # end

my_update_events = ([
            #{
            #    "event_title": "",
            #    "event_status": "Alive" / "Kill" / "Dead"
            #    "event": (raw sched event data)
            #}

        ]) # end

# Other variables
NEWS_INDEX = 1
NEWS_REFRESH_RATE = 320
NEWS_MAX_COUNT = 3
NEWS_MAX_ARTICLES = get_max_articles() # news handling
NEWS_ARTICLE = 0

UPDATES_MAX_TITLE_LENGTH = 32
UPDATES_MAX_COUNT = 5
UPDATES_COUNT = 0

# Covid updates initialised to zeros (use for testing data updates)
#LOCAL_DATA = [0, 0, 0]
#NATIONAL_DATA = [0, 0, 0]

logging.basicConfig(filename='logs/covid_dashboard.log', filemode='w', level=logging.INFO, format='%(asctime)s, %(levelname)s - %(message)s')


# =================================================================

def __update_data(text_field, rep, data, news, update_field):
    """ Updates data as part of update scheduling """

    global LOCAL_DATA
    global NATIONAL_DATA

    global NEWS_INDEX
    global NEWS_MAX_COUNT
    global NEWS_MAX_ARTICLES
    global NEWS_ARTICLE

    # repeat scheduled event (if update_field is not None)
    if rep and update_field:
        s.enter(get_repeat_interval(), 1, __update_data, kwargs={
          'text_field' : text_field,
          'rep' : rep,
          'data' : data,
          'news' : news,
          'update_field' : update_field
        })  # repeat event after 24 hours

    # update data
    if data:
        LOCAL_DATA = get_covid_data_local()
        NATIONAL_DATA = get_covid_data_national()

    # add news
    if news:
        if NEWS_ARTICLE >= NEWS_MAX_ARTICLES:
            NEWS_ARTICLE = 0 # start over from beginning of available articles

        if NEWS_INDEX <= NEWS_MAX_COUNT: # if the number of news on right panel do not exceed limit
            news_title, news_content = get_news(NEWS_ARTICLE)
            s.enter(0, 1, add_news, argument=(news_title, news_content)) # add a news event
            NEWS_ARTICLE += 1 # iterate through available articles
            NEWS_INDEX += 1

    logging.info("The update \"" + text_field + "\" has been scheduled.")

def add_news(t, c):
    """ Adds news """

    my_news.append(
        {
            "title": t,
            "content": c

        }) # end news append

    logging.info("A news item has been added.")


def add_update(t, c):
    """ Adds updates. """

    my_updates.append(
        {
            "title": t,
            "content": c

        }) # end news append

    logging.info("A scheduled update entry has been added.")


def cleanse_dead_updates():
    """ Removes updates that are no longer in schedule queue but still stored in the container """

    update_death_count = 0 # used for logging

    if my_update_events: # if not empty
        for i in range(len(my_update_events)):
            if my_update_events[i]["event_status"] == "Kill": # if the event is tagged as dead
                s.cancel(my_update_events[i]["event"]) # kill event
                my_update_events[i]["event_status"] = "Dead"

        # remove dead events
        counter = 0
        while counter < len(my_update_events):
            if my_update_events[counter]["event_status"] == "Dead":
                my_update_events.pop(counter)
                update_death_count += 1
                counter = 0
            else:
                counter += 1

    logging.info("Removed " + str(update_death_count) + " dead updates.")


def process_update_request(text_field):
    """ Schedules updates """

    global NEWS_REFRESH_RATE
    global NEWS_MAX_COUNT
    global NEWS_INDEX

    global UPDATES_MAX_COUNT
    global UPDATES_COUNT # check if above max count

    update_dupe_name = 0 # check for duplicate names with the scheduled updates
    update_processed_title = text_field
    sorted_dupes = []

    update_field = request.args.get('update')

    # optional user input
    web_repeat = request.args.get('repeat')
    web_covid_data = request.args.get('covid-data')
    web_news = request.args.get('news')

    # get the dupe stuff
    for i in range(len(my_updates)):
        sorted_dupes.append(my_updates[i]['title'])

    # sort the dupe stuff
    sorted_dupes.sort()

    if UPDATES_COUNT < UPDATES_MAX_COUNT:
        if update_field: # if time was added as part of update scheduling
            # check for dupes
            for i in range(len(my_updates)):
                if text_field == my_updates[i]['title']:
                    update_dupe_name += 1

            if update_dupe_name > 0:
                update_processed_title = text_field + ' (' + str(update_dupe_name) + ')'

            # check for dupes of dupes
            for i in range(len(my_updates)):
                if update_processed_title == sorted_dupes[i]:
                    update_dupe_name += 1
                    update_processed_title = text_field + ' (' + str(update_dupe_name) + ')'

            # if the update has been applied, schedule it for data
            my_update_events.append(
            {
              "event_title" : update_processed_title,
              "event_status" : "Alive",
              "event" : s.enter(schedule_time(update_field, time.strftime('%X')), 1, __update_data, # get current and desired times for schedule_time
              kwargs={
                'text_field' : update_processed_title,
                'rep' : web_repeat,
                'data' : web_covid_data,
                'news' : web_news,
                'update_field' : update_field

              }) # end s_enter
            }) # end append

            # add the update to the left
            add_update(update_processed_title, update_field)

            UPDATES_COUNT += 1

    if not update_field:
        # if the update has been applied, schedule it for data (no timer)
        my_update_events.append(
        {
          "event_title" : text_field,
          "event_status" : "Alive",
          "event" : s.enter(0, 1, __update_data,
          kwargs={
            'text_field' : text_field,
            'rep' : None,
            'data' : web_covid_data,
            'news' : web_news,
            'update_field' : None

          }) # end s_enter
        }) # end append


def process_news_closing(web_notif):
    """ Processes closure of news by user """

    global NEWS_INDEX

    if my_news:
        for i in range(len(my_news)):
            if my_news[i]['title'] == web_notif:
                my_news.pop(i) # pop news item from news container
                if NEWS_INDEX > 0:
                    NEWS_INDEX -= 1 # remove news item from right panel
                break

    logging.info("A news item has been closed.")


def remove_update(update_item):
    """ Removes the update item from left panel """

    global UPDATES_COUNT

    for i in range(len(my_updates)): # find and kill web page record of the update
        if my_updates[i]['title'] == update_item:
            my_updates.pop(i)
            if UPDATES_COUNT > 0:
                UPDATES_COUNT -= 1
            break

    logging.info("The update \"" + update_item + "\" has been cancelled.")


def process_update_closing(update_item, is_past = False):
    """ Processes closure of updates by user. """

    if my_updates: # if left panel not empty
        if is_past: # if the event executed as scheduled
            remove_update(update_item) # remove from left panel
        else:
            remove_update(update_item)
            for i in range(len(my_update_events)): # find and mark scheduled update as Kill
                if my_update_events[i]["event_title"] == update_item:
                    my_update_events[i]["event_status"] = "Kill"


def check_past_updates():
    """ Checks if any update events marked as Alive are actually in still in queue """

    not_in_queue_counter = 0

    for i in range(len(my_update_events)):
        if my_update_events[i]["event_status"] == "Alive":
            if my_update_events[i]["event"] not in s.queue: # if event is no longer in queue
                not_in_queue_counter += 1
                my_update_events[i]["event_status"] = "Dead"
                process_update_closing(my_update_events[i]["event_title"], True)

    logging.info("Found " + str(not_in_queue_counter) + " updates that are no longer in queue.")


@app.route("/")
def index():
    """ Redirects to main page """

    return redirect("/index")

@app.route("/index")
def main():
    """ Web execution; main page """

    # remove dead updates if present
    if my_update_events:
        cleanse_dead_updates()

    # user input
    text_field = request.args.get('two')
    if text_field:
        process_update_request(text_field[0:UPDATES_MAX_TITLE_LENGTH]) 

    web_notif = request.args.get('notif')
    if web_notif:
        process_news_closing(web_notif)

    update_item = request.args.get('update_item')
    if update_item:
        process_update_closing(update_item)

    # run scheduled updates
    s.run(blocking=False)

    # check if any updates are no longer alive
    check_past_updates()

    return render_template(
        'index.html',
        title ='The Covid-19 Dashboard',
        image ='bobbing.gif', # (ft. Kohaku, Tsukihime)
        location = get_location("local"),
        nation_location = get_location("national"),
        local_7day_infections = LOCAL_DATA[0],
        national_7day_infections = NATIONAL_DATA[0],
        hospital_cases = NATIONAL_DATA[1],
        deaths_total = NATIONAL_DATA[2],
        news_articles = my_news,
        updates = my_updates

        ) # end render_template

if __name__ == '__main__':
    print("Welcome to the Covid-19 Dashboard!")
    print("Access the dashboard by reaching the localhost URL at port 5000 (http://127.0.0.1:5000) in your browser\n")
    app.run()
