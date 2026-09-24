from __future__ import annotations

from dataclasses import dataclass, field
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
    image_url: str | None = None
    evolutions: list[str] = field(default_factory=list)

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
            image_url=data.get("image_url"),
            evolutions=data.get("evolutions", []),
        )

    @property
    def height_m(self) -> float:
        """Return the Pokémon height in metres."""
        return self.height / 10

    @property
    def weight_kg(self) -> float:
        """Return the Pokémon weight in kilograms."""
        return self.weight / 10
@dataclass
class Move:
    """Represent a Pokémon move."""

    id: int
    name: str
    type: str
    power: int | None
    accuracy: int | None
    pp: int | None
    damage_class: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Move:
        """Create a move from PokéAPI data."""
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"]["name"],
            power=data["power"],
            accuracy=data["accuracy"],
            pp=data["pp"],
            damage_class=data["damage_class"]["name"],
        )
@dataclass
class LearnsetEntry:
    """Represent how a Pokémon learns a move in a game version group."""

    move_name: str
    version_group: str
    method: str
    level_learned_at: int
@dataclass
class LearnsetMove:
    """Represent a move together with how a Pokémon learns it."""

    move: Move
    version_group: str
    method: str
    level_learned_at: int
@dataclass
class Item:
    """Represent a Pokémon item."""

    id: int
    name: str
    category: str
    effect: str
    image_url: str | None
    prices: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Item:
        """Create an item from PokéAPI data."""
        english_effect = next(
            (
                entry["short_effect"]
                for entry in data.get("effect_entries", [])
                if entry["language"]["name"] == "en"
            ),
            "",
        )

        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"]["name"],
            effect=english_effect,
            image_url=data.get("sprites", {}).get("default"),
            prices=data.get("prices", []),
        )
@dataclass
class Team:
    """Represent a Pokémon team."""

    members: list[Pokemon] = field(default_factory=list)

    @property
    def is_full(self) -> bool:
        """Return whether the team already has six Pokémon."""
        return len(self.members) >= 6

    def add(self, pokemon: Pokemon) -> bool:
        """Add a Pokémon if the team is not full."""
        if self.is_full:
            return False

        if any(member.id == pokemon.id for member in self.members):
            return False

        self.members.append(pokemon)
        return True

    def remove(self, pokemon_id: int) -> bool:
        """Remove a Pokémon from the team by Pokédex ID."""
        for index, member in enumerate(self.members):
            if member.id == pokemon_id:
                del self.members[index]
                return True

        return False

    def clear(self) -> None:
        """Remove all Pokémon from the team."""
        self.members.clear()
    