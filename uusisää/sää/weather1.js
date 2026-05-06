const weatherCodeMap = {
    0: ["Selkeää", "weatherpics/sun.png"],
    1: ["Melko selkeää", "weatherpics/sun.png"],
    2: ["Puolipilvistä", "weatherpics/cloudy.png"],
    3: ["Pilvistä", "weatherpics/overcast.png"],
    45: ["Sumuista", "weatherpics/fog.png"],
    48: ["Huurtunutta sumua", "weatherpics/fog.png"],
    51: ["Heikkoa tihkua", "weatherpics/rain.png"],
    53: ["Kohtalaista tihkua", "weatherpics/rain.png"],
    55: ["Voimakasta tihkua", "weatherpics/rain.png"],
    56: ["Light Freezing Drizzle?", "weatherpics/rain.png"],
    57: ["Dense Freezing Drizzle?", "weatherpics/rain.png"],
    61: ["Heikkoa sadetta", "weatherpics/rain.png"],
    63: ["Kohtalaista sadetta", "weatherpics/rain.png"],
    65: ["Voimakasta sadetta", "weatherpics/rain.png"],
    66: ["Light Freezing Rain", "weatherpics/rain.png"],
    67: ["Dense Freezing Rain", "weatherpics/rain.png"],
    71: ["Light Snow", "weatherpics/snow.png"],
    73: ["Moderate Snow", "weatherpics/snow.png"],
    75: ["Heavy Snow", "weatherpics/snow.png"],
    77: ["Snow Grains", "weatherpics/snow.png"],
    80: ["Slight Rain Showers", "weatherpics/rain.png"],
    81: ["Moderate Rain Showers", "weatherpics/rain.png"],
    82: ["Violent Rain Showers", "weatherpics/rain.png"],
    85: ["Slight Snow Showers", "weatherpics/snow.png"],
    86: ["Heavy Snow Showers", "weatherpics/snow.png"],
    95: ["Thunderstorm", "weatherpics/thunderstorm.png"],
    96: ["Thunderstorm With Slight Hail", "weatherpics/thunderstorm.png"],
    99: ["Thunderstorm With Heavy Hail", "weatherpics/thunderstorm.png"]
};

// ---------------- UI toggle ----------------

const div = document.getElementById("weather-container");
div.style.display = "none";

let display = 0;

function hideShow() {
    if (display === 0) {
        div.style.display = "block";
        display = 1;
    } else {
        div.style.display = "none";
        display = 0;
    }
}

// ---------------- Input + button ----------------

const cityInput = document.getElementById("city-input");
const searchButton = document.getElementById("search-button");

searchButton.addEventListener("click", getWeather);

// ---------------- MAIN WEATHER FUNCTION ----------------

async function getWeather() {
    const city = cityInput.value.trim();

    if (!city) return;

    try {
        const response = await fetch(`/weather?city=${encodeURIComponent(city)}`);
        const data = await response.json();

        if (data.error) {
            alert("City not found!");
            return;
        }

        const temperature = data.temperature;
        const windSpeed = data.windspeed;
        const weatherCode = data.weathercode;
        const country = data.country;

        const [weatherCondition, weatherImage] =
            weatherCodeMap[weatherCode] || ["Unknown", "weatherpics/default.png"];

        // City display
        document.getElementById("city").innerText =
            country && city !== country ? `${city}, ${country}` : city;

        // UI updates
        document.getElementById("weatherpics").src = weatherImage;
        document.getElementById("temperature").innerText = temperature;
        document.getElementById("weather-condition").innerText = weatherCondition;
        document.getElementById("wind-speed").innerText = windSpeed;

    } catch (err) {
        console.error("Weather fetch failed:", err);
        alert("Something went wrong while fetching weather.");
    }
}

// ---------------- OPTIONAL: auto-load from game ----------------

// If Flask injects this variable in template:
if (typeof pelinLokaatio !== "undefined" && pelinLokaatio) {
    window.addEventListener("load", () => {
        cityInput.value = pelinLokaatio;
        getWeather();
    });
}