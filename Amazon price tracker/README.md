# 📈 Amazon Price Tracker with Telegram Alerts

A robust Python script that automatically tracks product prices on Amazon.in. It uses **Selenium** to handle dynamic page loading and sends instant **Telegram notifications** when the price drops below your target.

## 🚀 Features

* **Selenium Automation:** Uses a real browser instance (Headless Chrome) to bypass basic static scraping protections.
* **Smart Alerts:** Only sends Telegram messages when the price hits your specific **Target Price**.
* **Secure:** API keys are stored safely in environment variables, not in the code.
* **Data Logging:** Automatically appends price history to a `prices.csv` file.
* **Background Execution:** Configured to run silently in the background.

## 🛠️ Tech Stack

* **Python 3.x**
* **Selenium** (Browser Automation)
* **BeautifulSoup4** (HTML Parsing)
* **Pandas** (Data Handling)
* **Python-Dotenv** (Security)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/amazon-price-tracker.git](https://github.com/yourusername/amazon-price-tracker.git)
    cd amazon-price-tracker
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install selenium beautifulsoup4 pandas matplotlib python-dotenv webdriver-manager requests
    ```

## ⚙️ Configuration (Important)

This project uses two configuration files. You must set them up before running the script.

### 1. Setup Secrets (.env)
Create a new file in the project folder named `.env` (no extension). Add your Telegram Bot details here:

```ini
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
(Note: You can get these from @BotFather and @userinfobot on Telegram)

2. Setup Settings (config.json)
Open the config.json file to set the product you want to track and your desired buy price:

JSON

{
  "url": "[https://www.amazon.in/dp/YOUR_PRODUCT_ID](https://www.amazon.in/dp/YOUR_PRODUCT_ID)",
  "target_price": 850
}
🏃 Usage
Run the script manually:

Bash

python price_tracker.py
If the current price is lower than your target_price, you will receive a Telegram message immediately.

⏰ Automating on Windows (Task Scheduler)
To have this script run automatically every day without you touching it:

Open Windows Task Scheduler.

Click Create Basic Task -> Name it "Amazon Price Tracker".

Trigger: Daily (e.g., 10:00 AM).

Action: Start a program.

Program/script: Path to python.exe (Type where python in cmd to find it).

Add arguments: Path to price_tracker.py.

Start in: [CRITICAL] The full path to your project folder (so it can find .env).

Make it Silent: Right-click the task > Properties > Select "Run whether user is logged on or not".

⚠️ Disclaimer
This project is for educational purposes only. Web scraping may violate Amazon's Terms of Service. Use this tool responsibly.


### One final tip for your repo
Since you are instructing people to look at `config.json`, make sure the `config.json` you upload to GitHub has dummy data, like this:

```json
{
  "url": "https://amzn.in/example-link",
  "target_price": 1000
}