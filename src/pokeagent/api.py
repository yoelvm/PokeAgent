from __future__ import annotations

import requests

BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon(name_or_id: str | int) -> dict:
    """Get raw Pokémon data from PokéAPI."""
    url = f"{BASE_URL}/pokemon/{name_or_id}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()