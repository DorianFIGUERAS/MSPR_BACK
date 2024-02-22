import requests
import unittest

class IntegrationTestFlaskApp(unittest.TestCase):
    BASE_URL = "http://wildlens.ddns.net:5000"

    def test_receive_uid_integration(self):
        response = requests.post(f"{self.BASE_URL}/userid", json={'uid': '12345'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('UID reçu avec succès', data['message '])
        self.assertEqual('12345', data['uid '])

    def test_upload_photo_integration(self):
        files = {'photo': open('C:/Users/Dorian FIGUERAS/Desktop/docker_flask/Dog-Tracks-5.jpg', 'rb')}
        response = requests.post(f"{self.BASE_URL}/upload_photo", files=files)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('Informations ', data)

if __name__ == '__main__':
    unittest.main(verbosity=2)



