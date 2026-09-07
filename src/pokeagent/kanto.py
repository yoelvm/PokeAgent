from __future__ import annotations

from typing import Any

from pokeagent.api import get_pokemon


KANTO_FIRST_ID = 1
KANTO_LAST_ID = 151


def get_kanto_pokemon() -> list[dict[str, Any]]:
    """Download the 151 original Kanto Pokémon."""
    pokemon_list = []

    for pokemon_id in range(KANTO_FIRST_ID, KANTO_LAST_ID + 1):
        pokemon = get_pokemon(pokemon_id)
        pokemon_list.append(pokemon)

    return pokemon_list