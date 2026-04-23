import schedule
import time
import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def send_newsletters():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    for user in users:
        news = requests.post("http://localhost:5000/fetch-news", json={"interests": user['interests']}).json()
        content = "\n".join([n['title'] for n in news[:5]])

        requests.post("http://localhost:5000/send-email", json={
            "email": user['email'],
            "content": content
        })

schedule.every().day.at("09:00").do(send_newsletters)

while True:
    schedule.run_pending()
    time.sleep(60)