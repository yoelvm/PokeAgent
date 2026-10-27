from __future__ import annotations

from pokeagent.api import (
    get_pokemon_version_names,
    get_version_group,
)
from pokeagent.models import GameVersionGroup


class GameDataService:
    """Provide Pokémon game and version-group operations."""

    def find_version_group(
        self,
        name_or_id: str | int,
     ) -> GameVersionGroup:
        """Find a version group by name or PokéAPI ID."""
        data = get_version_group(name_or_id)

        return GameVersionGroup.from_dict(data)
    def contains_version(
        self,
        version_group: GameVersionGroup,
        version_name: str,
     ) -> bool:
        """Return whether a version belongs to a version group."""
        normalized_version = (
            version_name.strip().lower().replace(" ", "-")
        )

        return normalized_version in version_group.versions
    def is_pokemon_available(
        self,
        pokemon_query: str | int,
        version_group_query: str | int,
     ) -> bool:
        """Return whether a Pokémon appears in a version group."""
        version_group = self.find_version_group(
            version_group_query
        )

        pokemon_versions = set(
            get_pokemon_version_names(
                pokemon_query
            )
        )

        return any(
            version in pokemon_versions
            for version in version_group.versions
        )