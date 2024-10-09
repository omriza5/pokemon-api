import requests
import random

LIMITS=[50,100,150]
class PokemonAPI():
    base_url = 'https://pokeapi.co/api/v2/pokemon'
    
    def get_all_pokemons(self) -> list[str]:
        try:
            limit = random.choice(LIMITS)
            print(f"Fetching {limit} pokemons...")
            
            url =f'{self.base_url}?limit={limit}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return [poke['name'] for poke in data['results']]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
    
    
    def get_pokemon_details(self,name: str) -> dict:
        try:
            print(f"Getting {name}'s details...")
            url =f'{self.base_url}/{name}'
            response = requests.get(url)
            response.raise_for_status()
            return response.json()        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
        