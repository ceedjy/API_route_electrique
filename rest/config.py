import os
from dotenv import load_dotenv

class Config:
    PATH_KEY_API = os.getenv("PATH_KEY_API") # permet de retrouver la clé secrète pour l'api de l'itinéraire dans le .env
