from flask import Flask, render_template, request
import requests
import random
import os

app = Flask(__name__)

API_KEY = "RfoIDRrl298fnzaW4jeUHNHMdlPN5murbDO7NNTUNkKBI9EfK1GhDFTf"
HEADERS = {"Authorization": API_KEY}
CATEGORIES = {
    "1": "landscape",
    "2": "sunset",
    "3": "flowers",
    "4": "portrait",
    "5": "abstract",
    "6": "wildlife",
    "7": "city",
    "8": "fruit",
    "9": "fashion"
}

def fetch_pexels_image(query):
    per_page = 10
    page = random.randint(1, 10)
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={per_page}&page={page}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    photos = data.get('photos', [])
    
    if photos:
        selected = random.choice(photos)
        return selected['src']['large'], selected.get('photographer', '')
    else:
        return None, None

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    photographer = None
    selected_category = None

    if request.method == "POST":
        choice = request.form.get("category")
        if choice == "10":
            selected_category = random.choice(list(CATEGORIES.values()))
        else:
            selected_category = CATEGORIES.get(choice)
        if selected_category:
            image_url, photographer = fetch_pexels_image(selected_category)

    return render_template("index.html", categories=CATEGORIES, image_url=image_url,
                           photographer=photographer, selected_category=selected_category)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
