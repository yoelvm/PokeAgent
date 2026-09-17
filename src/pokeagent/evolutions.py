from __future__ import annotations

from typing import Any

from pokeagent.api import (
    get_evolution_chain,
    get_pokemon_species,
)


KANTO_LAST_ID = 151


def get_species_id(species_url: str) -> int:
    """Extract a National Pokédex ID from a species URL."""
    return int(species_url.rstrip("/").split("/")[-1])


def extract_evolution_species(
    node: dict[str, Any],
) -> list[tuple[int, str]]:
    """Recursively extract IDs and names from an evolution chain."""
    species = node["species"]

    pokemon = [
        (
            get_species_id(species["url"]),
            species["name"],
        )
    ]

    for evolution in node["evolves_to"]:
        pokemon.extend(
            extract_evolution_species(evolution)
        )

    return pokemon


def get_evolution_names(
    name_or_id: str | int,
    max_species_id: int | None = None,
) -> list[str]:
    """Return species names in a Pokémon evolution chain."""
    species = get_pokemon_species(name_or_id)

    chain_url = species["evolution_chain"]["url"]
    chain = get_evolution_chain(chain_url)

    evolution_species = extract_evolution_species(
        chain["chain"]
    )

    if max_species_id is not None:
        evolution_species = [
            (species_id, name)
            for species_id, name in evolution_species
            if species_id <= max_species_id
        ]

    return [
        name
        for _, name in evolution_species
    ]


def get_kanto_evolution_names(
    name_or_id: str | int,
) -> list[str]:
    """Return only Kanto species from an evolution chain."""
    return get_evolution_names(
        name_or_id,
        max_species_id=KANTO_LAST_ID,
    )