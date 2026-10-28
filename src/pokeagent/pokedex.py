from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pokeagent.models import Pokemon

from pokeagent.api import get_pokemon_species_list


DATA_PATH = Path("data/pokedex_index.json")


def build_pokedex_index() -> list[dict[str, int | str]]:
    """Build a lightweight National Pokédex index."""
    species = get_pokemon_species_list()

    pokedex: list[dict[str, int | str]] = []

    for entry in species:
        species_id = int(
            entry["url"]
            .rstrip("/")
            .split("/")[-1]
        )

        pokedex.append(
            {
                "id": species_id,
                "name": entry["name"],
            }
        )

    pokedex.sort(
        key=lambda pokemon: int(
            pokemon["id"]
        )
    )

    return pokedex


def save_pokedex_index(
    path: Path = DATA_PATH,
 ) -> Path:
    """Save the National Pokédex index locally."""
    pokedex = build_pokedex_index()

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            pokedex,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return path
def pokemon_from_api_data(
    data: dict[str, Any],
 ) -> Pokemon:
    """Create a Pokemon model from raw PokéAPI data."""
    abilities = [
        entry["ability"]["name"]
        for entry in data.get("abilities", [])
    ]

    hidden_abilities = [
        entry["ability"]["name"]
        for entry in data.get("abilities", [])
        if entry.get("is_hidden", False)
    ]

    types = [
        entry["type"]["name"]
        for entry in data.get("types", [])
    ]

    stats = {
        entry["stat"]["name"]: entry["base_stat"]
        for entry in data.get("stats", [])
    }

    image_url = (
        data.get("sprites", {})
        .get("other", {})
        .get("official-artwork", {})
        .get("front_default")
    )

    if image_url is None:
        image_url = (
            data.get("sprites", {})
            .get("front_default")
        )

    return Pokemon(
        id=data["id"],
        name=data["name"],
        height=data["height"],
        weight=data["weight"],
        base_experience=data.get(
            "base_experience"
        ),
        types=types,
        abilities=abilities,
        stats=stats,
        image_url=image_url,
        evolutions=[],
        hidden_abilities=hidden_abilities,
    )