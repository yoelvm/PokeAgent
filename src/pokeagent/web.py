from __future__ import annotations

import streamlit as st

from pokeagent.service import PokedexService

TYPE_COLORS = {
    "normal": "#A8A77A",
    "fire": "#EE8130",
    "water": "#6390F0",
    "electric": "#F7D02C",
    "grass": "#7AC74C",
    "ice": "#96D9D6",
    "fighting": "#C22E28",
    "poison": "#A33EA1",
    "ground": "#E2BF65",
    "flying": "#A98FF3",
    "psychic": "#F95587",
    "bug": "#A6B91A",
    "rock": "#B6A136",
    "ghost": "#735797",
    "dragon": "#6F35FC",
    "dark": "#705746",
    "steel": "#B7B7CE",
    "fairy": "#D685AD",
}


def format_label(value: str) -> str:
    """Convert API-style names into readable labels."""
    return value.replace("-", " ").title()

def render_type_badges(pokemon_types: list[str]) -> None:
    """Render Pokémon types as colored badges."""
    badges = []

    for pokemon_type in pokemon_types:
        color = TYPE_COLORS.get(pokemon_type, "#777777")

        badges.append(
            f"""
            <span style="
                background-color: {color};
                color: white;
                padding: 6px 12px;
                border-radius: 14px;
                font-weight: 600;
                margin-right: 6px;
                display: inline-block;
            ">
                {format_label(pokemon_type)}
            </span>
            """
        )

    st.markdown(
        "".join(badges),
        unsafe_allow_html=True,
    )

def main() -> None:
    """Run the PokeAgent web interface."""
    st.set_page_config(
        page_title="PokeAgent",
        page_icon="🔴",
        layout="centered",
    )

    service = PokedexService()

    if "selected_pokemon_id" not in st.session_state:
        st.session_state.selected_pokemon_id = None

    st.title("PokeAgent")
    st.caption("Kanto Pokédex — #001 to #151")

    st.write(
        "Search for any of the original 151 Kanto Pokémon "
        "by name or National Pokédex number."
    )
    st.subheader("Browse by Type")

    available_types = sorted(
        {
            pokemon_type
            for pokemon in service.repository.get_all()
            for pokemon_type in pokemon.types
        }
    )

    selected_type = st.selectbox(
        "Pokémon type",
        options=[""] + available_types,
        format_func=lambda value: (
            "Select a type..."
            if not value
            else format_label(value)
        ),
    )

    if selected_type:
        type_pokemon = service.find_by_type(selected_type)

        st.write(
            f"**{len(type_pokemon)} Pokémon found**"
        )

        type_columns = st.columns(3)

        for index, pokemon in enumerate(type_pokemon):
            column = type_columns[index % 3]

            with column:
                if pokemon.image_url:
                    st.image(
                        pokemon.image_url,
                        use_container_width=True,
                    )

                st.write(
                    f"**#{pokemon.id:03d} "
                    f"{format_label(pokemon.name)}**"
                )
                if st.button(
                     "View",
                     key=f"view_{pokemon.id}",
                     use_container_width=True,
                ):
                    st.session_state.selected_pokemon_id = pokemon.id

    st.divider()

    with st.form("pokemon_search"):
        query = st.text_input(
            "Pokémon name or Pokédex number",
            placeholder="Example: Pikachu or 25",
        )

        submitted = st.form_submit_button("Search")

    if submitted:
        query = query.strip()

        if not query:
            st.warning(
                "Please enter a Pokémon name or Pokédex number."
            )
            return

        searched_pokemon = service.find_pokemon(query)

        if searched_pokemon is None:
            st.error(
                f"No Pokémon matching '{query}' "
                "was found in the Kanto Pokédex."
            )
            return

        st.session_state.selected_pokemon_id = searched_pokemon.id

    selected_pokemon_id = st.session_state.selected_pokemon_id

    if selected_pokemon_id is None:
        return

    pokemon = service.find_pokemon(selected_pokemon_id)

    if pokemon is None:
        return
    st.divider()

    st.header(
        f"#{pokemon.id:03d} {format_label(pokemon.name)}"
    )

    abilities = ", ".join(
        format_label(ability)
        for ability in pokemon.abilities
    )

    image_col, info_col = st.columns([1, 1.3])

    with image_col:
        if pokemon.image_url:
            st.image(
                pokemon.image_url,
                use_container_width=True,
            )

    with info_col:
        st.subheader("Pokédex Data")

        st.write("**Type:**")
        render_type_badges(pokemon.types)
        st.write(f"**Abilities:** {abilities}")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                "Height",
                f"{pokemon.height_m} m",
            )

        with metric_col2:
            st.metric(
                "Weight",
                f"{pokemon.weight_kg} kg",
            )

        if pokemon.base_experience is not None:
            st.metric(
                "Base Experience",
                pokemon.base_experience,
            )

    st.divider()

    st.subheader("Base Stats")

    stat_items = list(pokemon.stats.items())

    for start in range(0, len(stat_items), 3):
        stat_columns = st.columns(3)

        for column, (stat_name, value) in zip(
            stat_columns,
            stat_items[start:start + 3],
        ):
            with column:
                st.metric(
                    format_label(stat_name),
                    value,
                )

                st.progress(
                    min(value / 255, 1.0)
                )

    total_stats = sum(pokemon.stats.values())

    st.metric(
        "Total Base Stats",
        total_stats,
    )
if __name__ == "__main__":
     main()