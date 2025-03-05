if __name__ == "__main__":
    phone_number = "+14013360609"
    parsed_number = parse_phone_number(phone_number)
    latitude, longitude = get_geolocation_with_opencage(parsed_number)

    print(f"Latitude: {latitude}, Longitude: {longitude}")
