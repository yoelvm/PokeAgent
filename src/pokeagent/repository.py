from __future__ import annotations

import json
from pathlib import Path

from pokeagent.models import Pokemon


DEFAULT_POKEDEX_FILE = Path("data/kanto.json")


class PokemonRepository:
    """Load and query Pokémon from the local Pokédex."""

    def __init__(self, data_file: Path = DEFAULT_POKEDEX_FILE) -> None:
        self.data_file = data_file
        self._pokemon = self._load_pokemon()

    def _load_pokemon(self) -> list[Pokemon]:
        """Load Pokémon from the JSON Pokédex file."""
        with self.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            Pokemon.from_dict(item)
            for item in data
        ]

    def get_all(self) -> list[Pokemon]:
        """Return all Pokémon in the Pokédex."""
        return self._pokemon.copy()
    def get_by_id(self, pokemon_id: int) -> Pokemon | None:
        """Return a Pokémon by Pokédex ID."""
        for pokemon in self._pokemon:
            if pokemon.id == pokemon_id:
                return pokemon

        return None

    def get_by_name(self, name: str) -> Pokemon | None:
        """Return a Pokémon by name."""
        normalized_name = name.strip().lower()

        for pokemon in self._pokemon:
            if pokemon.name == normalized_name:
                return pokemon

        return None