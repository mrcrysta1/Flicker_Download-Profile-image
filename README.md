# Flickr Downloader Tool

Flickr Downloader is a Python-based tool that allows you to **bulk download public photos** from any Flickr profile.  

This project includes two versions of the tool:

---

## 🚀 Versions

### 1. Basic Version (`flikr.py`)
- A simple script that downloads a **limited number of photos** from a Flickr profile.
- Works on the first visible page only.
- Good for beginners who want to understand the basics.

### 2. Pro Version (`adv_flickr.py`)
- An advanced scraper with **pagination support**.
- Automatically loads multiple pages to collect **all public photos** from a profile.
- Downloads the **large size (`_b.jpg`)** images for better quality.
- No photo limit (downloads all available public images).

---

## ⚙️ Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

---

## 📦 Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/mrcrysta1/Flicker_Download-Profile-image.git
cd Flicker_Download-Profile-image
pip install -r requirements.txt
