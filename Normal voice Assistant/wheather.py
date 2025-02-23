import requests
from ss import key2  # Ensure ss.py contains: key2 = "YOUR_API_KEY"


def get_weather(city):
    """Fetches and returns the weather information for a given city."""
    api_address = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key2}&units=metric"

    try:
        response = requests.get(api_address)
        json_data = response.json()

        # Debugging: Print API response
        print(json_data)  # Helps in troubleshooting

        # Check if the API returned valid weather data
        if json_data.get("cod") != 200:
            return f"Error: {json_data.get('message', 'Could not fetch weather data')}"

        temperature = round(json_data["main"]["temp"], 1)
        description = json_data["weather"][0]["description"]

        return f"The current temperature in {city} is {temperature}°C with {description}."

    except Exception as e:
        return f"Error fetching weather: {e}"
