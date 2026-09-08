from __future__ import annotations

from pokeagent.models import Pokemon
from pokeagent.service import PokedexService


def format_label(value: str) -> str:
    """Convert API-style names into readable labels."""
    return value.replace("-", " ").title()


def format_pokemon(pokemon: Pokemon) -> str:
    """Format a Pokémon as a readable Pokédex entry."""
    types = ", ".join(
        format_label(pokemon_type)
        for pokemon_type in pokemon.types
    )

    abilities = ", ".join(
        format_label(ability)
        for ability in pokemon.abilities
    )

    stats = "\n".join(
        f"  {format_label(name)}: {value}"
        for name, value in pokemon.stats.items()
    )

    return (
        f"\n#{pokemon.id:03d} {format_label(pokemon.name)}\n"
        f"Type: {types}\n"
        f"Height: {pokemon.height_m} m\n"
        f"Weight: {pokemon.weight_kg} kg\n"
        f"Abilities: {abilities}\n"
        f"Base stats:\n{stats}\n"
    )


def main() -> None:
    """Run the interactive Kanto Pokédex."""
    service = PokedexService()

    print("PokeAgent - Kanto Pokedex")
    print("Search by Pokemon name or Pokedex number.")
    print("Type 'q' to quit.\n")

    while True:
        query = input("Search Pokemon: ").strip()

        if query.lower() in {"q", "quit", "exit"}:
            print("Goodbye!")
            break

        if not query:
            print("Please enter a Pokemon name or number.\n")
            continue

        pokemon = service.find_pokemon(query)

        if pokemon is None:
            print(
                f"No Pokemon matching '{query}' "
                "was found in the Kanto Pokedex.\n"
            )
            continue

        print(format_pokemon(pokemon))


if __name__ == "__main__":
    main()