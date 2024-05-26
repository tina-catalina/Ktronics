# Ktronics

Para instalar las librerías iniciales de pip ejecutar: pip install -r requirements.txt
Una vez instaladas las librerías, puede utilizar el .env de ejemplo para tener las variables de entorno ya declaradas, por ejemplo Flask pide indicar donde se encuenta la FLASK_APP (main.py), y otras variables como DB_PORT las utiliza el docker-compose de ejemplo.

Para Ubuntu es necesario instalar los siguientes paquetes:
    sudo apt-get update
    sudo apt-get install build-essential libpq-dev python3-dev