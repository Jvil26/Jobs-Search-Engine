from bs4 import BeautifulSoup
import requests

def scrape_url(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.content, "html.parser")