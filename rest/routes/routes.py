from flask import Blueprint, request, jsonify, render_template, current_app
import requests

route_bp = Blueprint("route_bp", __name__)
main_bp = Blueprint("main", __name__)

# route principale 
@main_bp.route("/")
def index():
    return render_template("index.html") # lien avec le html

# test de l'api 
@route_bp.get("/test")
def test():
    return jsonify({"msg": "API ok"}), 200 

# avoir les coor géographiques de 1 ville en particulier 
@route_bp.get("/APIcity/<city>")
def city(city):
    url = "https://nominatim.openstreetmap.org/search" # url pour appeler l'api 
    params = { # paramètres necessaires 
        "q" : city, # ville entrée en parametre 
        "format" : "json",
        "limit" : 1
    }
    headers = {
        'User-Agent': 'info802app' # les param demandés par l'API, c'est une clé d'api sans clé d'api ??? 
    }

    # on recupère la réponse de l'api 
    response = requests.request("GET", url, headers=headers, params=params)
    data = response.json() # on recupère juste le json qui nous intéresse

    # gestion d'erreur 
    if (not data) :
        return jsonify({"error": "Ville non trouvée. Veuillez réessayer."})
    
    # on retourne un json avec juste ce qu'on a besoin : latitude et longitude 
    return jsonify({
        "latitude": float(data[0]["lat"]),
        "longitude":float(data[0]["lon"])
    })

# avoir l'intinéraire entre 2 coordonnées géographiques 
@route_bp.post("/APIpath")
def path():
    data = request.json # on recupère la requette passée en entrée du post pour avoir les datas  
    startPt = data["startPt"]
    endPt = data["endPt"]

    # l'url de l'api 
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    
    # on passe des informations à l'api 
    hearders = {
        "Authorization": current_app.config["PATH_KEY_API"], # permet de retrouver la clé d'api dans le fichier config
        "Content-Type": "application/json"
    }

    # les paramètres d'entrée, on veut le point de départ et le point d'arrivée avec des coordonnées (latitude et longitude inversés car c'est ce que demande l'api)
    params = {
        "coordinates": [
            [startPt[1], startPt[0]],
            [endPt[1], endPt[0]]
        ]
    }

    # on recupère la réponse de l'api 
    response = requests.post(url, headers=hearders, json=params) # json = params car on envoie les parametres sous forme de json
    
    # on retourne la réponse de l'api sous forme de json 
    return response.json()
