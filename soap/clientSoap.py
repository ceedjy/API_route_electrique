import zeep

wsdl = 'http://127.0.0.1:8000/?wsdl'
client = zeep.Client(wsdl=wsdl)
print(client.service.temps(50.0, 1.0))
print(client.service.cout(40.0, 100.0))
