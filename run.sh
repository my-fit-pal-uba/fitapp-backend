#!/bin/bash
echo "Ejecutando el contenedor"
docker run -p 8080:8080 -v $(pwd)/src:/usr/local/app/src fit-backend
