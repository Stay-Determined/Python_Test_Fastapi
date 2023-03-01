import unittest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from main import app
import json
        
class TestCrudRequest(unittest.TestCase):
# Avant tout je tiens à préciser que l'exécution du fichier complet laisse dans la BDD 2 insertions, bien
# que tous les tests aient été validés (ce qui ne se passe pas si on effectue chaque test un à un)

# Commandes

#     Tout le fichier : 
#         python -m unittest test_main.py
    
#     Chaque test un à un (dans le bon ordre) :         
#         python -m unittest test_main.TestCrudRequest.test_get 
#         python -m unittest test_main.TestCrudRequest.test_post
#         python -m unittest test_main.TestCrudRequest.test_put
#         python -m unittest test_main.TestCrudRequest.test_delete 
    
    def setUp(self):
        #Connexion à la base de donnée mongodb nommé "test" avec une collection nommé "test"
        #C'est dans le setUp pour ne pas à avoir à le refaire dans chaque test, sinon le code devient illisible
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["test"]
        self.collection = self.db["test"]
        self.test_client = TestClient(app)
        
        
    def test_post(self):
        #Requête
        retour = self.test_client.post("/add_test", params={"nom": "a", "age": "0", "loisir": "aaa"} )
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Test ajouté"]) 
        
        #Récupération et vérification des données, si elles existent
        ajout = self.collection.find_one({"nom": "a"})
        self.assertIsNotNone(ajout)
        self.assertEqual(ajout["nom"], "a")
        self.assertEqual(ajout["age"], "0")
        self.assertEqual(ajout["loisir"], "aaa")
        
    def test_get(self):
        # J'utilise cette ligne car, pour une raison obscure, quand je test cette fonction seule 
        # après avoir testé le fonction test_post juste avant, cela fonctionne bien, mais 
        # quand il s"agit d"exécuter tout le programme, cela ne fonctionne plus
        self.collection.insert_one({"nom": "a", "age": "0", "loisir": "aaa"})
        
        #Requête (ici le retourn n'est pas fait de la même manière que les autres tests car
        #dans les fonctions du fichier "main.py", le retour effectué n'est pas non plus le même)
        retour = self.test_client.get("/get_test")
        self.assertEqual(retour.status_code, 200)
        test_utilisateur = json.loads(retour.content)
        self.assertEqual(test_utilisateur[0]["nom"], "a")


    def test_put(self):
        
        #Requête
        retour = self.test_client.put("/update_test", params = {"oldname": "a", "nom": "b", "age": "1", "loisir": "bbb"})
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["MAJ effectuée"]) 
        
        #Récupération et vérification des données, si elles existent ou non
        ajout = self.collection.find_one({"nom": "b"})
        self.assertIsNotNone(ajout)
        self.assertEqual(ajout["nom"], "b")
        self.assertEqual(ajout["age"], "1")
        self.assertEqual(ajout["loisir"], "bbb")

    def test_delete(self):
        
        #Requête
        retour = self.test_client.delete("/delete_test", params = {"nom": "b", "age": "1", "loisir": "bbb"})
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Suppression effectuée"])
        
        #Mettre en commentaire les trois prochaines lignes si ce test est fait sans avoir  
        #testé la requête GET avant
        retour = self.test_client.delete("/delete_test", params = {"nom": "a", "age": "0", "loisir": "aaa"})
        self.assertEqual(retour.status_code, 200)
        self.assertEqual(retour.json(), ["Suppression effectuée"])
        
        #Test pour voir si les deux insertions effectuées auparavant n'existent plus
        self.assertEqual(self.collection.count_documents({"name": "a", "age": "0", "loisir": "aaa"}), 0)
        self.assertEqual(self.collection.count_documents({"name": "b", "age": "1", "loisir": "bbb"}), 0)
        
if __name__ == "__main__":
    unittest.main()