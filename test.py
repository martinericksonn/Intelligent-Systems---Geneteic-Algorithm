import json
from typing import List
import requests
from requests.structures import CaseInsensitiveDict

TOKEN_ACCESS = 'BQCv_emMY2JRcWC0efmAla68ScX-KBzS31iKmLlfMq7SFKhDJAcHOijbGAxL2K_qDDK0Nt50YqmvjsJUGoOcurWMcEJWpj3CDAskks9gMIm4ctTmdJiZPa_jf3jOi26j2rXPCV0UBMtFL5RfU9ma4iAsl01ir4xBDAzHa3FAFJIuNpLa-X9mWYKGLzUG'

url = "https://api.spotify.com/v1/me/tracks?market=ES&limit=10&offset=5"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = "Bearer BQC9hG_IXStBFEFBPEsOC0BwSG6twlmEzM1IiaY2JTpBIwMa3G4-u7vvkIpIMQZf7ZZnjLh2CJ-HoHyn5rgmWu4RTLtAo7deN1nFXyll7H2q8_XGNgFLJw5mT6curOaR5KmNbHuzzwsUoYXpYmBmLL13cBL6V1bFzJxBcFjbeDtK9hQo9LaoOxhQA4pZ"

resp = requests.get(url, headers=headers)
parsed = resp.json()

# print(json.dumps(parsed['items'][0]['track']
#       ['album']['name'], indent=4, sort_keys=True))

print(resp.status_code)
print()

ids = []
for i in range(10):
    ids.append(parsed['items'][i]['track']
               ['album']['artists'][0]['id'])

    print('track:\t' + parsed['items'][i]['track']
          ['album']['name'])

    print('id:\t' + parsed['items'][i]['track']
          ['album']['artists'][0]['id'])

    print('artist:\t' + parsed['items'][i]['track']
          ['album']['artists'][0]['name'])

    print()
