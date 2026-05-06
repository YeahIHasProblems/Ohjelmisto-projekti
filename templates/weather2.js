async function haeSaa(lat, lon) {
  const url =
    `https://api.open-meteo.com/v1/forecast` +
    `?latitude=${lat}` +
    `&longitude=${lon}` +
    `&current=temperature_2m,wind_speed_10m,weather_code` +
    `&wind_speed_unit=ms` +
    `&timezone=auto`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("Sään haku epäonnistui");

  const data = await res.json();
  return data.current;
}

function weatherText(code) {
  const map = {
    0: "Selkeää",
    1: "Pääosin selkeää",
    2: "Puolipilvistä",
    3: "Pilvistä",
    45: "Sumua",
    48: "Kuuraa / sumua",
    51: "Kevyttä tihkua",
    53: "Tihkua",
    55: "Voimakasta tihkua",
    61: "Kevyttä sadetta",
    63: "Sadetta",
    65: "Voimakasta sadetta",
    71: "Kevyttä lumisadetta",
    73: "Lumisadetta",
    75: "Voimakasta lumisadetta",
    80: "Sadekuuroja",
    81: "Sadekuuroja",
    82: "Voimakkaita sadekuuroja",
    95: "Ukkosta"
  };

  return map[code] ?? "Tuntematon sää";
}

function weatherImage(code) {
  if (code === 0) return "img/sunny.png";
  if ([1, 2].includes(code)) return "img/partly-cloudy.png";
  if (code === 3) return "img/cloudy.png";
  if ([45, 48].includes(code)) return "img/fog.png";
  if ([51, 53, 55, 61, 63, 65, 80, 81, 82].includes(code)) return "img/rain.png";
  if ([71, 73, 75].includes(code)) return "img/snow.png";
  if ([95, 96, 99].includes(code)) return "img/thunder.png";

  return "img/unknown.png";
}

async function paivitaAirportSaa(airport) {
  // airport tulee SQL:stä, esim:
  // { name: "Los Bálticos Airport", latitude: 60.3172, longitude: 24.9633 }

  document.querySelector("#airportName").textContent = airport.name;

  const current = await haeSaa(airport.latitude, airport.longitude);

  document.querySelector("#saa").textContent =
    `Sää: ${weatherText(current.weather_code)}`;

  document.querySelector("#tuuli").textContent =
    `Tuuli: ${current.wind_speed_10m} m/s`;

  document.querySelector("#lampotila").textContent =
    `Lämpötila: ${current.temperature_2m} °C`;

  document.querySelector("#weatherImg").src =
    weatherImage(current.weather_code);
}