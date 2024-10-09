from pokemon import Pokemon
from pokemon_json_db import PokemonJsonDB
from pokemon_api import PokemonAPI

from typing import List,Dict
from termcolor import colored
import time
import random 


NO='n'

class PokemonApp(): 
    def __init__(self):
        self.pokemon_api = PokemonAPI()
        self.pokemons_db = PokemonJsonDB() 

    def run(self):
        while True:
            try:
                choice = self.get_user_choice()
                
                if choice == NO:
                    self.farewell_greeting()
                    return
                        
                pokemons = self.get_pokemons_from_api()
                pokemon = self.pick_random_pokemon(pokemons)
                
                requested_pokemon ={}
                if self.pokemons_db.is_pokemon_already_exists_in_db(pokemon):
                    requested_pokemon = self.pokemons_db.get_pokemon_by_name(pokemon)
                    requested_pokemon = Pokemon.from_json(requested_pokemon)
                else:
                    requested_pokemon = self.pokemon_api.get_pokemon_details(pokemon)
                    requested_pokemon = Pokemon.from_api(requested_pokemon)
                    self.pokemons_db.save_pokemon(requested_pokemon)
            
                self.display_pokemon(requested_pokemon)     
            except Exception as e:
                print("ERROR: ",e)
                return
            
            
    def get_pokemons_from_db(self) -> List[Dict]:
        return self.pokemons_db.load_collection()
    
    def get_pokemons_from_api(self) -> list[str]:
        return self.pokemon_api.get_all_pokemons()
    
    def display_pokemon(self,pokemon)-> None:
        pokemon_id = colored(f"ID: {pokemon.id}", 'cyan', attrs=['bold'])
        pokemon_name = colored(f"Name: {pokemon.name.capitalize()}", 'yellow', attrs=['bold', 'underline'])
        abilities_title = colored("Abilities:", 'green', attrs=['bold'])
    
        abilities = ', '.join([colored(ability, 'magenta') for ability in pokemon.abilities])

        fancy_line = colored("*" * 50, 'green', attrs=['bold', 'blink'])

        print(f'\n{fancy_line}')
        print(f"{pokemon_id}\n{pokemon_name}\n{abilities_title} {abilities}")
        print(f'{fancy_line}')
        
    
    def pick_random_pokemon(self,pokemons) -> str:
        return random.choice(pokemons)
    
    
    def get_user_choice(self):
        valid_choices = ['y','n']
        
        while True:
            choice = input('Whould you like to draw a Pokemon? (y/n): ').lower()
            if choice in valid_choices:
                return choice
            
    def farewell_greeting(self):
        fancy_line = colored("*" * 50, 'cyan', attrs=['bold', 'blink'])
        greeting_line = colored("★ Farewell, may your journey be bright and your heart full ★", 'yellow', attrs=['bold', 'underline', 'blink'])
        see_you_line = colored("☆ See you again soon! ☆", 'magenta', attrs=['bold', 'underline'])
        heart_symbol = colored("❤", 'red', attrs=['bold', 'blink'])
        
        print(fancy_line)
        time.sleep(0.5)  
        print(greeting_line)
        time.sleep(0.5)
        print(see_you_line)
        time.sleep(0.5)
        print(heart_symbol * 25)  
        print(fancy_line)
                
            
            