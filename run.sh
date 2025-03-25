#!/bin/bash

# Construir la imagen Docker
echo "Construyendo la imagen Docker..."
docker build -t fit-backend .

# Ejecutar el contenedor Docker
echo "Ejecutando el contenedor Docker..."
docker run -p 5000:5000 fit-backend