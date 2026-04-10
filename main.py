from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        try:
            city = request.form.get("city")

            # Get city location
            geo = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1",
                timeout=5
            ).json()

            # Check city exists
            if geo.get("results"):
                lat = geo["results"][0]["latitude"]
                lon = geo["results"][0]["longitude"]

                # Get weather
                data = requests.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m",
                    timeout=5
                ).json()

                weather = data.get("current")
            else:
                error = "City not found"

        except Exception as e:
            error = "Something went wrong"

    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    app.run(debug=True)