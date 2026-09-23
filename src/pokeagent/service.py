from __future__ import annotations

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

    def find_pokemon(self, query: str | int) -> Pokemon | None:
        """Find a Pokémon by Pokédex ID or name."""
        if isinstance(query, int):
            return self.repository.get_by_id(query)

        normalized_query = "-".join(
          str(query).strip().lower().replace(".", "").split()
        )

        if normalized_query.isdigit():
            return self.repository.get_by_id(int(normalized_query))

        return self.repository.get_by_name(normalized_query)

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
