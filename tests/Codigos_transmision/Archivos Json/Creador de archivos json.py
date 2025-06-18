import json
import os
ruta= "Ruta del archivo"
contenidos=""
try: 
    with open(ruta, "r", encoding="utf-8") as palabras:
        contenidos = palabras.read()
        print(contenidos)
except Exception as e:
    print("Hubo un error con la ruta")
words= contenidos.split()
print(words) 
with open("palabras.json", "w", encoding="utf-8") as js:
    json.dump({"palabras": words}, js, ensure_ascii=False, indent=2)
    print("Archivo json fue creado")

