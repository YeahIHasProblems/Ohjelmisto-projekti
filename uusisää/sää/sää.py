from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/weather")
def get_weather():
    city = request.args.get("city")

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_res = requests.get(geo_url).json()

    if "results" not in geo_res:
        return jsonify({"error": "Kaupunkia ei löytynyt"}), 404

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]
    country = geo_res["results"][0]["country"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_res = requests.get(weather_url).json()

    return jsonify({
        "city": city,
        "country": country,
        "temperature": weather_res["current_weather"]["temperature"],
        "windspeed": weather_res["current_weather"]["windspeed"],
        "weathercode": weather_res["current_weather"]["weathercode"]
    })
if __name__ == "__main__":
    app.run(debug=True, port=5001)
