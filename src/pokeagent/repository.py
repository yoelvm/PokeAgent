from __future__ import annotations

import json
from pathlib import Path

from pokeagent.api import get_pokemon
from pokeagent.models import Pokemon
from pokeagent.pokedex import pokemon_from_api_data


DEFAULT_POKEDEX_FILE = Path("data/kanto.json")


class PokemonRepository:
    """Repository for Pokémon data."""

    def __init__(self) -> None:
        # -----------------------------------------------------
        # LOCAL KANTO DATA
        # -----------------------------------------------------

        kanto_path = Path(
            "data/kanto.json"
        )

        with kanto_path.open(
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        self._pokemon = [
            Pokemon.from_dict(item)
            for item in data
        ]

        # -----------------------------------------------------
        # NATIONAL POKÉDEX INDEX
        # -----------------------------------------------------

        index_path = Path(
            "data/pokedex_index.json"
        )

        with index_path.open(
            encoding="utf-8"
        ) as file:
            self._pokedex_index = json.load(
                file
            )

        self._index_by_id = {
            entry["id"]: entry
            for entry in self._pokedex_index
        }

        self._index_by_name = {
            entry["name"]: entry
            for entry in self._pokedex_index
        }

        self._remote_cache: dict[int, Pokemon] = {}

    def get_all(self) -> list[Pokemon]:
        """Return all locally stored Pokémon."""
        return list(self._pokemon)

    def get_by_id(
        self,
        pokemon_id: int,
     ) -> Pokemon | None:
        """Find a Pokémon by National Pokédex ID."""
        for pokemon in self._pokemon:
            if pokemon.id == pokemon_id:
                return pokemon

        return self._get_remote_pokemon(
            pokemon_id
        )

    def get_by_name(
        self,
        name: str,
     ) -> Pokemon | None:
        """Find a Pokémon by name."""
        normalized_name = (
            name.strip()
            .lower()
            .replace(" ", "-")
        )

        for pokemon in self._pokemon:
            if pokemon.name == normalized_name:
                return pokemon

        index_entry = self._index_by_name.get(
            normalized_name
        )

        if index_entry is None:
            return None

        return self._get_remote_pokemon(
            index_entry["id"]
        )

    def get_by_type(
        self,
        pokemon_type: str,
     ) -> list[Pokemon]:
        """Return locally stored Pokémon of a type."""
        normalized_type = (
            pokemon_type.strip().lower()
        )

        return [
            pokemon
            for pokemon in self._pokemon
            if normalized_type in pokemon.types
        ]

    def _get_remote_pokemon(
        self,
        pokemon_id: int,
     ) -> Pokemon | None:
        """Load a non-local Pokémon from PokéAPI."""
        if pokemon_id in self._remote_cache:
            return self._remote_cache[
                pokemon_id
            ]

        if pokemon_id not in self._index_by_id:
            return None

        data = get_pokemon(
            pokemon_id
        )

        pokemon = pokemon_from_api_data(
            data
        )

        self._remote_cache[
            pokemon_id
        ] = pokemon

        return pokemon
    def get_index_entry_by_name(
        self,
        name: str,
     ) -> dict | None:
        """Return a lightweight National Pokédex index entry."""
        normalized_name = (
            name.strip()
            .lower()
            .replace(" ", "-")
        )

        return self._index_by_name.get(
            normalized_name
        )