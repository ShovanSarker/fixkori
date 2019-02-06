import socket

hostname, sld, tld, port = 'www', 'integralist', 'co.uk', 80
target = '{}.{}.{}'.format(hostname, sld, tld)

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)



# send some data (in this case a HTTP GET request)
def send_now(text, number):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    # client.connect((target, port))
    client.connect(('45.114.84.10', 9999))

    client.send(text + '' + number)

    # receive the response data (4096 is recommended buffer size)
    response = client.recv(4096)
    client.close()
    # client.shutdown()
    return response
