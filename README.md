# API electric route
This API is a course project about an API for route calculation. And more precisely about electric cars and charging station. <br>
The url to access the website whith my frontend version is : https://info802-rest-cass-gdhbc3dedadgdvgh.francecentral-01.azurewebsites.net <br>

# Documentation for the created API : 
The url for this API is (without endpoint) : https://info802-rest-cass-gdhbc3dedadgdvgh.francecentral-01.azurewebsites.net/api/

## Endpoint : /APIcity/'city'
### Description :
This route gives you the geographic coordinates of a city. <br>
This is a GET route.
### Parameters :
```
city : A city name, a string
```
### Return : 
A JSON with this format : <br>
```
{
    'latitude': ... float,
    'longitude': ... float 
}
```
### API used for this route : 
This route use Nominatim, which use itself OpenStreetMap. <br>
https://nominatim.org/ 

## Endpoint : /APIpath 
### Description :
This route gives you the path between two geographic coordinates. <br>
This is a POST route. 
### Parameters :
A JSON with this format : <br>
```
{   
    'startPt': ... the start point, a point [latitude, longitude], 
    'endPt': ... the end point, a point [latitude, longitude],  
    'bornePts' ... all the points for the charging station, a tab of points [[longitude, latitude], [...] ...]
}
```
### Return : 
A JSON with all points of the path and more. For more informations, you can see the documentation of the API used for this route. 
### API used for this route : 
This route use Openrouteservice. <br>
https://openrouteservice.org/

## Endpoint : /APIborne 
### Description : 
This route gives you all the charging station near a path based on the range of the car. <br>
This is a POST route. 
### Parameters : 
A JSON with this format : <br>
```
{
    'carAuto': ... the car range, a float, 
    'tabPath': ... all points of the path, a tab of points [[longitude, latitude], [...] ...]
}
```
### Return :
A tab of point which represent all the charging stations. 
### API used for this route : 
This route use Opendatasoft. <br>
https://public.opendatasoft.com/explore/assets/georef-france-commune/

## Endpoint : /APIcars
### Description : 
This route gives you a list of cars to use for your trip. <br>
This is a GET route. 
### Parameters : 
None. 
### Return : 
A JSON with this format : <br>
```
{
    "id": ... the car id, a int,
    "make": ... the car make, a string,
    "model": ... the car model, a string,
    "version": ... the car version, a string,
    "image": ... the car image,
    "autonomie": the car range par kilometer, a float
}
```
### API used for this route : 
This route use Chargetrip. <br>
https://www.chargetrip.com/

## Endpoint : /APItime/'speed'/'distance'/'chargeTime'/'nbCharge'
### Description :
This route gives you the time of your trip through a SOAP API. <br>
This is a GET route. 
### Parameters :
A JSON with this format : <br>
```
{
    'speed': ... the mean speed of your car, a float (or a string),
    'distance': ... the total distance of the path, a float (or a string),
    'chargeTime': ... the time of one charge in a charging station, a float (or a string),
    'nbCharge': ... the number of charging stations meet in the path, a int (or a string)
}
``` 
### Return : 
A string of the time with two possible formats : 
- 'hours' h 'minutes' -> if the total time is over an hour,
- 'minutes' min -> if the total time is less than an hour.
### API used for this route : 
This route use a SOAP API created by myself. <br>
No API key required.

## Endpoint : /APIcout/'coutOneBorne'/'nbCharge'
### Description :
This route gives you the total cost of your trip through a SOAP API. <br>
This is a GET route. 
### Parameters :
A JSON with this format : <br>
```
{
    'coutOneBorne': ... the cost of a full battery at one charging station, a float (or a string),
    'nbCharge': ... the number of charging stations meet in the path, a int (or a string)
}
``` 
### Return : 
A string of the cost of you trip. 
### API used for this route : 
This route use a SOAP API created by myself. <br>
No API key required.
