from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://pokeapi.co/api/v2"
DEFAULT_TIMEOUT = 10


class PokeAPIError(RuntimeError):
    """Raised when a PokéAPI request cannot be completed."""


def get_pokemon(name_or_id: str | int) -> dict[str, Any]:
    """Get raw Pokémon data from PokéAPI."""
    identifier = str(name_or_id).strip().lower()

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