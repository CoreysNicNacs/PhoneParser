import os
from dotenv import load_dotenv
import phonenumbers
import requests

# Load environment variables from .env file
load_dotenv()

def parse_phone_number(phone_number, region="US"):
    parsed_number = phonenumbers.parse(phone_number, region)
    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError("Invalid phone number")
    return parsed_number

def get_geolocation_with_opencage(location_string):
    api_key = os.getenv("OPENCAGE_API_KEY")
    if not api_key:
        raise EnvironmentError("API key not found. Please set the OPENCAGE_API_KEY environment variable.")
    
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location_string}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']
            return location['lat'], location['lng']
        else:
            raise ValueError("Geocoding failed")
    else:
        response.raise_for_status()

if __name__ == "__main__":
    phone_number = "+14019193267"
    parsed_number = parse_phone_number(phone_number)
    location_string = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    latitude, longitude = get_geolocation_with_opencage(location_string)

    print(f"Latitude: {latitude}, Longitude: {longitude}")