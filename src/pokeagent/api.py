from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://pokeapi.co/api/v2"
DEFAULT_TIMEOUT = 10


class PokeAPIError(RuntimeError):
    """Raised when a PokéAPI request cannot be completed."""


def get_pokemon(name_or_id: str | int) -> dict[str, Any]:
    """Get raw Pokémon data from PokéAPI."""
    identifier = "-".join(
    str(name_or_id).strip().lower().split()
    )

    if not identifier:
        raise ValueError("Pokemon name or ID cannot be empty.")

    url = f"{BASE_URL}/pokemon/{identifier}"

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 404:
            raise PokeAPIError(f"Pokemon '{name_or_id}' was not found.")

        response.raise_for_status()
        return response.json()

    except PokeAPIError:
        raise
    except requests.Timeout as exc:
        raise PokeAPIError("PokéAPI request timed out.") from exc
    except requests.RequestException as exc:
        raise PokeAPIError(f"PokéAPI request failed: {exc}") from exc
def get_pokemon_species(name_or_id: str | int) -> dict[str, Any]:
    """Get Pokémon species data from PokéAPI."""
    identifier = str(name_or_id).strip().lower()

    if not identifier:
        raise ValueError("Pokemon name or ID cannot be empty.")

    url = f"{BASE_URL}/pokemon-species/{identifier}"

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 404:
            raise PokeAPIError(
                f"Pokemon species '{name_or_id}' was not found."
            )

        response.raise_for_status()
        return response.json()

    except PokeAPIError:
        raise
    except requests.Timeout as exc:
        raise PokeAPIError("PokéAPI request timed out.") from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc
def get_evolution_chain(chain_url: str) -> dict[str, Any]:
    """Get an evolution chain from PokéAPI."""
    if not chain_url:
        raise ValueError("Evolution chain URL cannot be empty.")

    try:
        response = requests.get(chain_url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()

    except requests.Timeout as exc:
        raise PokeAPIError("PokéAPI request timed out.") from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc
def get_pokemon_list(limit: int = 20, offset: int = 0) -> dict[str, Any]:
    """Get a paginated list of Pokémon from PokéAPI."""
    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    if offset < 0:
        raise ValueError("Offset cannot be negative.")

    url = f"{BASE_URL}/pokemon"
    params = {
        "limit": limit,
        "offset": offset,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    except requests.Timeout as exc:
        raise PokeAPIError("PokéAPI request timed out.") from exc
    except requests.RequestException as exc:
        raise PokeAPIError(f"PokéAPI request failed: {exc}") from exc
def get_type(name_or_id: str | int) -> dict[str, Any]:
    """Get Pokémon type data from PokéAPI."""
    identifier = str(name_or_id).strip().lower()

    if not identifier:
        raise ValueError("Type name or ID cannot be empty.")

    url = f"{BASE_URL}/type/{identifier}"

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 404:
            raise PokeAPIError(
                f"Pokemon type '{name_or_id}' was not found."
            )

        response.raise_for_status()
        return response.json()

    except PokeAPIError:
        raise
    except requests.Timeout as exc:
        raise PokeAPIError("PokéAPI request timed out.") from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc     
def get_move(name_or_id: str | int) -> dict[str, Any]:
    """Get Pokémon move data from PokéAPI."""
    identifier = "-".join(
     str(name_or_id).strip().lower().split()
    )

    if not identifier:
        raise ValueError("Move name or ID cannot be empty.")

    url = f"{BASE_URL}/move/{identifier}"

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 404:
            raise PokeAPIError(
                f"Pokemon move '{name_or_id}' was not found."
            )

        response.raise_for_status()
        return response.json()

    except PokeAPIError:
        raise
    except requests.Timeout as exc:
        raise PokeAPIError("PokéAPI request timed out.") from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc
def get_item(name_or_id: str | int) -> dict[str, Any]:
    """Get Pokémon item data from PokéAPI."""
    identifier = "-".join(
    str(name_or_id).strip().lower().split()
    )

    if not identifier:
        raise ValueError("Item name or ID cannot be empty.")

    url = f"{BASE_URL}/item/{identifier}"

    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 404:
            raise PokeAPIError(
                f"Pokemon item '{name_or_id}' was not found."
            )

        response.raise_for_status()
        return response.json()

    except PokeAPIError:
        raise
    except requests.Timeout as exc:
        raise PokeAPIError("PokéAPI request timed out.") from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc
def get_ability(name_or_id: str | int) -> dict[str, Any]:
    """Get Pokémon ability data from PokéAPI."""
    identifier = "-".join(
        str(name_or_id).strip().lower().split()
    )

    if not identifier:
        raise ValueError("Ability name or ID cannot be empty.")

    url = f"{BASE_URL}/ability/{identifier}"

    try:
        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
        )

        if response.status_code == 404:
            raise PokeAPIError(
                f"Pokemon ability '{name_or_id}' was not found."
            )

        response.raise_for_status()
        return response.json()

    except PokeAPIError:
        raise
    except requests.Timeout as exc:
        raise PokeAPIError(
            "PokéAPI request timed out."
        ) from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc
def get_version_group(name_or_id: str | int) -> dict[str, Any]:
    """Get Pokémon version-group data from PokéAPI."""
    identifier = "-".join(
        str(name_or_id).strip().lower().split()
    )

    if not identifier:
        raise ValueError(
            "Version group name or ID cannot be empty."
        )

    url = f"{BASE_URL}/version-group/{identifier}"

    try:
        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
        )

        if response.status_code == 404:
            raise PokeAPIError(
                f"Version group '{name_or_id}' was not found."
            )

        response.raise_for_status()
        return response.json()

    except PokeAPIError:
        raise
    except requests.Timeout as exc:
        raise PokeAPIError(
            "PokéAPI request timed out."
        ) from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc
def get_pokemon_version_names(
    name_or_id: str | int,
 ) -> list[str]:
    """Return version names where a Pokémon appears."""
    data = get_pokemon(name_or_id)

    return [
        entry["version"]["name"]
        for entry in data.get("game_indices", [])
    ]
def get_pokemon_species_list() -> list[dict[str, Any]]:
    """Return the complete Pokémon species index from PokéAPI."""
    url = f"{BASE_URL}/pokemon-species"

    try:
        count_response = requests.get(
            url,
            params={"limit": 1},
            timeout=DEFAULT_TIMEOUT,
        )

        count_response.raise_for_status()

        count = count_response.json()["count"]

        response = requests.get(
            url,
            params={
                "limit": count,
                "offset": 0,
            },
            timeout=DEFAULT_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()["results"]

    except requests.Timeout as exc:
        raise PokeAPIError(
            "PokéAPI request timed out."
        ) from exc
    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc
def get_generation(
    name_or_id: str | int,
 ) -> dict[str, Any]:
    """Get Pokémon generation data from PokéAPI."""
    identifier = "-".join(
        str(name_or_id).strip().lower().split()
    )

    if not identifier:
        raise ValueError(
            "Generation name or ID cannot be empty."
        )

    url = f"{BASE_URL}/generation/{identifier}"

    try:
        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
        )

        if response.status_code == 404:
            raise PokeAPIError(
                f"Generation '{name_or_id}' was not found."
            )

        response.raise_for_status()

        return response.json()

    except PokeAPIError:
        raise

    except requests.Timeout as exc:
        raise PokeAPIError(
            "PokéAPI request timed out."
        ) from exc

    except requests.RequestException as exc:
        raise PokeAPIError(
            f"PokéAPI request failed: {exc}"
        ) from exc