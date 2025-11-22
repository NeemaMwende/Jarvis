from langchain.tools import tool
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# Initialize geolocator and timezone finder
geolocator = Nominatim(user_agent="time_tool")
tf = TimezoneFinder()

@tool
def get_time(city: str) -> str:
    """Returns the current local time for any city using geopy + timezonefinder + pytz."""
    try:
        # Get location coordinates (latitude, longitude)
        location = geolocator.geocode(city)
        if not location:
            return f"Sorry, I couldn't find the city '{city}'."

        lat, lon = location.latitude, location.longitude

        # Find timezone from coordinates
        timezone_str = tf.timezone_at(lat=lat, lng=lon)
        if not timezone_str:
            return f"Sorry, couldn't determine timezone for '{city}'."

        # Get current time in that timezone
        timezone = pytz.timezone(timezone_str)
        current_time = datetime.now(timezone).strftime("%I:%M %p")

        return f"The current time in {city.title()} ({timezone_str}) is {current_time}."

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__": 
    print(get_time("London"))
