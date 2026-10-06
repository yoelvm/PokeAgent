from __future__ import annotations

from pokeagent.api import get_ability
from pokeagent.models import Ability


class AbilityService:
    """Provide Pokémon ability operations."""

    def find_ability(
        self,
        name_or_id: str | int,
    ) -> Ability:
        """Find an ability by name or PokéAPI ID."""
        data = get_ability(name_or_id)

        return Ability.from_dict(data)