from pymongo import MongoClient
import unittest
import model
import main
import requests

class mainTest(unittest.TestCase):
    def test_get_test(self):
        reponse = requests.get("http://localhost:8000/test")
        self.assertEqual(reponse.status_code, 200)
        self.assertIsInstance(reponse.json(),list)

    def test_delete_test(self):
        reponse = requests.get("http://localhost:8000/test")
        self.assertEqual(reponse.status_code, 200)
        
    def test_add_test(self):
        reponse = requests.get("http://localhost:8000/test")
        self.assertEqual(reponse.status_code, 200)
        
    
    def test_update_test(self):
        reponse = requests.get("http://localhost:8000/test")
        self.assertEqual(reponse.status_code, 200)
        
    