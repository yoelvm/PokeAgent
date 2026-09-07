from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Pokemon:
    """Represent a Pokémon stored in the local Pokédex."""

    id: int
    name: str
    height: int
    weight: int
    base_experience: int | None
    types: list[str]
    abilities: list[str]
    stats: dict[str, int]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Pokemon:
        """Create a Pokémon from Pokédex JSON data."""
        return cls(
            id=data["id"],
            name=data["name"],
            height=data["height"],
            weight=data["weight"],
            base_experience=data["base_experience"],
            types=data["types"],
            abilities=data["abilities"],
            stats=data["stats"],
        )
    @property
    def height_m(self) -> float:
        """Return the Pokémon height in metres."""
        return self.height / 10

    @property
    def weight_kg(self) -> float:
        """Return the Pokémon weight in kilograms."""
        return self.weight / 10