import json
from typing import List
import requests
from requests.structures import CaseInsensitiveDict

TOKEN_ACCESS_TRACKS = "Bearer BQCsSlCmmf7mDCFKRB8N3uEDYttx2YI76xR-OTfoCFuwRayHsjBz4enY3-vtVuEDMkLPsUnfV7N-Tpumdyn_1a0Vx0lPWh7Y2mShxQ2QUCekPvqMQ7eajuHPiRkWEewdoQo2zWn6JKbPh7pHyTbf_cerdVfqu5971HweFJmmHYB2b0iXQI3j5FTR3Paz"
TOKEN_ACCESS_GENRE = "Bearer BQBBKLxHDyj73VN3iJ_vBQkRNjOG_eM5-m_0LerpquF1srV3J7wIOyY5ACS_ierqpkoqDtkR15eSiapguAHm2V2OeULssCJUV1QjZPqKX6NlmGM59eo6lwmbRlwnjOQYSRuURshAz7OBK_FOIO2A17LgY5dUzpWnKHvQjs_BtZKVgjaLfz8TYjozTfqB"
TOKEN_ACCESS_FT_PLAYLIST = "Bearer BQCZNJ-F73xPccDN-xPWyVJeFivJgu9SIB3w68Ji144SsKEYnt1UakM-XAQxoaA_szufJz-bmiMHhephQ-JjcTY9jtCf_iLDloRFnVfdxtluOcWGnfrXtsb9M9oNeO_Q3CO5USUlGX2t8UBSOD5Lm8eBI9tvmMU0Ll7Al8jmN241r-dAeDDRWqqUH3OM"
TOKEN_ACCESS_PL_TRACKS = "Bearer BQCP8CAS5fB_9DsyQNNoUnZdaq5qTy5dbcSmSQu7X8QnE4SQ0GCAjfBTq6l7TudNsjudD7eiCT8AOgH0BzIgPwtGmSGunX2EbRH_tc2bUNgb4BPnA9Sqr7c838wEsX92qzY_AspjWjXgtTWO31xM_tyuMsdpOrIu78f4t65fesbdJ0iJqRaPoY8PG8ux"
LIMIT = 10


def get_genre(modified_ids):

    url = f"https://api.spotify.com/v1/artists?ids={modified_ids}"

    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = TOKEN_ACCESS_GENRE

    resp = requests.get(url, headers=headers)
    return resp.json()


url = f"https://api.spotify.com/v1/me/tracks?market=ES&limit={LIMIT}&offset=5"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = TOKEN_ACCESS_TRACKS


resp = requests.get(url, headers=headers)

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


modified_ids = ", ".join(ids)
modified_ids = modified_ids.replace(' ', '')
parsed = get_genre(modified_ids)

#print(json.dumps(parsed, indent=4, sort_keys=True))
# genre = {}
# for i in range(10):
#     if parsed['artists'][i]['genres'] in genre[parsed['artists'][i]['genres']].keys():
#         genre[parsed['artists'][i]['genres']] += 1
#     else:
#         genre[parsed['artists'][i]['genres']] = 1
# print(genre)


genres = []
for i in range(10):
    genres.append(parsed['artists'][i]['genres'])

print(genres)

genre_occurance = {}
for genre in genres:
    for i in genre:
        if i in genre_occurance.keys():
            genre_occurance[i] += 1
        else:
            genre_occurance[i] = 1

print()
genre_occurance = dict(
    sorted(genre_occurance.items(), key=lambda item: item[1]))
print(genre_occurance)

genres = []
for i in range(10):
    genres.append(parsed['artists'][i]['genres'])


url = "https://api.spotify.com/v1/browse/featured-playlists?country=PH"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = TOKEN_ACCESS_FT_PLAYLIST

resp = requests.get(url, headers=headers)

parsed = resp.json()
print(json.dumps(parsed, indent=4, sort_keys=True))


playlists = {}
playlist_ids = []

for item in parsed['playlists']['items']:
    playlists[item['id']] = item['name']
    playlist_ids.append(item['id'])

    print(f"{item['id']}\n{item['name']}")
    print()

url = "https://api.spotify.com/v1/playlists/37i9dQZF1DXcZQSjptOQtk/tracks?market=PH"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = TOKEN_ACCESS_PL_TRACKS


resp = requests.get(url, headers=headers)
data = resp.json()
print(json.dumps(data, indent=4, sort_keys=True))


# print(data['items'][0])
# print(json.dumps(data['items'][0]['track']['album']['name'], indent=4, sort_keys=True))
tracks_population = {}
for item in data['items']:
    track_id = item['track']['album']['id']
    track_name = item['track']['album']['name']
    artists_id = item['track']['album']['artists'][0]['id']
    artists_name = item['track']['album']['artists'][0]['name']
    tracks_population[track_id] = [track_name, {artists_id: artists_name}]
    # print(item['track']['album']['name'])

# print(tracks_population)

    # print(item['track']['album']['id'])
    # print(item['track']['album']['artists'][0]['name'])
    # print(item['track']['album']['artists'][0]['id'])
