import unittest
from app import app  # Assuming 'app' is your Flask application

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_upload_file(self):
        # Simulate uploading a valid file
        with open('test_file.txt', 'w') as f:
            f.write("Sensitive data: 123-45-6789")

        with open('test_file.txt', 'rb') as f:
            response = self.client.post('/upload', data={'file': f})
        
        # Check if the file was processed and sensitive data is extracted
        response_data = response.get_json()
        self.assertIn("message", response_data)
        self.assertIn("sensitive_data", response_data)
        self.assertGreater(len(response_data['sensitive_data']), 0)

    def test_upload_invalid_file_type(self):
        # Simulate uploading an invalid file type (non-text)
        with open('test_image.jpg', 'wb') as f:
            f.write(b'Invalid file content')

        with open('test_image.jpg', 'rb') as f:
            response = self.client.post('/upload', data={'file': f})

        # Expect a 400 status code for invalid file type
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertIn("error", response_data)
        self.assertEqual(response_data['error'], "Invalid file type. Only text and CSV files are allowed.")

    def test_upload_multiple_sensitive_data(self):
        # Simulate uploading a file with multiple sensitive data entries
        with open('test_multiple.txt', 'w') as f:
            f.write("Sensitive data: 123-45-6789 and 987-65-4321")

        with open('test_multiple.txt', 'rb') as f:
            response = self.client.post('/upload', data={'file': f})

        response_data = response.get_json()
        sensitive_data = response_data.get('sensitive_data', [])
        
        # Check that more than one sensitive data entry was extracted
        self.assertGreater(len(sensitive_data), 1)

if __name__ == '__main__':
    unittest.main()
