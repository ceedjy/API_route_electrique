from flask import Blueprint, request, jsonify, render_template, current_app
import requests
import math as mt
import zeep

route_bp = Blueprint("route_bp", __name__)
main_bp = Blueprint("main", __name__)

# pour le soap :
wsdl = 'http://127.0.0.1:8000/?wsdl'
clientZeep = zeep.Client(wsdl=wsdl)

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
    bornePts = data["bornePts"]

    # l'url de l'api 
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    
    # on passe des informations à l'api 
    hearders = {
        "Authorization": current_app.config["PATH_KEY_API"], # permet de retrouver la clé d'api dans le fichier config
        "Content-Type": "application/json"
    }

    # les paramètres d'entrée, on veut les points de passage dans l'ordre avec en premier le point de départ et en dernier le point d'arrivée (latitude et longitude inversés car c'est ce que demande l'api)
    bornePts.append([endPt[1], endPt[0]])
    bornePts.insert(0,[startPt[1], startPt[0]])
    print(bornePts)
    params = {
        "coordinates": bornePts
    }

    # on recupère la réponse de l'api 
    response = requests.post(url, headers=hearders, json=params) # json = params car on envoie les parametres sous forme de json
    
    # on retourne la réponse de l'api sous forme de json 
    return response.json()

# avoir les bornes entre 2 points géographiques
@route_bp.post("/APIborne")
def borne():
    data = request.json # on recupère la requette passée en entrée du post pour avoir les datas  
    autonomie = int(data["carAuto"]) * 1000 # autonomie de la voiture, *1000 pour le mettre en mètre 
    tabPath = data["tabPath"] # tous les points du chemin, longitude - latitude 

    tabBorne = []
    indice = 0 # indice du tableau de point 
    autonomie80 = autonomie * 90 / 100
    autonomie10 = autonomie * 10 / 100
    # tant qu'il reste du chemin à parcourir 
    while(indice < len(tabPath)-2):
        # on va chercher le point où on est à 90% de l'autonomie de la voiture 
        tempDist = 0 # distance temporaire pour faire la comparaison 
        while(tempDist < autonomie80 and indice < (len(tabPath)-2)):
            indice += 1 
            tempDist += mt.sqrt((tabPath[indice+1][0] - tabPath[indice][0])**2 + (tabPath[indice+1][1] - tabPath[indice][1])**2) * 111000
        # a partir de là, le point à partir duquel on cherche la borne est à tabPath[indice]
        if (indice != (len(tabPath)-2)):
            # on cherche où est la borne la plus proche à partir du point tabPath[indice]
            borne = findOneBorne(tabPath[indice], autonomie10)

            # gestion des erreurs
            if(borne != [-1, -1]): 
                tabBorne.append(borne)
            else:
                # on a pas trouvé de borne à proximité 
                autonomie25 = autonomie * 25 / 100
                # on recule de 1/4 de l'autonomie 
                tempDist = 0 # distance temporaire pour faire la comparaison 
                while(tempDist < autonomie25 and indice < (len(tabPath)-2)):
                    indice -= 1 
                    tempDist += mt.sqrt((tabPath[indice+1][0] - tabPath[indice][0])**2 + (tabPath[indice+1][1] - tabPath[indice][1])**2) * 111000
                # a partir de là, le point à partir duquel on cherche la borne est à tabPath[indice], on prend 1/4 de l'autonomie comme étant le rayon de recherche
                borne = findOneBorne(tabPath[indice], autonomie25)
                tabBorne.append(borne)

    return tabBorne

# retrouve une seule borne à partir d'un point et d'une distance 
def findOneBorne(point, distance):
    # l'url de l'api
    url = "https://odre.opendatasoft.com/api/records/1.0/search/"
    params = {
        "dataset": "bornes-irve",
        "rows": 1,
        "geofilter.distance": f"{point[0]},{point[1]},{distance}"
    }

    # on recupère la réponse de l'api 
    response = requests.get(url, params=params) 
    response = response.json()
    if(response["nhits"] != 0):
        borne = response["records"][0]["fields"]["coordonneesxy"] # latitude, longitude 
    else:
        borne = [-1, -1]

    # on retourne la réponse de l'api sous forme de json 
    return borne

@route_bp.get("/APIcars")
def cars():
    url = "https://api.chargetrip.io/graphql"

    headers = {
        "Content-Type": "application/json",
        "x-client-id": current_app.config["ROUTE_KEY_API_CLIENT_ID"],
        "x-app-id": current_app.config["ROUTE_KEY_API_APP_ID"]
    }

    # $page, $size, $search : valeurs par default pour la version gratuite -> 0, 10, tous les véhicules
    query = """
    query vehicleList($page: Int, $size: Int, $search: String) {
        vehicleList(
            page: $page, 
            size: $size, 
            search: $search
        ) {
            id
            naming {
                make
                model
                chargetrip_version
            }
            range {
                chargetrip_range {
                    best
                }
            }
            media {
                image {
                    thumbnail_url
                }
            }
        }
    }
    """

    response = requests.post(
        url,
        json={"query": query},
        headers=headers
    )

    data = response.json()
    cars = []
    for car in data["data"]["vehicleList"]:
        cars.append({
            "id": car["id"],
            "make": car["naming"]["make"],
            "model": car["naming"]["model"],
            "version": car["naming"]["chargetrip_version"],
            "image": car["media"]["image"]["thumbnail_url"],
            "autonomie": car["range"]["chargetrip_range"]["best"]
        })

    return cars

@route_bp.get("/APItime/<speed>/<distance>/<chargeTime>/<nbCharge>")
def time(speed, distance, chargeTime, nbCharge):
    #temp = float(distance) /float(speed) + float(chargeTime)*int(nbCharge)
    #return {"res": str(temp)}
    return clientZeep.service.time(float(speed), float(distance), float(chargeTime), int(nbCharge))

@route_bp.get("/APIcout/<coutOneBorne>/<nbCharge>")
def cout(coutOneBorne, nbCharge):
    #return {"res": str(float(coutOneBorne) * int(nbCharge))}
    return clientZeep.service.cout(float(coutOneBorne), int(nbCharge))
