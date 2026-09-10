from __future__ import annotations

import streamlit as st

from pokeagent.service import PokedexService


def format_label(value: str) -> str:
    """Convert API-style names into readable labels."""
    return value.replace("-", " ").title()


def main() -> None:
    """Run the PokeAgent web interface."""
    st.set_page_config(
        page_title="PokeAgent",
        page_icon="🔴",
        layout="centered",
    )

    service = PokedexService()

    st.title("PokeAgent")
    st.caption("Kanto Pokédex — #001 to #151")

    st.write(
        "Search for any of the original 151 Kanto Pokémon "
        "by name or National Pokédex number."
    )

    with st.form("pokemon_search"):
        query = st.text_input(
            "Pokémon name or Pokédex number",
            placeholder="Example: Pikachu or 25",
        )

        submitted = st.form_submit_button("Search")

    if not submitted:
        return

    query = query.strip()

    if not query:
        st.warning("Please enter a Pokémon name or Pokédex number.")
        return

    pokemon = service.find_pokemon(query)

    if pokemon is None:
        st.error(
            f"No Pokémon matching '{query}' "
            "was found in the Kanto Pokédex."
        )
        return

    st.divider()

    st.header(
        f"#{pokemon.id:03d} {format_label(pokemon.name)}"
    )

    types = ", ".join(
        format_label(pokemon_type)
        for pokemon_type in pokemon.types
    )

    abilities = ", ".join(
        format_label(ability)
        for ability in pokemon.abilities
    )

    st.write(f"**Type:** {types}")
    st.write(f"**Abilities:** {abilities}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Height", f"{pokemon.height_m} m")

    with col2:
        st.metric("Weight", f"{pokemon.weight_kg} kg")

    st.subheader("Base Stats")

    for stat_name, value in pokemon.stats.items():
        st.write(
            f"**{format_label(stat_name)}:** {value}"
        )
        st.progress(min(value / 255, 1.0))


if __name__ == "__main__":
    main()