from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import json  # Needed to read config.json
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

def send_telegram_alert(message):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        print("Error: Telegram credentials not found in .env file.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, json=payload)
        print("Telegram notification sent!")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def get_product_price(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    price = None
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        price_element = soup.find('span', class_='a-offscreen')
        if price_element:
            price = price_element.get_text()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        
    return price

def save_price_to_csv(price, url):
    with open('prices.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), url, price])

def clean_price(price_str):
    """Converts a string like '₹1,299.00' to a float 1299.0"""
    try:
        # Remove currency symbol, commas, and whitespace
        clean = price_str.replace('₹', '').replace(',', '').replace('$', '').strip()
        return float(clean)
    except:
        return 0.0

if __name__ == "__main__":
    # 1. Load settings from config.json
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        url = config['url']
        target_price = config['target_price']
    except FileNotFoundError:
        print("Error: config.json file not found.")
        exit()
    except json.JSONDecodeError:
        print("Error: Your config.json has a syntax error (check for extra commas).")
        exit()

    print(f"Checking price for: {url}")
    price_str = get_product_price(url)

    if price_str:
        print(f"Current Price on Site: {price_str}")
        save_price_to_csv(price_str, url)
        
        # 2. Compare Price Logic
        current_price_num = clean_price(price_str)
        
        if current_price_num <= target_price:
            print("Price is within target! Sending alert.")
            message = (
                f"🚨 Price Drop Alert!\n\n"
                f"Target: ₹{target_price}\n"
                f"Current: {price_str}\n"
                f"Link: {url}"
            )
            send_telegram_alert(message)
        else:
            print(f"Price is too high (Target: {target_price}). No alert sent.")
            
    else:
        print("Could not retrieve the price.")