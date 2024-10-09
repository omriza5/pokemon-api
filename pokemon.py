from typing import Dict,Self

class Pokemon:
    def __init__(self,id: str,name: str,abilities: list[str]) -> None:
        self.id = id
        self.name = name
        self.abilities = abilities
    
    
    def to_dict(self) -> Self:
        return {
            'id': self.id,
            'name': self.name,
            'abilities': self.abilities
        }
    
    @classmethod
    def from_api(cls, data: Dict) -> 'Pokemon':
        id = data['id']
        name = data['name']
        abilities = [ability['ability']['name'] for ability in data['abilities']]
        return cls(id, name, abilities)
    
    @classmethod
    def from_json(cls, data: Dict) -> 'Pokemon':
        return cls(data['id'], data['name'], data['abilities'])
    
    def __str__(self):
        return f"Pokémon {self.name} (ID: {self.id}), Abilities: {', '.join(self.abilities)}"
    