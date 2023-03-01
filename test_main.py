import unittest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from main import app
import json

class TestCrudRequest(unittest.TestCase):
    
    def setUp(self):
        #Connexion à la base de donnée mongodb nommé "test" avec une collection nommé "test"
        #C'est dans le setUp pour ne pas à avoir à le refaire dans chaque test, cela devient illisible
        
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['test']
        self.collection = self.db['test']
        self.test_client = TestClient(app)
        
        
        
    def test_post(self):
        retour = self.test_client.post("/add_test", params={"nom": "a", "age": "0", "loisir": "aaa"} )
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Test ajouté"]) 
        ajout = self.collection.find_one({"nom": "a"})
        self.assertIsNotNone(ajout)
        self.assertEqual(ajout["age"], "0")
        self.assertEqual(ajout["loisir"], "aaa")
        
    def test_get(self):
        # Test de la requête GET (en supposant que les données nom/age/loisir sont a/0/aaa )
        retour = self.test_client.get("/get_test")
        self.assertEqual(retour.status_code, 200)
        test_utilisateur = json.loads(retour.content)
        self.assertEqual(test_utilisateur[0]["nom"], "a")
        self.assertEqual(test_utilisateur[1]["age"], "0")
        self.assertEqual(test_utilisateur[2]["loisir"], "aaa")
        self.assertEqual(retour.json(), ["Récupération effectuée"]) 

    def test_put(self):

        retour = self.test_client.put('/update_test', params = {"oldname": "a", "nom": "b", "age": "2", "loisir": "bbb"})
        
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["MAJ effectuée"]) 
        updated_doc = self.collection.find_one({"nom": "b"})
        self.assertEqual(updated_doc["age"], "2")
        self.assertEqual(updated_doc["loisir"], "bbb")

if __name__ == '__main__':
    unittest.main()