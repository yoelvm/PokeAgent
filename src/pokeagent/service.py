from __future__ import annotations

from pokeagent.api import (
    get_generation,
    get_type,
)
from pokeagent.models import Pokemon
from pokeagent.repository import PokemonRepository
from pokeagent.type_effectiveness import (
    get_type_effectiveness as calculate_type_effectiveness,
)

VALID_STATS = {
    "hp",
    "attack",
    "defense",
    "special-attack",
    "special-defense",
    "speed",
}


class PokedexService:
    """Provide Pokédex search operations."""

    def __init__(self, repository: PokemonRepository | None = None) -> None:
        self.repository = repository or PokemonRepository()

    def find_pokemon(
        self,
        query: str | int,
     ) -> Pokemon | None:
        """Find a Pokémon by name or National Pokédex ID."""
        normalized_query = "-".join(
            str(query)
            .strip()
            .lower()
            .replace(".", "")
            .split()
        )

        if not normalized_query:
            return None

        if normalized_query.isdigit():
            pokemon_id = int(
                normalized_query
            )

            if pokemon_id < 1:
                return None

            return self.repository.get_by_id(
                pokemon_id
            )

        return self.repository.get_by_name(
            normalized_query
        )

    def find_by_type(self, pokemon_type: str) -> list[Pokemon]:
        """Return all Pokémon matching a given type."""
        normalized_type = pokemon_type.strip().lower()

        return [
            pokemon
            for pokemon in self.repository.get_all()
            if normalized_type in pokemon.types
        ]
    def find_by_type_and_min_stat(
        self,
        pokemon_type: str,
        stat_name: str,
        minimum: int,
     ) -> list[Pokemon]:
        """Return Pokémon matching a type and minimum base stat."""
        normalized_type = pokemon_type.strip().lower()
        normalized_stat = stat_name.strip().lower()

        if normalized_stat not in VALID_STATS:
            raise ValueError(
                f"Unknown stat '{stat_name}'. "
                f"Valid stats are: {', '.join(sorted(VALID_STATS))}."
            )

        return [
            pokemon
            for pokemon in self.repository.get_all()
            if normalized_type in pokemon.types
            and pokemon.stats.get(normalized_stat, 0) >= minimum
        ]
    def get_type_effectiveness(
        self,
        query: str | int,
     ) -> dict[str, dict[str, float]] | None:
        """Return defensive type effectiveness for a Pokémon."""
        pokemon = self.find_pokemon(query)

        if pokemon is None:
            return None

        return calculate_type_effectiveness(
            pokemon.types
        )
    def find_by_types(
        self,
        primary_type: str,
        secondary_type: str | None = None,
     ) -> list[dict[str, int | str]]:
        """Find National Pokédex Pokémon by one or two types."""
        primary = primary_type.strip().lower()

        primary_data = get_type(
            primary
        )

        primary_names = {
            entry["pokemon"]["name"]
            for entry in primary_data["pokemon"]
        }

        matching_names = primary_names

        if secondary_type:
            secondary = secondary_type.strip().lower()

            if secondary != primary:
                secondary_data = get_type(
                    secondary
                )

                secondary_names = {
                    entry["pokemon"]["name"]
                    for entry in secondary_data["pokemon"]
                }

                matching_names = (
                    primary_names
                    & secondary_names
                )

        results = []

        for name in matching_names:
            index_entry = (
                self.repository
                .get_index_entry_by_name(name)
            )

            if index_entry is not None:
                results.append(
                    {
                        "id": index_entry["id"],
                        "name": index_entry["name"],
                    }
                )

        results.sort(
            key=lambda pokemon: pokemon["id"]
        )

        return results
    def find_by_generation(
        self,
        generation: str | int,
     ) -> list[dict[str, int | str]]:
        """Find National Pokédex Pokémon by generation."""
        data = get_generation(
            generation
        )

        results = []

        for species in data["pokemon_species"]:
            index_entry = (
                self.repository
                .get_index_entry_by_name(
                    species["name"]
                )
            )

            if index_entry is not None:
                results.append(
                    {
                        "id": index_entry["id"],
                        "name": index_entry["name"],
                    }
                )

        results.sort(
            key=lambda pokemon: pokemon["id"]
        )

        return results
