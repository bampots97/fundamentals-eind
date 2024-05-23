import requests
import sys


def handle_api_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Er is iets fout gegaan: {response.status_code}")
        if response.status_code == 404:
            print("Kan deze Pokemon niet vinden probeer het opnieuw")
        main()


def get_api_data(url):
    response = requests.get(url)
    return handle_api_response(response)


def get_pokemon(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    pokemon_data = get_api_data(url)

    abilities = [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
    types = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
    print(f"Name: {pokemon_data['name']}")
    print(f"Abilities: {', '.join(abilities)}")
    print(f"Type: {', '.join(types)}")


def get_pokemon_evolution(pokemon_evolution_name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_evolution_name}/"
    species_data = get_api_data(url)
    evolution_chain_url = species_data['evolution_chain']['url']
    evolution_chain_data = get_api_data(evolution_chain_url)
    return evolution_chain_data


def get_pokemon_moves(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    pokemon_data = get_api_data(url)
    moves = [move["move"]["name"] for move in pokemon_data["moves"]]
    print("Moves:")
    for move in moves:
        print(move)


def add_to_favorites(pokemon_name):
    with open("favorites.txt", "r") as file:
        favorites = file.readlines()

    if pokemon_name.strip() in [favorite.strip() for favorite in favorites]:
        print(f"{pokemon_name} is al als favoriet opgeslagen.")
    else:
        answer = input(f"wil je {pokemon_name} als favoriet opslaan? (ja/nee): ").lower().strip()
        if answer == "ja":
            with open("favorites.txt", "a") as file:
                file.write(f"{pokemon_name}\n")
            print(f"{pokemon_name} is toegevoegd aan favorieten!")
        else:
            print("De Pokemon is niet aan favorieten toegevoegd.")


def view_favorites():
    with open("favorites.txt", "r") as file:
        favorites = file.readlines()
        if favorites:
            print("Favoriete Pokemon:")
            for index, favorite in enumerate(favorites):
                print(f"{index + 1}. {favorite.strip()}")
        else:
            print("er zijn geen favorieten gevonden.")
            print("Als er geen favorieten zijn gevonden kies dan 'nee'")


def remove_from_favorites():
    view_favorites()
    pokemon_index = int(input("Geef het nummer van de Pokemon die je wilt verwijderen uit je favorieten: ")) - 1

    with open("favorites.txt", "r") as file:
        favorites = file.readlines()

    removed_pokemon = favorites.pop(pokemon_index).strip()

    with open("favorites.txt", "w") as file:
        for favorite in favorites:
            file.write(favorite)

    print(f"{removed_pokemon} is verwijderd uit favorieten.")


def get_more_info(pokemon_name):
    answer = input("Wil je nog iets weten over deze Pokemon of je favorieten bewerken? (ja/nee): ").lower().strip()
    if answer == "ja":
        info = input(
            "Wat wil je nog weten?\n1. Evolutie\n2. Moves\n3. Favorieten opties\nKies een optie (1/2/3): ").strip()
        if info == "1":
            evolution_chain_data = get_pokemon_evolution(pokemon_name)
            if evolution_chain_data:
                print("EvolutieChain:")
                chain = evolution_chain_data['chain']
                pokemon_list = []
                while chain:
                    pokemon_list.append(chain['species']['name'])
                    print(chain['species']['name'])
                    if chain['evolves_to']:
                        chain = chain['evolves_to'][0]
                    else:
                        chain = None
                add_to_favorites(pokemon_name)
            else:
                print(f"Geen informatie gevonden over de evolutie van {pokemon_name}")
        elif info == "2":
            get_pokemon_moves(pokemon_name)
            add_to_favorites(pokemon_name)
        elif info == "3":
            favo_option = input(
                "Wat wil je doen met je favorieten?\n1. Favorieten bekijken\n2. Favoriet verwijderen\n3. Toevoegen als favoriet\nKies een optie (1/2/3): ").lower().strip()
            if favo_option == "1":
                view_favorites()
            elif favo_option == "2":
                remove_from_favorites()
            elif favo_option == "3":
                add_to_favorites(pokemon_name)
            else:
                print("Ongeldige keuze.")
        else:
            print("Ongeldige keuze.")


def main():
    while True:
        choice = input("Wil je een Pokemon opzoeken of je favorieten bekijken? (pokemon/favorieten): ").lower().strip()
        if choice == "favorieten":
            view_favorites()
            change_favorites = input("Wil je je favorieten aanpassen? (ja/nee): ").lower().strip()
            if change_favorites == "ja":
                remove_from_favorites()
        elif choice == "pokemon":
            while True:
                users_pokemon = input("Type de naam van een Pokemon: ").lower().strip()
                get_pokemon(users_pokemon)
                get_more_info(users_pokemon)

                another_search = input(
                    "Wil je nog een Pokemon opzoeken of je favorieten willen bekijken? (pokemon/favorieten): ").lower().strip()
                if another_search == "favorieten":
                    nice_var_name = input(
                        "Wil je je favorieten nog inzien of aanpassen? kies\n1. voor het bekijken van je favorieten\n2. voor het verwijderen van een van je favorieten: ").lower().strip()
                    if nice_var_name == "1":
                        view_favorites()
                    elif nice_var_name == "2":
                        remove_from_favorites()
                elif another_search != "pokemon":
                    break
        else:
            print("Ongeldige keuze. Probeer het opnieuw.")


if __name__ == "__main__":
    main()
