import json
import time
import requests
import schedule
import sqlite3
import openai
import pyupbit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI and Upbit clients
openai.api_key = os.getenv("OPENAI_API_KEY")
upbit = pyupbit.Upbit(os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY"))

def get_news_data(query="bitcoin"):
    print("Fetching news data...")
    serpapi_api_key = os.getenv("SERPAPI_API_KEY")
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_api_key,
        "tbm": "nws"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "news_results" in results:
        news_results = results["news_results"]
        news_data = []
        for news in news_results:
            news_item = {
                "title": news.get("title"),
                "link": news.get("link"),
                "source": news.get("source"),
                "date": news.get("date"),
                "snippet": news.get("snippet")
            }
            news_data.append(news_item)
        return news_data
    else:
        print("No news results found.")
        return []

def fetch_and_prepare_data():
    print("Fetching and preparing data...")
    # Placeholder for the actual implementation
    return "Some market data"

def fetch_last_decisions():
    print("Fetching last decisions...")
    # Placeholder for the actual implementation
    return "Previous decisions"

def fetch_fear_and_greed_index(limit=30):
    print("Fetching fear and greed index...")
    # Placeholder for the actual implementation
    return "Current fear and greed index"

def get_current_status():
    print("Fetching current status...")
    # Placeholder for the actual implementation
    return json.dumps({
        'btc_balance': 0.1,
        'krw_balance': 1000000,
        'avg_buy_price': 50000000
    })

def initialize_webdriver():
    print("Initializing WebDriver...")
    service = Service('/usr/local/bin/chromedriver')  # 경로 확인
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_current_base64_image():
    driver = None
    screenshot_path = "screenshot.png"
    try:
        # Set up Chrome options for headless mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        service = Service('/usr/local/bin/chromedriver')  # Specify the path to the ChromeDriver executable

        # Initialize the WebDriver with the specified options
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the desired webpage
        driver.get("https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-BTC")

        # Wait for the page to load completely
        wait = WebDriverWait(driver, 10)  # 10 seconds timeout

        # Wait for the first menu item to be clickable and click it
        first_menu_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='fullChartiq']/div/div/div[1]/div/div/cq-menu[1]")))
        first_menu_item.click()

        # Wait for the "1 Hour" option to be clickable and click it
        one_hour_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//cq-item[@stxtap=\"Layout.setPeriodicity(1,60,'minute')\"]")))
        one_hour_option.click()

        # Wait for the indicators menu item to be clickable and click it
        indicators_menu_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='fullChartiq']/div/div/div[1]/div/div/cq-menu[3]")))
        indicators_menu_item.click()

        # Wait for the indicators container to be present
        indicators_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "cq-scroll.ps-container")))

        # Scroll the container to make the "MACD" indicator visible
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 2.5", indicators_container)

        # Wait for the "MACD" indicator to be clickable and click it
        macd_indicator = wait.until(EC.element_to_be_clickable((By.XPATH, "//cq-item[translate[@original='MACD']]")))
        macd_indicator.click()

        # Take a screenshot to verify the actions
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        print(f"Error making current image: {e}")
        return ""
    finally:
        if driver:
            # Close the browser
            driver.quit()
        if os.path.exists(screenshot_path):
            with open(screenshot_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        return ""

def analyze_data_with_gpt4(news_data, data_json, last_decisions, fear_and_greed, current_status, current_base64_image):
    print("Analyzing data with GPT-4...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": news_data},
                {"role": "user", "content": data_json},
                {"role": "user", "content": last_decisions},
                {"role": "user", "content": fear_and_greed},
                {"role": "user", "content": current_status},
                {"role": "user", "content": [{"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{current_base64_image}"}}]}
            ]
        )
        advice = response['choices'][0]['message']['content']
        return advice
    except Exception as e:
        print(f"Error in GPT-4 API call: {e}")
        return None

def execute_buy(percentage):
    print(f"Executing buy for {percentage}% of available funds...")

def execute_sell(percentage):
    print(f"Executing sell for {percentage}% of holdings...")

def save_decision_to_db(decision, current_status):
    print("Saving decision to database...")
    # Placeholder for actual implementation

def make_decision_and_execute():
    print("Making decision and executing...")
    try:
        news_data = get_news_data()
        data_json = fetch_and_prepare_data()
        last_decisions = fetch_last_decisions()
        fear_and_greed = fetch_fear_and_greed_index(limit=30)
        current_status = get_current_status()
        current_base64_image = get_current_base64_image()
    except Exception as e:
        print(f"Error: {e}")
    else:
        max_retries = 5
        retry_delay_seconds = 5
        decision = None
        for attempt in range(max_retries):
            try:
                advice = analyze_data_with_gpt4(news_data, data_json, last_decisions, fear_and_greed, current_status, current_base64_image)
                if advice:
                    decision = json.loads(advice)
                    break
            except Exception as e:
                print(f"JSON parsing failed: {e}. Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)
                print(f"Attempt {attempt + 2} of {max_retries}")
        if not decision:
            print("Failed to make a decision after maximum retries.")
            return
        else:
            try:
                percentage = decision.get('percentage', 100)

                if decision.get('decision') == "buy":
                    execute_buy(percentage)
                elif decision.get('decision') == "sell":
                    execute_sell(percentage)
                
                save_decision_to_db(decision, current_status)
            except Exception as e:
                print(f"Failed to execute the decision or save to DB: {e}")

def initialize_db():
    print("Initializing database...")
    # Placeholder for actual implementation

if __name__ == "__main__":
    initialize_db()
    # testing
    schedule.every().minute.do(make_decision_and_execute)

    # Schedule the task to run at 00:01
    schedule.every().day.at("00:01").do(make_decision_and_execute)

    # Schedule the task to run at 08:01
    schedule.every().day.at("08:01").do(make_decision_and_execute)

    # Schedule the task to run at 16:01
    schedule.every().day.at("16:01").do(make_decision_and_execute)

    while True:
        schedule.run_pending()
        time.sleep(1)
