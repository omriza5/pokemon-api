from file_handler import FileHandler

import json
from typing import List, Dict

class PokemonJsonDB:
    def __init__(self,filename='pokemon_db.json') -> None:
        self.filename = filename
        self.file_handler = FileHandler(self.filename)
        
    def load_collection(self) -> List[Dict]:
        try:
            data = self.file_handler.read_from_file()
            return json.loads(data) if data else  []
        except json.JSONDecodeError:
            print("Error parsing JSON data")
            return []
        
    def save_pokemon(self, pokemon: Dict) -> None:
        try:
            pokemons = self.load_collection()
            if not self.is_pokemon_already_exists_in_db(pokemon):     
                pokemons.append(pokemon.to_dict())
                self.file_handler.write_to_file(json.dumps(pokemons, indent=2))
                print(f"Pokémon {pokemon.name} added to the collection.")
            else:
                print(f"Pokémon {pokemon.name} already exists in the collection.")
        except Exception as e:
            print(f"Error while saving Pokémon: {e}")
    
    def get_pokemon_by_name(self,name):
        pokemons = self.load_collection()
        for pokemon in pokemons:
            if pokemon['name'].lower() == name.lower():
                return pokemon
        return None
        
    def is_pokemon_already_exists_in_db(self,pokemon_name: Dict) -> bool:
        pokemons = self.load_collection()

        for record in pokemons:
            if record['name'] == pokemon_name:
                return True
        return False
