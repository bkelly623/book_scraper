import requests
from bs4 import BeautifulSoup
import csv

# Base URL for pagination
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Function to get book details from a page
def scrape_books(page_number):
    url = BASE_URL.format(page_number)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page {page_number}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    book_data = []
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').get_text(strip=True)
        availability = book.find('p', class_='instock availability').get_text(strip=True)

        # Extract star rating (convert text-based class to numerical rating)
        rating_class = book.find('p', class_='star-rating')['class'][1]
        ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating = ratings.get(rating_class, "N/A")

        book_data.append([title, price, availability, rating])

    return book_data

# Open a CSV file to store results
with open("books_scraped.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability", "Rating"])  # Header row

    for page in range(1, 4):  # Scraping first 3 pages
        print(f"Scraping page {page}...")
        books = scrape_books(page)
        writer.writerows(books)

print("Scraping complete. Data saved to books_scraped.csv.")

