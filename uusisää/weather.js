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



//function showWeather(airport) {
//  document.querySelector('#airport-name').innerHTML = `Weather at ${airport.name}`;
 // document.querySelector('#airport-temp').innerHTML = `${airport.weather.temp}°C`;
// document.querySelector('#weather-icon').src = airport.weather.icon;
// document.querySelector('#airport-conditions').innerHTML = airport.weather.description;
 // document.querySelector('#airport-wind').innerHTML = `${airport.weather.wind.speed}m/s`;
//}

async function loadWeather() {
    const response = await fetch("/api/weather");

    if (!response.ok) {
        console.log("Weather not available");
        return;
    }

    const weather = await response.json();

    const weatherInfo = weatherCodeMap[weather.weathercode] || [
        "Tuntematon sää",
        "weatherpics/unknown.png"
    ];

    document.querySelector("#tempurate").textContent =
        `${weather.temperature}°C`;

    document.querySelector("#airport-wind").textContent =
        `${weather.windspeed} m/s`;

    document.querySelector("#airport-conditions").textContent =
        weatherInfo[0];

    document.querySelector("#weather-icon").src =
        weatherInfo[1];
}

loadWeather();
