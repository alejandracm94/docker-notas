# Docker Notas

API de notas hecha con Flask y PostgreSQL, que corre en dos contenedores con Docker Compose.

## Servicios
- app: API en Flask (puerto 5000)
- db: PostgreSQL 16 (puerto 5432, solo dentro de la red de Docker)

## Cómo levantarlo
1. Copiar las variables de entorno: `cp .env.example .env`
2. Levantar los contenedores: `docker compose up -d`

## Probarlo
Guardar una nota:
curl -X POST http://localhost:5000/notas -H "Content-Type: application/json" -d "{\"texto\":\"Hola\"}"

Consultar las notas:
curl http://localhost:5000/notas

## Tecnologías
Docker, Docker Compose, Flask, PostgreSQL, GitHub Actions