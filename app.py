from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

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

    # Try to extract title from meta first
    title_tag = soup.find("meta", {"name": "DC.title"})
    title = title_tag["content"] if title_tag else None

    # Fallback: try to get title from main content table
    if not title:
        label_cell = soup.find("th", string="Title")
        if label_cell:
            title_td = label_cell.find_next_sibling("td")
            if title_td:
                title = title_td.get_text(strip=True)

    if not title:
        title = "Not found"

    return jsonify({
        "patent_number": patent_number,
        "epo_url": url,
        "title": title
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
