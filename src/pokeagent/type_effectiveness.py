from __future__ import annotations

from pokeagent.api import get_type


BATTLE_TYPES = [
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy",
]


def get_type_defensive_multipliers(
    pokemon_types: list[str],
 ) -> dict[str, float]:
    """Calculate incoming damage multipliers for Pokémon types."""
    multipliers = {
        attacking_type: 1.0
        for attacking_type in BATTLE_TYPES
    }

    for pokemon_type in pokemon_types:
        type_data = get_type(pokemon_type)
        relations = type_data["damage_relations"]

        for item in relations["double_damage_from"]:
            attacking_type = item["name"]

            if attacking_type in multipliers:
                multipliers[attacking_type] *= 2

        for item in relations["half_damage_from"]:
            attacking_type = item["name"]

            if attacking_type in multipliers:
                multipliers[attacking_type] *= 0.5

        for item in relations["no_damage_from"]:
            attacking_type = item["name"]

            if attacking_type in multipliers:
                multipliers[attacking_type] *= 0

    return multipliers
def classify_type_effectiveness(
    multipliers: dict[str, float],
 ) -> dict[str, dict[str, float]]:
    """Group defensive type multipliers by effectiveness."""
    weaknesses = {
        pokemon_type: multiplier
        for pokemon_type, multiplier in multipliers.items()
        if multiplier > 1
    }

    resistances = {
        pokemon_type: multiplier
        for pokemon_type, multiplier in multipliers.items()
        if 0 < multiplier < 1
    }

    immunities = {
        pokemon_type: multiplier
        for pokemon_type, multiplier in multipliers.items()
        if multiplier == 0
    }

    return {
        "weaknesses": weaknesses,
        "resistances": resistances,
        "immunities": immunities,
    }
def get_type_effectiveness(
    pokemon_types: list[str],
 ) -> dict[str, dict[str, float]]:
    """Return defensive weaknesses, resistances and immunities."""
    multipliers = get_type_defensive_multipliers(
        pokemon_types
    )

    return classify_type_effectiveness(
        multipliers
    )