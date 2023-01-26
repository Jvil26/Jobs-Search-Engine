import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
import datetime
from sql_queries import *
from webscrape import *

load_dotenv()

app = Flask(__name__)
url = os.getenv("DB_URL")
connection = psycopg2.connect(url)

@app.post("/api/search")
def create_search():
    data = request.get_json()
    name = data["name"]
    try:
        info = scrape_url()
        if info["is_processed"]:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_SEARCHES_TABLE)
                    cursor.execute(FIND_SEARCH, (name,))
                    search_with_name = cursor.fetchone()
                    if search_with_name:
                        search_count = search_with_name[3]
                        cursor.execute(UPDATE_SEARCH, (datetime.date.today.strftime("%B %d, %Y"), search_count + 1, name))
                    else:
                        cursor.execute(INSERT_SEARCH, (name, 0, datetime.date.today.strftime("%B %d, %Y")))
        return { "success": True, "data": info }
    except:
        return { "error": True }

@app.get("/")
def home():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)