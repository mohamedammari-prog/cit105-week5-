from fetch_data import format_weather


def test_format_weather_shows_all_fields():
    sample = {
        "city": "Miami", "country": "United States",
        "temperature": 28, "feels_like": 31, "humidity": 70,
        "wind_speed": 12, "temperature_unit": "°C", "wind_unit": "km/h",
    }
    output = format_weather(sample)
    assert "Miami, United States" in output
    assert "Temperature:" in output and "28 °C" in output
    assert "Feels like:" in output and "31 °C" in output
    assert "Relative humidity:" in output and "70%" in output
    assert "Wind speed:" in output and "12 km/h" in output


def test_format_weather_handles_missing_fields():
    output = format_weather({"city": "Tunis"})
    assert "Tunis" in output
    assert "Not available" in output
