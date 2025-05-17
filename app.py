from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "EPO Scraper is running!"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    patent_number = data.get("patent_number")

    if not patent_number:
        return jsonify({"error": "No patent number provided"}), 400

    url = f"https://register.epo.org/application?number={patent_number}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    title_tag = soup.find("meta", {"name": "DC.title"})
    title = title_tag["content"] if title_tag else "Not found"

    return jsonify({
        "patent_number": patent_number,
        "epo_url": url,
        "title": title
    })
