"""Fetch current weather from Open-Meteo and display it clearly."""
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_data(city, timeout=5, url=WEATHER_URL):
    """Look up a city and fetch current weather; return (data, message)."""
    try:
        place_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=timeout,
        )
        if place_response.status_code == 404:
            return None, "City lookup returned 404: check the city name."
        if 500 <= place_response.status_code <= 599:
            return None, "The location service is temporarily unavailable (server error)."
        if place_response.status_code != 200:
            return None, f"City lookup failed with HTTP {place_response.status_code}."
        place_response.raise_for_status()
        places = place_response.json().get("results") or []
        if not places:
            return None, f"No location found for {city!r}. Try another city."

        place = places[0]
        params = {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m",
            "timezone": "auto",
        }
        response = requests.get(url, params=params, timeout=timeout)
        if response.status_code == 404:
            return None, "Weather endpoint returned 404: the requested path was not found."
        if 500 <= response.status_code <= 599:
            return None, "The weather service is temporarily unavailable (server error)."
        if response.status_code != 200:
            return None, f"Weather request failed with HTTP {response.status_code}."
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})
        return {
            "city": place.get("name", city),
            "country": place.get("country", "Unknown"),
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "temperature_unit": data.get("current_units", {}).get("temperature_2m", "°C"),
            "wind_unit": data.get("current_units", {}).get("wind_speed_10m", "km/h"),
        }, None
    except requests.exceptions.Timeout:
        return None, "The weather service took too long to respond. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the service. Check your internet connection and try again."
    except requests.exceptions.RequestException:
        return None, "A network error occurred while contacting the weather service."
    except (ValueError, KeyError, TypeError):
        return None, "The service returned data in an unexpected format. Please try again."


def format_weather(data):
    """Format a weather dictionary without requiring a network connection."""
    def display(value, suffix=""):
        return "Not available" if value is None else f"{value}{suffix}"

    lines = [
        f"Weather for {data.get('city', 'Unknown city')}, {data.get('country', 'Unknown country')}",
        "-" * 48,
        f"Temperature:      {display(data.get('temperature'), ' ' + data.get('temperature_unit', '°C'))}",
        f"Feels like:        {display(data.get('feels_like'), ' ' + data.get('temperature_unit', '°C'))}",
        f"Relative humidity: {display(data.get('humidity'), '%')}",
        f"Wind speed:        {display(data.get('wind_speed'), ' ' + data.get('wind_unit', 'km/h'))}",
    ]
    return "\n".join(lines)


def main():
    city = input("Enter a city: ").strip()
    if not city:
        print("Please enter a city name.")
        return
    data, error = fetch_data(city)
    if error:
        print(error)
        return
    print(format_weather(data))


if __name__ == "__main__":
    main()
