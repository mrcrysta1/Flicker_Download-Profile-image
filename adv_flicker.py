import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

username = "32271947@N06"
base_url = f"https://www.flickr.com/photos/{username}/"

all_images = set()

# Setup Selenium (Chrome headless)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

page = 1
while True:
    url = f"{base_url}page{page}"
    print(f"Fetching {url} ...")
    driver.get(url)
    time.sleep(2)

    # scroll until all photos load on this page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # parse this page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    imgs = soup.find_all("img")
    found_new = 0

    for img in imgs:
        link = img.get("src")
        if link and "staticflickr.com" in link:
            if link.startswith("//"):
                link = "https:" + link
            # force large (_b)
            link = link.rsplit("_", 1)[0] + "_b.jpg"
            if link not in all_images:
                all_images.add(link)
                found_new += 1

    print(f"Page {page}: found {found_new} new images, total so far {len(all_images)}")

    # agar is page me koi new image hi na mile → stop
    if found_new == 0:
        break

    page += 1

driver.quit()

print(f"\n✅ Total photos collected: {len(all_images)}")

# download folder
os.makedirs("flickr_downloads", exist_ok=True)

for i, img_url in enumerate(all_images):
    try:
        data = requests.get(img_url).content
        with open(f"flickr_downloads/photo_{i}.jpg", "wb") as f:
            f.write(data)
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Failed {img_url}: {e}")
