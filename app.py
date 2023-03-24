import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from datetime import datetime, timezone
from sql_queries import *
from webscrape import *

load_dotenv()

app = Flask(__name__)
url = os.getenv("DB_URL")
connection = psycopg2.connect(url)

@app.post("/api/search")
def create_search():
    data = request.get_json()
    job_category = data["job_category"]
    try:
        info = scrape_jobs(job_category)
        curr_date = datetime.now(timezone.utc)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_SEARCHES_TABLE)
                cursor.execute(FIND_SEARCH, (job_category,))
                search_with_name = cursor.fetchone()
                if search_with_name:
                    search_count = search_with_name[3]
                    cursor.execute(UPDATE_SEARCH, (curr_date, search_count + 1, job_category))
                else:
                    cursor.execute(INSERT_SEARCH, (job_category, 0, curr_date))
                response = cursor.fetchone()
        return { "success": True, "search": response, "job_info": info }, 201
    except Exception as e:
        return { "error": str(e) }

@app.get("/")
def home():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)