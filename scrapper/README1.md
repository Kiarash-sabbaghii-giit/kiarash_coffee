## connection.py Module
This module is responsible for checking the connection to MongoDB Compass and verifying that the website is accessible.
It uses the requests library to send a GET request to the website URL and handles various connection errors such as network issues, timeouts, and HTTP errors.
This module ensures that the system is ready before starting the main scraping process.


## web_crawling_main.py Module
This is the main scraping module that performs the core data extraction from the Lamiz Coffee website.
It uses the requests library to fetch the HTML content of the menu page and BeautifulSoup to parse the HTML structure.
This module connects to MongoDB using PyMongo, identifies all 12 menu tabs, extracts product information including names, prices, descriptions, and image links, and stores the data in the appropriate database collections.


## help_code.py Module
This module was created specifically to handle the cakes and testbar sections that were not scraped successfully during the initial run of the main module.
It implements alternative methods to find and extract product information from these specific menu categories.
This module demonstrates a more targeted approach to scraping problematic sections by using different HTML class selectors and filtering techniques.


## correct_main_scrapper.py Module
This module corrects an important oversight in the original scraping logic by adding support for products that have multiple pricing options.
It now recognizes and handles products that come in three size choices (big, small, medium) as well as espresso drinks that offer both single and double shot options.
This module stores each price variant as a separate record in the database using a composite key of product name and price type to prevent duplicates.


## help_code_2.py Module
This module handles price formatting by adding comma separators to all prices stored in the database.
It updates existing records by converting prices from formats like 123670 to 123,670 without requiring a full re-scrape of the website.
This module provides a convenient way to standardize price display across all collections without rerunning the entire scraping process . 