from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pokeagent.api import get_pokemon


KANTO_FIRST_ID = 1
KANTO_LAST_ID = 151

DATA_DIR = Path("data")
KANTO_DATA_FILE = DATA_DIR / "kanto.json"


def get_kanto_pokemon() -> list[dict[str, Any]]:
    """Download the 151 original Kanto Pokémon."""
    pokemon_list = []

    for pokemon_id in range(KANTO_FIRST_ID, KANTO_LAST_ID + 1):
        pokemon = get_pokemon(pokemon_id)
        pokemon_list.append(pokemon)

    return pokemon_list


def simplify_pokemon(pokemon: dict[str, Any]) -> dict[str, Any]:
    """Keep the Pokédex information needed by PokeAgent."""
    return {
        "id": pokemon["id"],
        "name": pokemon["name"],
        "height": pokemon["height"],
        "weight": pokemon["weight"],
        "base_experience": pokemon["base_experience"],
        "types": [
            item["type"]["name"]
            for item in pokemon["types"]
        ],
        "abilities": [
            item["ability"]["name"]
            for item in pokemon["abilities"]
        ],
        "stats": {
            item["stat"]["name"]: item["base_stat"]
            for item in pokemon["stats"]
        },
    }


def save_kanto_pokedex() -> Path:
    """Download and save the Kanto Pokédex as JSON."""
    pokemon_list = get_kanto_pokemon()

    pokedex = [
        simplify_pokemon(pokemon)
        for pokemon in pokemon_list
    ]

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with KANTO_DATA_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            pokedex,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return KANTO_DATA_FILE