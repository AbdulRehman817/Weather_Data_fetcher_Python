from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None

    if request.method == "POST":
        city = request.form["city"]

        # Get city location
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        ).json()

        if "results" in geo:
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            # Get weather
            data = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
            ).json()

            weather = data["current"]

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)