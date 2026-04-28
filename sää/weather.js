const weatherCodeMap = {
    0: ["Selkeää", "iweatherpics/sun.png"],
    1: ["Melko selkeää", "weatherpics/sun.png"],
    2: ["Puolipilvistä", "weatherpics/cloudy.png"],
    3: ["Pilvistä", "weatherpics/overcast.png"],
    45: ["Sumuista", "weatherpics/fog.png"],
    48: ["Huurtunutta sumua", "weatherpics/fog.png"],
    51: ["Heikkoa tihkua", "weatherpics/rain.png"],
    53: ["Kohtalaista tihkua", "rweatherpics/ain.png"],
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


const cityInput = document.getElementById("city-input");
const searchButton = document.getElementById("search-button");
searchButton.addEventListener("click", getWeather);

async function getWeather() {
    const city = cityInput.value.trim();
    console.log(city);

    // Geocoding API
    const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${city}`
    const geoResponse = await fetch(geoUrl);
    const geoData = await geoResponse.json();
    console.log(geoData);

    const latitude = geoData.results[0].latitude;
    const longitude = geoData.results[0].longitude;
    const country = geoData.results[0].country;

    // Weather API
    const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`
    const weatherResponse = await fetch(weatherUrl);
    const weatherData = await weatherResponse.json();
    console.log(weatherData);

    const temperature = weatherData.current_weather.temperature;
    const windSpeedKmh = weatherData.current_weather.windspeed;
    const windSpeed = (windSpeedKmh / 3.6).toFixed(1);
    const weatherCode = weatherData.current_weather.weathercode;
    const [weatherCondition, weatherImage] = weatherCodeMap[weatherCode];

    if (country && city != country) {
        document.getElementById("city").innerText = `${city}, ${country}`;
    }
    else {
            document.getElementById("city").innerText = `${city}`;
    }

    
    document.getElementById("weatherpics").src = weatherImage;
    document.getElementById("temperature").innerText = temperature;
    document.getElementById("weather-condition").innerText = weatherCondition
    document.getElementById("wind-speed").innerText = windSpeed;

    
}