import json
import socket
import sys
import time
import urllib.request

BASE = "http://localhost:5000"


def fallar(mensaje):
    print("FALLO: " + mensaje)
    sys.exit(1)


# 1. El contenedor de la app debe resolver el nombre del servicio "db"
try:
    ip = socket.gethostbyname("dbx")
    print("OK: el nombre 'db' se resuelve a " + ip)
except Exception as e:
    fallar("no se pudo resolver el nombre 'db': " + str(e))

# 2. La API debe responder (se reintenta mientras arranca)
for _ in range(20):
    try:
        urllib.request.urlopen(BASE + "/notas", timeout=3)
        print("OK: la API responde")
        break
    except Exception:
        time.sleep(3)
else:
    fallar("la API no respondio a tiempo")

# 3. Guardar una nota (la app escribe en PostgreSQL)
texto = "prueba jenkins " + str(int(time.time()))
req = urllib.request.Request(
    BASE + "/notas",
    data=json.dumps({"texto": texto}).encode(),
    headers={"Content-Type": "application/json"},
)
try:
    resp = urllib.request.urlopen(req, timeout=5)
    print("OK: POST /notas respondio " + str(resp.status))
except Exception as e:
    fallar("POST /notas fallo: " + str(e))

# 4. Leer las notas y comprobar que la nueva quedo guardada
try:
    notas = json.load(urllib.request.urlopen(BASE + "/notas", timeout=5))
except Exception as e:
    fallar("GET /notas fallo: " + str(e))

if not any(n.get("texto") == texto for n in notas):
    fallar("la nota guardada no aparece en la base de datos")

print("OK: la nota se guardo y se leyo desde PostgreSQL")
print("TODAS LAS PRUEBAS PASARON")