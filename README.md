# h1 The Covid Dashboard README


INTRODUCTION
____________

This project implements a simple Covid dashboard, which obtains Covid-related data from the United Kingdom, finds news articles, allows for scheduling of updates using event-driven architecture, all while allowing for customization through the source code or the configuration file.

This project was written and published by Ruslan Prigarin on Dec. 17th, 2021.



PREREQUISITES
_____________

First and foremost, you want to make sure you have Python installed to run this project.

Second, you will need an API key for the "newsapi" module. You can get it at https://newsapi.org, but it will require you to make an account. After that, you may place the key in the "api_key.txt" file.
	* Note: the program will function without the API key, but the news functionality will simply yield blank results.



INSTALLATION
____________

Launch setup.py



GETTING STARTED
_______________

Once you have everything setup, you can launch the program from the console as follows:

	>> python main.py

You should see something like this after a successful lauch:

	Welcome to the Covid-19 Dashboard!
	Access the dashboard by reaching the localhost URL (127.0.0.1) in your browser
	
	* Serving Flask app 'main' (lazy loading)
	* Environment: production
	WARNING: This is a development server. Do not use it in a production deployment.
	Use a production WSGI server instead.
	* Debug mode: off

Accessing 127.0.0.1 through HTTP at port 5000, where the main functionality of your program is going to be.

Most if not all of the activities will be saved in logs/covid_dashboard.log

For modification of the basic program functionality, such as local Covid data or news article terms, you may visit "config.json" which, while not looking at all like a .json file, has parameters that you may change within the quotes. The default values of the "config.json" file are as follows:

	DATA_LOCAL_AREA = "Exeter"
	DATA_LOCAL_TYPE = "ltla"
	DATA_NATION_AREA = "England"
	DATA_NATION_AREA = "nation"

	NEWS_TERMS = "Covid COVID-19 coronavirus"
	NEWS_CATEGORY = "health"
	NEWS_LANGUAGE = "en"

	UPDATE_REPEAT_INTERVAL = "86400"



TESTING
_______

Currently the testing is barebones, only covering data and news handling functions. The tests are currently not built into the program to run automatically along with it, so if you want to launch the tests you may have to launch them manually (python or pytest work in this case):
	
	>> python test_covid_data_handler.py
	>> python test_news_data_handling.py



DEVELOPER DOCUMENTATION
_______________________

For those interested in the actual code, the source code is available with this project. To access docstrings for the functions, you may try the following:

	>> import module_name
	>> help(module_name)



DETAILS
_______

Maybe I'll work on this thing again once day, who knows.

Ruslan Prigarin
rp641@exeter.ac.uk
17/12/2021