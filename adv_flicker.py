import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

username = "32271947@N06"
url = f"https://www.flickr.com/photos/{username}/"

# Setup Selenium (Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get(url)

# scroll down until all photos load
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # wait for lazy-load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# parse final loaded page
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

all_images = set()
for img in soup.find_all("img"):
    link = img.get("src")
    if link and "staticflickr.com" in link:
        if link.startswith("//"):
            link = "https:" + link
        link = link.rsplit("_", 1)[0] + "_b.jpg"
        all_images.add(link)

print(f"Total found: {len(all_images)}")

# download
os.makedirs("flickr_downloads", exist_ok=True)
for i, img_url in enumerate(all_images):
    try:
        data = requests.get(img_url).content
        with open(f"flickr_downloads/photo_{i}.jpg", "wb") as f:
            f.write(data)
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Failed {img_url}: {e}")
