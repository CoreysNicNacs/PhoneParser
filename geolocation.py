import phonenumbers
import requests

def parse_phone_number(phone_number):
    parsed_number = phonenumbers.parse(phone_number, "US")
    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError("Invalid phone number")
    return parsed_number

def get_geolocation_with_opencage(phone_number):
    api_key = "2d22fe6b4d0d463ca4712e5b380fba89"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={phone_number}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']
            return location['lat'], location['lng']
        else:
            raise ValueError("Geocoding failed")
    else:
        raise ConnectionError("API request failed")

if __name__ == "__main__":
    phone_number = "+14019193267"
    parsed_number = parse_phone_number(phone_number)
    latitude, longitude = get_geolocation_with_opencage(phone_number)

    print(f"Latitude: {latitude}, Longitude: {longitude}")
