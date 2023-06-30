from fastapi import FastAPI
import psycopg2
from psycopg2 import extras

app = FastAPI()

# Database connection details
db_params = {
    "host": "localhost",
    "database": "my_database",
    "user": "my_username",
    "password": "my_password",
}
@app.get("/reviews")
def get_reviews():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    # Fetch reviews from the database
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return reviews
@app.post("/reviews")
def create_review(review: dict):
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

    # Insert the new review into the database
    cursor.execute(
        "INSERT INTO reviews (title, content) VALUES (%s, %s)",
        (review["title"], review["content"]),
    )
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return {"message": "Review created successfully"}
