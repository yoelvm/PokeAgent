from __future__ import annotations

import math

from pokeagent.natures import get_nature_modifier
from pokeagent.models import Pokemon, StatTraining


def calculate_hp(
    base_stat: int,
    iv: int,
    ev: int,
    level: int,
 ) -> int:
    """Calculate a Pokémon HP stat."""
    return (
        math.floor(
            (
                (
                    2 * base_stat
                    + iv
                    + math.floor(ev / 4)
                )
                * level
            )
            / 100
        )
        + level
        + 10
    )

def calculate_stat(
    base_stat: int,
    iv: int,
    ev: int,
    level: int,
    nature: str,
    stat_name: str,
 ) -> int:
    """Calculate a non-HP Pokémon stat."""
    base_value = (
        math.floor(
            (
                (
                    2 * base_stat
                    + iv
                    + math.floor(ev / 4)
                )
                * level
            )
            / 100
        )
        + 5
    )

    nature_modifier = get_nature_modifier(
        nature,
        stat_name,
    )

    return math.floor(
        base_value * nature_modifier
    )

def calculate_pokemon_stats(
    pokemon: Pokemon,
    training: StatTraining,
    level: int,
    nature: str,
 ) -> dict[str, int]:
    """Calculate all final stats for a Pokémon."""
    training.validate()

    if level < 1 or level > 100:
        raise ValueError(
            "Level must be between 1 and 100."
        )

    calculated: dict[str, int] = {}

    for stat_name, base_stat in pokemon.stats.items():
        iv = training.ivs.get(
            stat_name,
            31,
        )

        ev = training.evs.get(
            stat_name,
            0,
        )

        if stat_name == "hp":
            calculated[stat_name] = calculate_hp(
                base_stat,
                iv,
                ev,
                level,
            )

        else:
            calculated[stat_name] = calculate_stat(
                base_stat,
                iv,
                ev,
                level,
                nature,
                stat_name,
            )

    return calculated