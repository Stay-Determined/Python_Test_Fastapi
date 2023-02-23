from mongoengine import Document, StringField, IntField
from typing import Union

#Utilisation de mongoengine
#class Test(Document): 
#    nom = StringField(max_length=50)
#    age = IntField()
#    loisir = StringField(max_length=50)
    
class User(Document):
    nom: str
    age: Union[int, None] = None
    loisir: Union[str, None] = None



