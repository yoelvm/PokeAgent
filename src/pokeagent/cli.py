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
        if query.lower() in {"help", "h", "?"}:
            print(
                "\nAvailable commands:\n"
                "  <name>                         Search by Pokemon name\n"
                "  <number>                       Search by Pokedex number\n"
                "  type <type>                    List Pokemon by type\n"
                "  stat <type> <stat> <minimum>   Filter by type and base stat\n"
                "  help                           Show this help\n"
                "  q                              Quit PokeAgent\n"
            )
            continue

        if query.lower() in {"q", "quit", "exit"}:
            print("Goodbye!")
            break

        if not query:
            print("Please enter a Pokemon name or number.\n")
            continue
        if query.lower().startswith("type "):
            pokemon_type = query[5:].strip()

            if not pokemon_type:
                print("Please enter a Pokemon type.\n")
                continue

            pokemon_list = service.find_by_type(pokemon_type)

            if not pokemon_list:
                print(
                    f"No Pokemon of type '{pokemon_type}' "
                    "were found in the Kanto Pokedex.\n"
                )
                continue

            print(
                f"\nPokemon of type "
                f"{format_label(pokemon_type)}:"
            )

            for pokemon in pokemon_list:
                print(
                    f"  #{pokemon.id:03d} "
                    f"{format_label(pokemon.name)}"
                )

            print()
            continue
        if query.lower().startswith("stat "):
            parts = query.split()

            if len(parts) != 4:
                print(
                    "Usage: stat <type> <stat> <minimum>\n"
                    "Example: stat electric speed 120\n"
                )
                continue

            _, pokemon_type, stat_name, minimum_text = parts

            try:
                minimum = int(minimum_text)
            except ValueError:
                print("Minimum stat must be a number.\n")
                continue

            try:
                pokemon_list = service.find_by_type_and_min_stat(
                    pokemon_type,
                    stat_name,
                    minimum,
                )
            except ValueError as exc:
                print(f"{exc}\n")
                continue

            if not pokemon_list:
                print(
                    f"No Pokemon matched type '{pokemon_type}' "
                    f"with {stat_name} >= {minimum}.\n"
                )
                continue

            print(
                f"\nPokemon of type {format_label(pokemon_type)} "
                f"with {format_label(stat_name)} >= {minimum}:"
            )

            for pokemon in pokemon_list:
                print(
                    f"  #{pokemon.id:03d} "
                    f"{format_label(pokemon.name)} - "
                    f"{format_label(stat_name)}: "
                    f"{pokemon.stats[stat_name.lower()]}"
                )

            print()
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