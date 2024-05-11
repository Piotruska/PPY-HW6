import requests

def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_pokemon_abilities():
    url = "https://pokeapi.co/api/v2/ability"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        abilities = [ability['name'] for ability in data['results']]
        return abilities
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def get_pokemon_moves(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        moves = [move['move']['name'] for move in data['moves']]
        return moves
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def get_pokemon_types():
    url = "https://pokeapi.co/api/v2/type"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        types = [type_info['name'] for type_info in data['results']]
        return types
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def get_pokemon_of_type(pokemon_type):
    url = f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pokemon_names = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
        return pokemon_names
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def display_pokemon_info(pokemon_info):
    print("\nPokémon Information:")
    print(f"Name: {pokemon_info['name'].capitalize()}")
    print(f"Height: {pokemon_info['height']}")
    print(f"Weight: {pokemon_info['weight']}")
    print("Abilities:")
    for ability in pokemon_info['abilities']:
        print(f"- {ability['ability']['name']}")

def main_menu():
    print("\nWelcome to the Pokémon Information System!")
    print("Please select an option:")
    print("1. Get Pokémon Information")
    print("2. Get Pokémon Abilities")
    print("3. Get Pokémon Moves")
    print("4. Get Pokémon Types")
    print("5. Get Pokémon of a Specific Type")
    print("6. Exit")


while True:
    main_menu()
    choice = input("Enter your choice: ")
    if choice == '1':
        pokemon_name = input("Enter the Pokémon name: ")
        pokemon_info = get_pokemon_info(pokemon_name)
        if pokemon_info:
            display_pokemon_info(pokemon_info)
    elif choice == '2':
        abilities = get_pokemon_abilities()
        if abilities:
            print("\nPokémon Abilities:")
            for ability in abilities:
                print(ability)
    elif choice == '3':
        pokemon_name = input("Enter the Pokémon name: ")
        moves = get_pokemon_moves(pokemon_name)
        if moves:
            print("\nPokémon Moves:")
            for move in moves:
                print(move)
    elif choice == '4':
        types = get_pokemon_types()
        if types:
            print("\nPokémon Types:")
            for type_name in types:
                print(type_name)
    elif choice == '5':
        pokemon_type = input("Enter the Pokémon type: ")
        pokemon_of_type = get_pokemon_of_type(pokemon_type)
        if pokemon_of_type:
            print(f"\nPokémon of Type {pokemon_type.capitalize()}:")
            for pokemon_name in pokemon_of_type:
                print(pokemon_name.capitalize())
    elif choice == '6':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
