# Taobao Order and Shipping Info Scraper
This Python script automates the process of scraping order details and shipping information from the Taobao order page. It is particularly useful for users purchasing a large number of items through Taobao and using third-party forwarders, where manually tracking shipping numbers can become a cumbersome task. By extracting relevant order information such as order IDs, item names, prices, shipping companies, tracking numbers, and shipping addresses, the script simplifies the compilation of tracking data.

### Features:
- Scrapes order details (Order ID, Item Name, Price) directly from the main Taobao order page.
- Navigates to individual shipping pages to gather shipping company, tracking number, and shipping address.
- Saves collected information in an easily accessible CSV format.
- Random time delays between page loads to avoid triggering captcha or blocking mechanisms.

### Future Improvements:
- Scraping multiple tracking numbers for a single order.
- Selecting specific orders to scrape instead of the current first 50 orders.

### Requirements:
- Selenium WebDriver
- Python 3.x
- Brave browser and corresponding driver

### Usage:
- Install necessary Python packages: selenium. (pip install -U selenium) [https://pypi.org/project/selenium/]
- Update the script with the correct paths for Brave browser and ChromeDriver.
- Run the script and manually log in to Taobao.
- The script will then collect order and shipping information and save it to output.csv in the same directory as the python script.
