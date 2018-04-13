# Author: Yuki
# Date: April 13th, 2018
# Version: v1.0
# Pokemon lookup tool that uses PokeAPI.

import json
import requests
import sys

DATABASE_URL = "http://pokeapi.co/api/v2"
STATS_FORMAT = {"hp": "HP", "attack": "Attack", "special-attack": "Sp. Attack",
                "defense": "Defense", "special-defense": "Sp. Defense", "speed": "Speed"}
BASIC_INFO = {"Name": "name", "ID": "id", "Weight": "weight", "Abilities": "abilities",
              "Type": "types"}


def basic_info(data: dict):
    info_list = []
    info_list.append(("Name", data["name"]))
    info_list.append(("ID", data["id"]))
    info_list.append(("Weight", str(data["weight"] / 10) + "kg"))
    
    all_abilities = ["Abilities"]
    for index in range(len(data["abilities"])):
        all_abilities.append(data["abilities"][index]["ability"]["name"])
    info_list.append(all_abilities)
    
    if len(data["types"]) == 2:
        info_list.append(("Type", data["types"][0]["type"]["name"],
        data["types"][1]["type"]["name"]))
    else:
        info_list.append(("Type", data["types"][0]["type"]["name"]))

    return info_list


def get_base_stats(data: dict):
    stat_dict = {}

    for stat in data["stats"]:
        stat_dict[stat["stat"]["name"]] = stat["base_stat"]

    return stat_dict


def format_stats(stats_data: dict):
    stats_list = []
    total = 0

    for stat in STATS_FORMAT:
        total += stats_data[stat]
        stats_list.append((STATS_FORMAT[stat], stats_data[stat]))

    stats_list.append(("Total", total))
    return stats_list


def new_lookup(u_input):
    pokemon_id = u_input
    info = requests.get("/".join([DATABASE_URL, "pokemon", pokemon_id]))
    poke_data = json.loads(info.text)
    if "detail" in poke_data:
        print("Error. Please try again.")
        return

    complete_info = basic_info(poke_data) + format_stats(get_base_stats(poke_data))
    for info in complete_info:
        if info[0] == "Type" and len(info[0]) == 2:
            print("{0}: {1} / {2}".format(info[0], info[1].capitalize(), 
            info[2].capitalize()))
        
        elif info[0] == "Abilities":
            capitalized = [ability.capitalize() for ability in info[1:]]
            print("{0}: {1}".format(info[0], ", ".join(capitalized)))

        elif type(info[1]) == str:
            print("{0}: {1}".format(info[0], info[1].capitalize()))

        else:
            print("{0}: {1}".format(info[0], info[1]))

if __name__ == "__main__":
	print("Made by Yuki")
	print("Version 1.0.2")
    command = input("Search for Name or ID of Pokemon ('Q' to quit): ").lower()
    print("------------------\n")
    while command != 'Q':
        new_lookup(command)
        print("------------------\n")
        command = input("Search for Name or ID of Pokemon ('Q' to quit): ").lower()
        print("------------------\n")