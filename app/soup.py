import os
import re
import pathlib
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

env_path = pathlib.Path(__file__).parents[1] / ".env"
load_dotenv(env_path)

SCRAPER_BASE_URL = os.getenv("SCRAPER_BASE_URL", "http://books.toscrape.com")

def scrape_books_toscrape(max_pages=2):
    books = []

    for page in range(1, max_pages + 1):
        url = f"{SCRAPER_BASE_URL}/catalogue/page-{page}.html"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            for book in soup.find_all("article", class_="product_pod"):
                title = book.h3.a["title"]
                
                raw_price = book.find("p", class_="price_color").text
                price_match = re.search(r'[\d\.,]+', raw_price)
                price_value = price_match.group(0) if price_match else "0.00"
                
                stock = book.find("p", class_="instock availability").text.strip()
                
                rating_class = book.find("p", class_="star-rating")["class"]
                rating = rating_class[1]

                books.append({
                    "title": title,
                    "price": float(price_value),
                    "stock": stock,
                    "rating": rating
                })

        except requests.exceptions.RequestException:
            continue

    return books
