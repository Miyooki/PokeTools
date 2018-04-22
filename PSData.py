# @Author: Yuki
# Date: April 20th, 2018
# Version: 1.0.2
# Pokemon Showdown replay data scrapper.

from urllib.request import Request, urlopen

# file_name = input("Enter the name of the file: ")
# test_file = "Gen7DoublesOU-2018-04-16-miyooki-princeofbellair"
# ps_file = open(file_name + ".html")

# data = []
# for line in ps_file:
#    if line != "\n":
#        data.append(line.strip())


replay_url = input("Enter Pokemon Showdown replay URL: ")

web_request = Request(replay_url + ".log", headers={'User-Agent': 'Mozilla/5.0'})
data_log = urlopen(web_request)

data = []
for line in data_log:
    data.append(line.strip().decode("utf-8"))


def get_player_names(data):
    name1 = next(info for info in data if "|player|p1" in info).split("|")[3]
    name2 = next(info for info in data if "|player|p2" in info).split("|")[3]
    return(name1, name2)


def get_pokemons(data):
    try:
        p1_team_size = int(next(info for info in data if "|teamsize|p1" in info).split("|")[3])
        p2_team_size = int(next(info for info in data if "|teamsize|p2" in info).split("|")[3])
    except:
        p1_team_size = 6
        p2_team_size = 6

    p1_poke_list = []
    p2_poke_list = []

    for index in range(len(data)):

        if "|poke|p1" in data[index]:
            while len(p1_poke_list) < p1_team_size:
                p1_poke_list.append(data[index].split("|")[3:])
                index += 1

        if "|poke|p2" in data[index]:
            while len(p2_poke_list) < p2_team_size:
                p2_poke_list.append(data[index].split("|")[3:])
                index += 1
            break

    p1_poke_list = [poke[0].split(", ")[0] for poke in p1_poke_list]
    p2_poke_list = [poke[0].split(", ")[0] for poke in p2_poke_list]

    return p1_poke_list, p2_poke_list


def poke_name_parser(poke_list):
    for index in range(len(poke_list[0])):
        if poke_list[0][index] == "Landorus-Therian":
            poke_list[0][index] = "Landorus"
    
    for index in range(len(poke_list[1])):
        if poke_list[1][index] == "Landorus-Therian":
            poke_list[1][index] = "Landorus"

    return poke_list

def possible_moves(data, pokemons):

    p1_moves_dict = dict((poke, []) for poke in pokemons[0])
    p2_moves_dict = dict((poke, []) for poke in pokemons[1])

    for moves in data:

        if "|move|p1" in moves:
            separator = moves.split("|")
            poke_id = separator[2].split(" ")[1]
            if separator[3] not in p1_moves_dict[poke_id]:
                p1_moves_dict[poke_id].append(separator[3])

        if "|move|p2" in moves:
            separator = moves.split("|")
            poke_id = separator[2].split(" ")[1]
            if separator[3] not in p2_moves_dict[poke_id]:
                p2_moves_dict[poke_id].append(separator[3])

    return p1_moves_dict, p2_moves_dict


print("Pokemon Showdown Info Scrapper")
print("------------------------------\n")
print("Showing data for " + replay_url)

names = get_player_names(data)
pokemons = poke_name_parser(get_pokemons(data))
moves = possible_moves(data, pokemons)

print("Player 1:", names[0])
print("Pokemon used:")
for poke in moves[0]:
    print("{0}: {1}".format(poke, moves[0][poke]))

print("\n")

print("Player 2:", names[1])
print("Pokemon used:")
for poke in moves[1]:
    print("{0}: {1}".format(poke, moves[1][poke]))

print("------------------------------\n")
