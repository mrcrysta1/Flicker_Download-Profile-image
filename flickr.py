import os
import requests
from bs4 import BeautifulSoup

username = ""   # Flickr user ID
base_url = f"https://www.flickr.com/photos/{username}/"

all_images = set()

page = 1
while True:
    url = f"{base_url}page{page}"
    print(f"Fetching {url} ...")
    resp = requests.get(url)
    if resp.status_code != 200:
        break

    soup = BeautifulSoup(resp.text, "html.parser")
    imgs = soup.find_all("img")

    count_before = len(all_images)

    for img in imgs:
        link = img.get("src")
        if link and "staticflickr.com" in link:
            if link.startswith("//"):
                link = "https:" + link
            # force large size (_b)
            link = link.rsplit("_", 1)[0] + "_b.jpg"
            all_images.add(link)

    # agar new images add hi nahi hui to stop
    if len(all_images) == count_before:
        break

    page += 1

print(f"Total found: {len(all_images)} photos")

# Download folder
os.makedirs("flickr_downloads", exist_ok=True)

for i, img_url in enumerate(all_images):
    try:
        data = requests.get(img_url).content
        with open(f"flickr_downloads/photo_{i}.jpg", "wb") as f:
            f.write(data)
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Failed {img_url}: {e}")

print("\n✅ Done! All available photos downloaded.")
