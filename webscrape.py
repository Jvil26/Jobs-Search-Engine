from bs4 import BeautifulSoup
import requests
import re

BASE_URL = 'https://www.linkedin.com/jobs/'
CARD_CLASS = "base-card"
ROLE_CLASS = "base-search-card__title"
INFO_LINK_CLASS = "base-card__full-link"
LOCATION_CLASS = "job-search-card__location"
COMPANY_CLASS = "hidden-nested-link"
LISTDATE_CLASS = "job-search-card__listdate"

def scrape_jobs(job_category):
    info = {}
    result = requests.get(BASE_URL + job_category + '-jobs/')
    doc = BeautifulSoup(result.text, 'html.parser')
    if not doc.main:
        raise Exception("Error getting jobs")
    job_cards = doc.main.find_all(class_=CARD_CLASS)
    for i in range(len(job_cards)):
        print(job_cards[i])
        internship = {
            "role": job_cards[i].find(class_=ROLE_CLASS).text.strip(), 
            "link": job_cards[i].find(class_=INFO_LINK_CLASS)["href"],
            "location": job_cards[i].find(class_=LOCATION_CLASS).text.strip(),
            "list_date": job_cards[i].find(class_=re.compile(f"^{LISTDATE_CLASS}")).text.strip()
        }
        company = job_cards[i].find(class_=COMPANY_CLASS).text.strip()
        info[company] = internship
    print(info)
    return info
    

if __name__ == "__main__":
    scrape_jobs("computer-science-intern")