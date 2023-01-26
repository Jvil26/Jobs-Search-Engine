CREATE_SEARCHES_TABLE = (
    "CREATE TABLE IF NOT EXISTS searches (id SERIAL PRIMARY KEY, date TIMESTAMP, name TEXT, search_count INTEGER"
)

INSERT_SEARCH = "INSERT INTO searches (name, search_count, date) VALUES (%s, %d, %s)"

MOST_SEARCHED = "SELECT * from searches order by search_count desc limit 10"

MOST_RECENT_SEARCHES = "SELECT * from searches order by date desc limit 10"

FIND_SEARCH = "SELECT * from searches WHERE searches.name = (%s)"

UPDATE_SEARCH = "UPDATE searches SET date = %s, search_count = %d WHERE name = %s"