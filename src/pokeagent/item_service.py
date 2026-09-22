from __future__ import annotations

from pokeagent.api import get_item
from pokeagent.models import Item


class ItemService:
    """Provide Pokémon item operations."""

    def find_item(
        self,
        name_or_id: str | int,
    ) -> Item:
        """Find an item by name or PokéAPI ID."""
        data = get_item(name_or_id)

        return Item.from_dict(data)