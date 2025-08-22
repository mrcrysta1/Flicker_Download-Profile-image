import os
import requests
from bs4 import BeautifulSoup

# Flickr profile (public photos)
profile_url = "https://www.flickr.com/photos/32271947@N06/"

resp = requests.get(profile_url)
soup = BeautifulSoup(resp.text, "html.parser")

images = set()
for img in soup.find_all("img"):
    link = img.get("src")
    if link and "staticflickr.com" in link:
        if link.startswith("//"):   # <-- Fix for missing schema
            link = "https:" + link
        images.add(link)

# Make folder
os.makedirs("flickr_downloads", exist_ok=True)

# Download all images
for i, img_url in enumerate(images):
    try:
        data = requests.get(img_url).content
        with open(f"flickr_downloads/photo_{i}.jpg", "wb") as f:
            f.write(data)
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Failed {img_url}: {e}")

print(f"\n✅ Done! {len(images)} images downloaded.")
