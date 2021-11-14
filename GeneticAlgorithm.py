# %% [markdown]
# # <h1><b> Spotfiy Recommender System
#

# %% [markdown]
# <h3>
# System: Genetic Algorithm <br>
# API: Spotify for Developers <br>
# Lang: Python (conda base)<br>
# Copyright: 2021 <br>
# Developer: Martin Erickson Lapetaje
# </h3>
#

# %% [markdown]
# ## Replace fields below

# %%
import requests
import random
import numpy as np
from requests.structures import CaseInsensitiveDict
from typing import List
import json
TOKEN_ACCESS = 'Bearer BQD9tppQWjAYLdXvmgSolAQ_0U5MH-kRy8_Jc68tTmX6d6c8pwwVoXIrL4Lva94Eiy4q8sx6wk8gAo3oaaEza3tBaCR9GbR0xdJUTJitTtIskSgOQNoLtSQIgZzy2bc-bhuLZHn4F_pc1n36fBrwHubdluZHem5AVmwk-FrGKdHgNF3qIiwJ_D845befFrnOmW-06ayduqttFo51X5WMgK3o8nVgta8DNXdtk_iX-7sAAziIq_OKh2RglA'
USER_ID = '22ss5cgw4ofmnwzoq3evu7gpa'

# %% [markdown]
# ## Imports
#

# %%

# %% [markdown]
#
# ## Constant Variables
#
# ### refresh tokens
# <a href="https://developer.spotify.com/console/get-current-user-saved-tracks/?market=ES&limit=10&offset=5">TOKEN_ACCESS_SAVED_TRACKS </a><br>
# <a href="https://developer.spotify.com/console/get-several-artists/?ids=">TOKEN_ACCESS_SEVERAL_ARTIST </a><br>
# <a href="https://developer.spotify.com/console/get-featured-playlists/?country=PH&locale=&timestamp=&limit=&offset=">TOKEN_ACCESS_SAVED_TRACKS </a><br>
# <a href="https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=37i9dQZF1DXcZQSjptOQtk&market=PH&fields=&limit=&offset=&additional_types=">TOKEN_ACCESS_PLAYLIST_ITEMS </a><br>
#

# %%
LIMIT = 10
ARTIST_ID = 1
GENRE = 0
CHROMOSOME = 1
GENE = 1
GENRES = 2
FITNESS = 10

# %% [markdown]
# ## Defined Functions

# %%


def printf(parsed):
    print(json.dumps(parsed, indent=4, sort_keys=True))

# %% [markdown]
# # <b> Part 1: Intializing Data From Spotify API
# ## API queries and extracting of relevant data

# %% [markdown]
# ![title](img/gatherUserData.png)

# %% [markdown]
# ## GET Top Tracks
#

# %% [markdown]
# ![title](img/userTopTracks.png)

# %%


url = "https://api.spotify.com/v1/me/tracks?market=PH&limit=50&offset=0"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = TOKEN_ACCESS


resp = requests.get(url, headers=headers)
print(resp)

# %% [markdown]
# ## EXTRACT: track ids, track name, artist name and artist ids
#
#

# %%
parsed = resp.json()
print(resp.status_code)
# print(len(parsed['items']))

artists_ids = []
for item in parsed['items']:
    artists_ids.append(item['track']['artists'][0]['id'])

    print(f"track: {item['track']['name']}")
    print(f"artist: {item['track']['artists'][0]['name']}\n")

# %% [markdown]
# ## GET Genre From Artists
#

# %%
printf(artists_ids)

# %% [markdown]
# ![title](img/genreTracks.png)
#

# %%


def get_genre(modified_ids):

    url = f"https://api.spotify.com/v1/artists?ids={modified_ids}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = TOKEN_ACCESS
    resp = requests.get(url, headers=headers)

    return resp.json()


def slice_genre_list(artists_ids):
    new_artists_ids = list(set(artists_ids))
    genre_list = []
    len_artists = 0
    start = 0
    while len_artists < len(new_artists_ids):
        len_artists += 10
        modified_ids = ", ".join(artists_ids[start: len_artists])
        modified_ids = modified_ids.replace(' ', '')
        genre_list.append(get_genre(modified_ids))
        start = len_artists

    return genre_list


genre_list = []
genre_list = slice_genre_list(artists_ids)
printf(genre_list)


# %% [markdown]
# ## EXTRACT: Genres of artists

# %%
genres_initlized = []
for artists in genre_list:
    for genres in artists['artists']:
        ''.append(genres['genres'])

# %% [markdown]
# ## EXTRACT: cccurances in genre

# %%


def genre_occurances(genres_initlized):
    genre_occurance = {}
    for genre in genres_initlized:
        for i in genre:
            if i in genre_occurance.keys():
                genre_occurance[i] += 1
            else:
                genre_occurance[i] = 1
    return genre_occurance


genre_occurance = genre_occurances(genres_initlized)
genre_occurance = dict(
    sorted(genre_occurance.items(), key=lambda item: item[1]))
print(json.dumps(genre_occurance, indent=4, sort_keys=False))

# %% [markdown]
#

# %% [markdown]
# ## REQUEST: Seeding PH featured playlist from spotify

# %% [markdown]
# ![title](img/featuredPlaylist.png)

# %%
url = "https://api.spotify.com/v1/browse/featured-playlists?country=PH"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = TOKEN_ACCESS

resp = requests.get(url, headers=headers)

parsed = resp.json()
print(json.dumps(parsed, indent=4, sort_keys=True))

# %% [markdown]
# ## EXTRACT: extract query result into playlist ID and Name

# %%
playlists = {}
playlist_ids = []

for item in parsed['playlists']['items']:
    playlists[item['id']] = item['name']
    playlist_ids.append(item['id'])

    print(f"{item['id']}\n{item['name']}")
    print()

# %%
print(playlist_ids)

# %% [markdown]
# ## REQUEST: seeding tracks from each playlist

# %% [markdown]
# ![title](img/populationTracks.png)

# %%


def get_playlist_items(playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?market=PH"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = TOKEN_ACCESS

    resp = requests.get(url, headers=headers)
    return resp.json()


# playlist_ids = get_playlist_items(playlist_ids)
tracks = []
for item in playlist_ids:
    tracks.append(get_playlist_items(item))

    #print(json.dumps(track, indent=4, sort_keys=True))
printf(tracks)

# %%
# print(tracks)
# print(json.dumps(tracks, indent=4, sort_keys=True))
print(len(tracks))

# %% [markdown]
# ## Extracting data from query request

# %%
# 3DpduguWUTtn3NQ1PFr2Kd
tracks_population = {}
artists_ids = []

for track in tracks:
    for item in track['items']:
        if item['track'] is not None:
            track_id = item['track']['id']
            track_name = item['track']['album']['name']
            artists_id = item['track']['album']['artists'][0]['id']
            artists_name = item['track']['album']['artists'][0]['name']

            tracks_population[track_id] = [
                track_name, {artists_id: artists_name}]
            artists_ids.append(artists_id)

# print(json.dumps(tracks_population, indent=4, sort_keys=True))
printf(tracks_population)

# %%

print(artists_ids)

# %% [markdown]
# ## Removing duplicate Artist's ID
# ### without Removing duplicate the total Artist's ID in the list was 24,000+ which this will result an error in requesting for a query

# %%
artists_ids_set = list(set(artists_ids))
printf(artists_ids_set)

# %% [markdown]
# ## Slice list for API requst 50 artist at most

# %%
lst = np.arange(0, len(artists_ids_set), 50)
len_artists = 0
start = 0

genre_list = []
while len_artists < len(artists_ids_set):
    len_artists += 10

    modified_ids = ", ".join(artists_ids[start: len_artists])
    # genre_list.append(get_genre(modified_ids))
    modified_ids = modified_ids.replace(' ', '')

    print()

    printf(modified_ids)
    genre_list.append(get_genre(modified_ids))
    start = len_artists

# %% [markdown]
# ## Extract artist's genres

# %%
genre_list_all = slice_genre_list(artists_ids_set)
printf(genre_list)

# %% [markdown]
# ## EXTRACT: dictionary for artists genre

# %%
genres_in_population = {}
for artists in genre_list:
    print(genre_list)
    for genres in artists['artists']:
        genres_in_population[genres['id']] = [genres['genres'], genres['name']]

printf(genres_in_population)
print(len(genres_in_population))

# %% [markdown]
# ## Adding genres in populated tracks
# ## Initializing list of populated tracks

# %%


def get_key(var):
    key = list(var)
    return key[0]


print(len(tracks_population))

database = []
for key in tracks_population:
    track = tracks_population[key][ARTIST_ID]
    id = get_key(tracks_population[key][ARTIST_ID])

    if(id in genres_in_population.keys()):
        genre = genres_in_population[id][GENRE]
        tracks_population[key].append(genre)

    database.append([key, tracks_population[key]])

# print(tracks_population[key])


# %% [markdown]
# ## database population length

# %%
database_len = len(database)
print(database_len)

# %% [markdown]
# # <b> How do we get the fitness of each chromosome?
#

# %% [markdown]
# ![title](img/populationTracks.png)

# %% [markdown]
# # <b> Part 2: Initialize Population
# ## Generate 10 random tracks from database and to populated generation

# %% [markdown]
# ![title](img/trackDatabase.png)

# %% [markdown]
# ## Generate Chromosomes and Population

# %%
NUMBER_OF_CHROMO = 4


def generate_chromosomes():
    num = random.sample(range(database_len), LIMIT)
    return num


def genrate_population():
    population = {}
    for gen in range(NUMBER_OF_CHROMO):
        chromosomes = []
        for index in generate_chromosomes():
            chromosomes.append(database[index])

        population[gen] = chromosomes

    return population


population = genrate_population()


# %%
CHROMOSOME_ZERO = 0
printf(population[CHROMOSOME_ZERO])


# %% [markdown]
# # <b> Part 3: Fitness of each chromosome
# ## seed the fitness of a gene and sum the total in each chromosome

# %% [markdown]
# ![title](img/fitness.png)

# %%
def fitness_function(population):
    for chromosomes in population:
        fitness = 0

        for chromosome in population[chromosomes]:
            if not isinstance(chromosome, int) and len(chromosome[GENE]) > 2:
                for gene in chromosome[GENE][GENRES]:
                    if gene in genre_occurance.keys():
                        fitness += genre_occurance[gene]

        if len(population[chromosomes]) > 10:
            population[chromosomes][10] = fitness
        else:
            population[chromosomes].append(fitness)

        # print(population[chromosomes])


fitness_function(population)
# printf(population)

# %% [markdown]
# # <b> Part 4: Selection of parents
# ## The idea of selection phase is to select the fittest individuals and let them pass their genes to the next generation.

# %% [markdown]
# ![title](img/parent.png)

# %% [markdown]
# ## Get the highest fitness parents

# %%


def selection_function():
    fitness_val = []
    for chromosome in population:
        fitness = population[chromosome][FITNESS]
        fitness_val.append(population[chromosome][FITNESS])

    fitness_val.sort(reverse=True)
    fitness_val_drop = fitness_val[2:]
    fitness_val = fitness_val[:-2]
    return fitness_val, fitness_val_drop


fitness_val, fitness_val_drop = selection_function()

print(fitness_val)
print(fitness_val_drop)

# %% [markdown]
# # <b> Part 5: Crossover of parents chromosomes
# ## Crossover is the most significant phase in a genetic algorithm. For each pair of parents to be mated, a crossover point is chosen at random from within the genes.

# %% [markdown]
# ![title](img/crossover.png)

# %%


def crossover(parent):
    for i in range(4):
        parent[0][i], parent[1][-(i+2)] = parent[1][-(i+2)], parent[0][i]


def crossover_function(fitness):
    crossover_parent = []
    iteration = 0

    for fitness in fitness:
        for chromosome in population:
            if fitness == population[chromosome][FITNESS]:
                iteration += 1
                crossover_parent.append(population[chromosome])

                if iteration % 2 == 0:
                    crossover(crossover_parent)
                    crossover_parent.clear()


crossover_function(fitness_val)
crossover_function(fitness_val_drop)

# %% [markdown]
# # <b> Part 6: Mutation
# ## In certain new offspring formed, some of their genes can be subjected to a mutation with a low random probability.
#

# %% [markdown]
# ![title](img/mutation.png)

# %% [markdown]
# ## Mutation of child chromosome

# %%


def mutation(population_chromosome):
    num_of_mutation = random.choice(range(0, 2))
    for num in range(num_of_mutation):
        gene_to_mutate = random.choice(range(0, 10))
        random_gene = random.choice(range(database_len))
        population_chromosome[gene_to_mutate] = database[random_gene]


def mutation_function(fitness, population):
    for fit in fitness:
        for chromosome in population:
            if fit == population[chromosome][FITNESS]:
                mutation_2(population[chromosome])


# %% [markdown]
# ## Select the most unfit track
# ### Conditions:<br>lowest genre score track<br>no genre available<br>genre unrealated to users genre count

# %%
BODY = 1
DETAILS = 1
ID = 0


def generate_gene():
    random_gene = random.choice(range(database_len))
    return database[random_gene]


def get_fintess(genres):
    fit_value = 0
    for genre in genres:
        if genre in genre_occurance.keys():
            fit_value += genre_occurance[genre]

    return fit_value


def replace_gene_lowest(population_chromosome, key):
    for gene in range(len(population_chromosome)):
        this_gene = population_chromosome[gene]
        if not isinstance(this_gene, int):
            if this_gene[ID] == key:
                population_chromosome[gene] = generate_gene()


def mutate_low_fit_gene(population_chromosome):
    temp = {}
    for gene in range(len(population_chromosome)):
        this_gene = population_chromosome[gene]
        if not isinstance(this_gene, int):
            fit = get_fintess(this_gene[BODY][GENRES])
            temp[this_gene[ID]] = fit

    # print(temp)
    temp = dict(sorted(temp.items(), key=lambda item: item[1]))
    key = next(iter(temp))

    replace_gene_lowest(population_chromosome, key)


def mutation_2(population_chromosome):
    clean = True
    for gene in range(len(population_chromosome)):
        this_gene = population_chromosome[gene]

        if not isinstance(this_gene, int):
            if len(this_gene[BODY]) < 3:
                clean = False
                population_chromosome[gene] = generate_gene()
                break

            if this_gene[BODY][GENRES] == []:
                clean = False
                population_chromosome[gene] = generate_gene()
                break

    if(clean):
        mutate_low_fit_gene(population_chromosome)


# %%


# %%
def printpop(population_chromosome):
    print(population_chromosome)

    for chromosome in population_chromosome:
        print(f'{chromosome}')


print(f'\nBefore')
for chromosomes in population:
    printpop(population[chromosomes])


mutation_function(fitness_val, population)
mutation_function(fitness_val_drop, population)

print(f'\nAfter')
for chromosomes in population:
    printpop(population[chromosomes])
    # printpop(chromosomes)


# %%


# %% [markdown]
# ## new chromosomes in low fitness chromosomes

# %%
def generate_new_chromosomes():
    new_chromosomes = []
    for chromo_index in generate_chromosomes():
        new_chromosomes.append(database[chromo_index])

    return new_chromosomes


def new_chromosomes_function():
    for fitness in fitness_val_drop:
        for chromosome in population:
            if len(population[chromosome]) > 10 and fitness == population[chromosome][FITNESS]:
                population[chromosome] = generate_new_chromosomes()


print('before')
for chromosome in population:
    print()
    print(population[chromosome])

# new_chromosomes_function()

print('\nafter')
for chromosome in population:
    print()
    print(population[chromosome])

# %% [markdown]
# # <b> Part 6: Loop back until generation 500th

# %%
population = genrate_population()

# %%


def this_generation(generation_count):
    avg = 0
    print(f'\nGeneration: {generation_count}\nFitness: ', end='')
    for chromosome in range(4):
        print(f'{population[chromosome][10]}', end=' ')
        avg += population[chromosome][10]

    print(f'\navg: {avg}\n')


# %%
generation_count = 0
MAX_GEN = 250

for generation in range(MAX_GEN):
    generation_count += 1

    fitness_function(population)
    this_generation(generation_count)
    fitness_val, fitness_val_drop = selection_function()

    crossover_function(fitness_val)
    crossover_function(fitness_val_drop)

    mutation_function(fitness_val, population)
    mutation_function(fitness_val_drop, population)

    # new_chromosomes_function()


# %% [markdown]
# # <b>Part 7: The result of Genetic Algorithm

# %%
for chromosomes in population:
    print()
    for chromosome in population[chromosomes]:
        print(chromosome)

# %% [markdown]
# ## Extract the highest fitness chromosome

# %%
most_fit_value = fitness_val[0]
print(most_fit_value)

# %% [markdown]
# # <b> Part 8: Creating the playlist

# %% [markdown]
# ## API request for generating a playlist in spotify

# %%
TOKEN_ACCESS_GENERATE = 'Bearer BQDE4onYvetvIYZRRAv4qTuRc8HApVIZVywAUNH3ewinCPrNV9UCnQJznfLmWAraPwfbe2H1fze5vst8rO9d4CqHgbz6fS-5D-p2HgW-_NMHNGErV5khoOr8Hd38aYkeN9s14PTdQ9rc18R-IO-8X0ADWzknXw0wjfxJXKsL8DQTdGm9-pP8QGG5NLk_h16fJxvf1_Mq4X7boX8fNaZ1syHj3l4lTUHd4UTWNT2xS0HxRhPxSQfRt-FTfg'
TITLE = f"Groove #{most_fit_value}"
DESCRIPTION = f"Playlist generated by a genetic algorithm, a method of solving based on a natural selection process that mimics biological evolution, AI analysis from liked tracks, with fitness value of {most_fit_value} in the {MAX_GEN}th generation, developed by Martin Erickson Lapetaje, BSCS-3 of USJ-R"

url = f"https://api.spotify.com/v1/users/{USER_ID}/playlists"

headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = TOKEN_ACCESS

data = {"name": TITLE, "description": DESCRIPTION, "public": "false"}
resp = requests.post(url, headers=headers, data=json.dumps(data))

printf(resp.json())

# %%
result = resp.json()
playlist_id = result['id']

# %% [markdown]
# ## Appending the parent chromosome track IDs
#

# %%
track_ids = []
for chromosomes in population:
    if most_fit_value == population[chromosomes][FITNESS]:
        for chromosome in population[chromosomes]:
            if not isinstance(chromosome, int):
                track_ids.append("spotify%3Atrack%3A"+chromosome[ID])
                # track_ids.append(chromosome[ID])


track_ids = "%2C".join(track_ids)
track_ids = track_ids.replace(' ', '')
print(track_ids)


# %% [markdown]
# ## Adding the tracks from the result of our Genetic algorithm

# %%
# url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks?uris=spotify%3Atrack%3A4iV5W9uYEdYUVa79Axb7Rh%2Cspotify%3Atrack%3A1301WleyT98MSxVHPZCA6M"
url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={track_ids}"

headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"
headers["Authorization"] = TOKEN_ACCESS
headers["Content-Length"] = "0"


resp = requests.post(url, headers=headers)

print(resp.status_code)


# %% [markdown]
# ## The generated playlist

# %% [markdown]
# ![title](img/result.png)
