Le projet à été utilisé avec une base de donnée Mongodb
L'api utilisée est Fastapi
Le package "pymongo" à été utilisé pour la réalisation des méthodes http de requettage CRUD

Est contenu dans chaque fichier :
  - main.py --> contient les quatres méthodes CRUD (get, post, put, delete)
  - test_main.py --> contient les différents test des méthodes CRUD

La base de donnée nommé "test" contient la collection "test" qui elle contient les données qui se présentent sour la forme :
 - _id (généré automatiquement)
 - nom
 - age
 - loisir
