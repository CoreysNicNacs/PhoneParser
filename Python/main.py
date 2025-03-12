from geolocation import parse_phone_number, get_geolocation_with_opencage
import phonenumbers
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    phone_number = "+14013360609"
    try:
        parsed_number = parse_phone_number(phone_number)
        location_string = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        latitude, longitude = get_geolocation_with_opencage(location_string)
        logging.info(f"Latitude: {latitude}, Longitude: {longitude}")
    except Exception as e:
        logging.error(f"Error: {e}")