from flask import Flask, request, jsonify
import openai
import yagmail
import os
from dotenv import load_dotenv

load_dotenv()
p
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# DB connection
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Fetch news
@app.route('/fetch-news', methods=['POST'])
def fetch_news():
    interests = request.json.get('interests')
    url = f"https://newsapi.org/v2/everything?q={interests}&apiKey={NEWS_API_KEY}"
    res = requests.get(url).json()
    return jsonify(res.get('articles', []))

# Summarize with OpenAI
@app.route('/summarize', methods=['POST'])
def summarize():
    content = request.json.get('content')
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize this: {content}"}]
    )
    return jsonify({"summary": response['choices'][0]['message']['content']})

# Scrape article
@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    paragraphs = [p.text for p in soup.find_all('p')]
    return jsonify({'content': ' '.join(paragraphs[:10])})

# Save user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (email, interests, frequency) VALUES (%s,%s,%s)",
                   (data['email'], data['interests'], data['frequency']))
    db.commit()
    return jsonify({"message": "User registered"})

# Send email
@app.route('/send-email', methods=['POST'])
def send_email():
    email = request.json.get('email')
    content = request.json.get('content')

    yag = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
    yag.send(to=email, subject="Your Newsletter", contents=content)

    return jsonify({"message": "Email sent"})

if __name__ == '__main__':
    app.run(debug=True)