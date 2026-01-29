from spyne.service import ServiceBase
from spyne.application import Application
from spyne import rpc, Unicode, Integer, Iterable
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11

class HelloWorldService(ServiceBase):
    @rpc(float, float, _returns=str)
    def temps(ctx, v, dist): # vitesse moyenne en km/h et distance en km 
        tps = dist/v
        if tps < 1 : # tps est en heure 
            # mettre en minutes 
            m = int((tps % 1)*60)
            res = str(m) + ' min'
        else : 
            # mettre en heure 
            h = int(tps)
            m = int((tps % 1)*60) 
            res = str(h) + 'h' + str(m)
        return res 

    @rpc(float, float, _returns=str)
    def cout(ctx, coutParKm, dist): # cout par km/h en € et distance en km TODO : refaire en prenant compte de l'autonomie et du tps de chargement
        cout = coutParKm * dist
        return str(cout) + "€"
    
application = Application(
    [HelloWorldService], 
    'spyne.examples.hello.soap', 
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()