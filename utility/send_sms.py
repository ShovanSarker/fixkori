import urllib.parse
import urllib.request


def send_now(number, text):
    username = '01619262692'
    password = 'R8W54DN7'
    number = number
    message = text
    params = urllib.parse.urlencode({'username': username,
                               'password': password,
                               'number': number,
                               'message': message})
    response = urllib.request.urlopen('http://66.45.237.70/api.php?' + params)
    response.close()
    return 'Success'
