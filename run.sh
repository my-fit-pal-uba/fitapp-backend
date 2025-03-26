#!/bin/bash
echo "Ejecutando el contenedor"
docker run -p 5000:8080 -v $(pwd)/src:/usr/local/app/src fitbackend