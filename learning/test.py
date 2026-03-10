from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

try:
    # This line triggers the fresh download
    print("Downloading/Verifying driver...")
    driver_path = ChromeDriverManager().install()
    
    # Initialize the driver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    # Test a simple load
    driver.get("https://www.google.com")
    print(f"Success! Browser Title: {driver.title}")
    
    time.sleep(2)
    driver.quit()

except Exception as e:
    print(f"Still hitting a snag: {e}")