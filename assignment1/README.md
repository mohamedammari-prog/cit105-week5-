# CIT 105 Module 5 — Assignment 1: Public API Consumption

## API and endpoint
This project uses the Open-Meteo Geocoding API (`https://geocoding-api.open-meteo.com/v1/search`) to look up a city, then the Open-Meteo Forecast API (`https://api.open-meteo.com/v1/forecast`) to retrieve current weather. No API key is required.

## Fields extracted
City, country, temperature, apparent temperature ("feels like"), relative humidity, and wind speed. The formatter displays unavailable fields safely.

## Setup and run
Requires Python 3.9+ and `requests`.
```bash
python -m pip install requests pytest
python fetch_data.py
python -m pytest -q
```

## Failure Modes — fill with actual captured output
Do not submit guessed output as captured evidence. Run each case and paste the exact terminal output here.

### Bad path (404)
Temporarily call `fetch_data("Miami", url="https://api.open-meteo.com/v1/not-a-real-path")` from a small local test or temporarily change `WEATHER_URL` to that invalid path, then run the script. Paste the exact output:
```text
[PASTE ACTUAL OUTPUT HERE]
```

### Timeout
Temporarily call `fetch_data("Miami", timeout=0.000001)` and print the returned error. Paste the exact output:
```text
[PASTE ACTUAL OUTPUT HERE]
```

### No network
Disable Wi-Fi/mobile data on the computer, run the script, and paste the exact output:
```text
[PASTE ACTUAL OUTPUT HERE]
```

## AI assistance disclosure
ChatGPT assisted with an initial code draft and test ideas. I reviewed and must be able to explain the final code. I will verify actual behavior before submission.
