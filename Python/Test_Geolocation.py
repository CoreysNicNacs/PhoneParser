import unittest
from geolocation import parse_phone_number, get_geolocation_with_opencage

class TestGeolocation(unittest.TestCase):
    
    def test_parse_phone_number(self):
        phone_number = "+14019193267"
        parsed_number = parse_phone_number(phone_number)
        self.assertTrue(parsed_number)

    def test_get_geolocation_with_opencage(self):
        location_string = "+1 401-919-3267"
        # Mock the request to OpenCage API if needed
        latitude, longitude = get_geolocation_with_opencage(location_string)
        self.assertIsNotNone(latitude)
        self.assertIsNotNone(longitude)

if __name__ == '__main__':
    unittest.main()