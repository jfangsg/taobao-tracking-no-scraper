import sys
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import random

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument(r"user-data-dir={Input selenium profile directory}")
chrome_options.add_experimental_option("detach", True)
chrome_options.binary_location = r"{Input brave browser exe directory}"
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

def crawler_main_page(driver, output_dict):
    try:
        orders_section = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='tp-bought-root']")))
        print('Collecting order and price info from main page...')
        
        order_elements = orders_section.find_elements(By.XPATH, ".//td[contains(@class, 'bought-wrapper-mod__head-info-cell___')]")
        order_ids = []
        for order_elem in order_elements:
            try:
                order_id_elem = order_elem.find_element(By.XPATH, ".//span[contains(@data-reactid, 'order-') and contains(@data-reactid, '.1.2')]")
                order_id = order_id_elem.text
                print(f"Found Order ID: {order_id}")
                order_ids.append(order_id)
            except NoSuchElementException:
                print("Order ID not found")
                continue
            
            # Get item name
            try:
                item_name_elem = orders_section.find_element(By.XPATH, f".//span[contains(@data-reactid, '$order-{order_id}') and contains(@data-reactid, '.0.1:1:0.$0.$0.0.1.0.0.1')]")
                item_name = item_name_elem.text
                print(f"Item Name: {item_name}")
            except NoSuchElementException:
                item_name = "Item name not found"
                print(item_name)
            
            # Get item price
            try:
                price_elem = orders_section.find_element(By.XPATH, f".//span[contains(@data-reactid, '$order-{order_id}') and contains(@data-reactid, '.0.1:1:0.$0.$4.0.0.2.0.1')]")
                item_price = price_elem.text
                print(f"Item Price: {item_price}")
            except NoSuchElementException:
                item_price = "Price not found"
                print(item_price)
            
            # Save initial data to output dictionary
            output_dict[order_id] = [item_name, item_price, "Shipping company not found", "Tracking number not found", "Shipping address not found"]
        
        # Navigate to each shipment page to get additional info
        for order_id in order_ids:
            try:
                shipment_url = f"https://market.m.taobao.com/app/dinamic/pc-trade-logistics/home.html?orderId={order_id}"
                driver.get(shipment_url)
                delay = random.uniform(5, 15)
                print(f"Time delay before loading next page: {delay} seconds")
                time.sleep(delay)  # Random delay between 5 to 15 seconds between loading shipment pages
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'rax-text-v2')))
                
                # Get shipping company
                try:
                    shipping_company_elem = driver.find_element(By.XPATH, ".//span[@class='rax-text-v2 desc ellipsis']")
                    shipping_company = shipping_company_elem.text
                    print(f"Shipping Company: {shipping_company}")
                except NoSuchElementException:
                    shipping_company = "Shipping company not found"
                    print(shipping_company)
                
                # Get tracking number
                try:
                    tracking_number_elem = driver.find_element(By.XPATH, ".//span[@class='rax-text-v2 desc']")
                    tracking_number = tracking_number_elem.text
                    print(f"Tracking Number: {tracking_number}")
                except NoSuchElementException:
                    tracking_number = "Tracking number not found"
                    print(tracking_number)
                
                # Get shipping address
                try:
                    shipping_address_elem = driver.find_element(By.XPATH, ".//div[contains(@class, 'rax-view-v2 flexRow pc-address-wrapper')]//span[@class='rax-text-v2 title']")
                    shipping_address = shipping_address_elem.text
                    print(f"Shipping Address: {shipping_address}")
                except NoSuchElementException:
                    shipping_address = "Shipping address not found"
                    print(shipping_address)
                
                # Update output dictionary with shipping info
                output_dict[order_id][2] = shipping_company
                output_dict[order_id][3] = tracking_number
                output_dict[order_id][4] = shipping_address
                
            except Exception as e:
                print(f"Error navigating to shipment page for order ID {order_id}: {e}")
                continue
            
    except Exception as e:
        print(f"Error collecting data from main page: {e}")
        return

def save_to_csv(output_dict, filename='output.csv'):
    existing_orders = set()
    if os.path.exists(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if row:
                    existing_orders.add(row[0])
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if os.stat(filename).st_size == 0:
            writer.writerow(['Order ID', 'Item Name', 'Price', 'Shipping Company', 'Tracking Number', 'Shipping Address'])
        for key, value in output_dict.items():
            if key not in existing_orders:
                writer.writerow([key] + value)

def main():
    # Clear the terminal before starting
    os.system('cls' if os.name == 'nt' else 'clear')
    output_dict = {}

    PATH = r"{Input Chromedriver.exe directory}"

    driver = webdriver.Chrome(service=Service(PATH), options=chrome_options)
    driver.set_page_load_timeout(60)
    print("Navigating to Taobao login page...")
    print("Please log in to Taobao and press Enter once logged in...")
    input("Press Enter after manually navigating to the itemlist page...")

    try:
        WebDriverWait(driver, 60).until(lambda d: "itemlist" in d.current_url or "已买到的宝贝" in d.title)
        print("Successfully navigated to the order page.")
    except TimeoutException as e:
        print(f"Timeout waiting for the order page: {e}")
    
    crawler_main_page(driver, output_dict)
    save_to_csv(output_dict)
    print('Data has been saved to output.csv')

    input("Press Enter to exit...")

if __name__ =="__main__":
    main()
