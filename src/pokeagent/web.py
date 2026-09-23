from __future__ import annotations

import streamlit as st
from pokeagent.move_service import MoveService
from pokeagent.item_service import ItemService
from pokeagent.api import PokeAPIError

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
VERSION_GROUP_OPTIONS = {
    "Red / Blue": "red-blue",
    "Yellow": "yellow",
}

MOVE_METHOD_OPTIONS = {
    "All Methods": None,
    "Level Up": "level-up",
    "Machine": "machine",
    "Tutor": "tutor",
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
def render_effectiveness_badges(
    effectiveness: dict[str, float],
 ) -> None:
    """Render type effectiveness values as colored badges."""
    if not effectiveness:
        st.write("None")
        return

    badges = []

    for pokemon_type, multiplier in effectiveness.items():
        color = TYPE_COLORS.get(
            pokemon_type,
            "#777777",
        )

        multiplier_text = (
            str(int(multiplier))
            if multiplier.is_integer()
            else str(multiplier)
        )

        badges.append(
            f"""
            <span style="
                background-color: {color};
                color: white;
                padding: 6px 10px;
                border-radius: 14px;
                font-weight: 600;
                margin: 3px;
                display: inline-block;
            ">
                {format_label(pokemon_type)} ×{multiplier_text}
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
    move_service = MoveService()
    item_service = ItemService()

    if "selected_pokemon_id" not in st.session_state:
        st.session_state.selected_pokemon_id = None

    if "selected_item_query" not in st.session_state:
        st.session_state.selected_item_query = None

    if "selected_move_query" not in st.session_state:
        st.session_state.selected_move_query = None

    st.title("PokeAgent")
    st.caption("Kanto Pokédex — #001 to #151")

    pokedex_tab, moves_tab, items_tab = st.tabs(
        ["Pokédex", "Moves", "Items"]
    )
    

    # ---------------------------------------------------------
    # POKÉDEX TAB
    # ---------------------------------------------------------

    with pokedex_tab:
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
            type_pokemon = service.find_by_type(
                selected_type
            )

            st.write(
                f"**{len(type_pokemon)} Pokémon found**"
            )

            type_columns = st.columns(3)

            for index, pokemon in enumerate(
                type_pokemon
            ):
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
                        st.session_state.selected_pokemon_id = (
                            pokemon.id
                        )

        st.divider()

        with st.form("pokemon_search"):
            query = st.text_input(
                "Pokémon name or Pokédex number",
                placeholder="Example: Pikachu or 25",
            )

            submitted = st.form_submit_button(
                "Search"
            )
        if st.button(
            "Clear Pokémon",
            key="clear_pokemon",
        ):
            st.session_state.selected_pokemon_id = None

        if submitted:
            query = query.strip()

            if not query:
                st.warning(
                    "Please enter a Pokémon name "
                    "or Pokédex number."
                )
            else:
                searched_pokemon = (
                    service.find_pokemon(query)
                )

                if searched_pokemon is None:
                    st.error(
                        f"No Pokémon matching '{query}' "
                        "was found in the Kanto Pokédex."
                    )

                    st.session_state.selected_pokemon_id = (
                        None
                    )

                else:
                    st.session_state.selected_pokemon_id = (
                        searched_pokemon.id
                    )

        selected_pokemon_id = (
            st.session_state.selected_pokemon_id
        )

        pokemon = None

        if selected_pokemon_id is not None:
            pokemon = service.find_pokemon(
                selected_pokemon_id
            )

        if pokemon is not None:
                st.divider()

                st.header(
                    f"#{pokemon.id:03d} "
                    f"{format_label(pokemon.name)}"
                )

                abilities = ", ".join(
                    format_label(ability)
                    for ability in pokemon.abilities
                )

                image_col, info_col = st.columns(
                    [1, 1.3]
                )

                with image_col:
                    if pokemon.image_url:
                        st.image(
                            pokemon.image_url,
                            use_container_width=True,
                        )

                with info_col:
                    st.subheader("Pokédex Data")

                    st.write("**Type:**")

                    render_type_badges(
                        pokemon.types
                    )

                    st.write(
                        f"**Abilities:** {abilities}"
                    )

                    metric_col1, metric_col2 = (
                        st.columns(2)
                    )

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

                    if (
                        pokemon.base_experience
                        is not None
                    ):
                        st.metric(
                            "Base Experience",
                            pokemon.base_experience,
                        )

                # -------------------------------------------------
                # BASE STATS
                # -------------------------------------------------

                st.divider()

                st.subheader("Base Stats")

                stat_items = list(
                    pokemon.stats.items()
                )

                for start in range(
                    0,
                    len(stat_items),
                    3,
                ):
                    stat_columns = st.columns(3)

                    for column, (
                        stat_name,
                        value,
                    ) in zip(
                        stat_columns,
                        stat_items[start:start + 3],
                    ):
                        with column:
                            st.metric(
                                format_label(
                                    stat_name
                                ),
                                value,
                            )

                            st.progress(
                                min(
                                    value / 255,
                                    1.0,
                                )
                            )

                total_stats = sum(
                    pokemon.stats.values()
                )

                st.metric(
                    "Total Base Stats",
                    total_stats,
                )

                # -------------------------------------------------
                # TYPE EFFECTIVENESS
                # -------------------------------------------------

                try:
                    effectiveness = (
                        service.get_type_effectiveness(
                            pokemon.id
                        )
                    )

                except PokeAPIError as exc:
                    effectiveness = None

                    st.warning(
                        "Type effectiveness could not "
                        f"be loaded: {exc}"
                    )

                if effectiveness:
                    st.divider()

                    st.subheader(
                        "Type Effectiveness"
                    )

                    (
                        weakness_col,
                        resistance_col,
                        immunity_col,
                    ) = st.columns(3)

                    with weakness_col:
                        st.write(
                            "**Weaknesses**"
                        )

                        render_effectiveness_badges(
                            effectiveness[
                                "weaknesses"
                            ]
                        )

                    with resistance_col:
                        st.write(
                            "**Resistances**"
                        )

                        render_effectiveness_badges(
                            effectiveness[
                                "resistances"
                            ]
                        )

                    with immunity_col:
                        st.write(
                            "**Immunities**"
                        )

                        render_effectiveness_badges(
                            effectiveness[
                                "immunities"
                            ]
                        )

                # -------------------------------------------------
                # EVOLUTION CHAIN
                # -------------------------------------------------

                if pokemon.evolutions:
                    st.divider()

                    st.subheader(
                        "Evolution Chain"
                    )

                    evolution_labels = [
                        format_label(name)
                        for name
                        in pokemon.evolutions
                    ]

                    st.write(
                        " → ".join(
                            evolution_labels
                        )
                    )

                # -------------------------------------------------
                # MOVES
                # -------------------------------------------------
    
                st.divider()

                st.subheader("Moves")

                game_col, method_col = st.columns(
                    2
                )

                with game_col:
                    selected_game_label = (
                        st.selectbox(
                            "Game",
                            options=list(
                                VERSION_GROUP_OPTIONS.keys()
                            ),
                            key=(
                                f"move_game_"
                                f"{pokemon.id}"
                            ),
                        )
                    )

                with method_col:
                    selected_method_label = (
                        st.selectbox(
                            "Learn Method",
                            options=list(
                                MOVE_METHOD_OPTIONS.keys()
                            ),
                            key=(
                                f"move_method_"
                                f"{pokemon.id}"
                            ),
                        )
                    )

                selected_version_group = (
                    VERSION_GROUP_OPTIONS[
                        selected_game_label
                    ]
                )

                selected_method = (
                    MOVE_METHOD_OPTIONS[
                        selected_method_label
                    ]
                )

                try:
                    with st.spinner(
                        "Loading moves..."
                    ):
                        moves = (
                            move_service
                            .get_detailed_learnset(
                                pokemon.id,
                                selected_version_group,
                                selected_method,
                            )
                        )

                except PokeAPIError as exc:
                    moves = []

                    st.warning(
                        "Move data could not "
                        f"be loaded: {exc}"
                    )

                if not moves:
                    st.info(
                        "No moves found for this "
                        "game and learning method."
                    )

                else:
                    move_rows = []

                    for learnset_move in moves:
                        move = (
                            learnset_move.move
                        )

                        level = (
                            learnset_move
                            .level_learned_at
                            if (
                                learnset_move.method
                                == "level-up"
                            )
                            else None
                        )

                        move_rows.append(
                            {
                                "Move": format_label(
                                    move.name
                                ),
                                "Level": level,
                                "Method": format_label(
                                    learnset_move.method
                                ),
                                "Type": format_label(
                                    move.type
                                ),
                                "Class": format_label(
                                    move.damage_class
                                ),
                                "Power": move.power,
                                "Accuracy": (
                                    move.accuracy
                                ),
                                "PP": move.pp,
                            }
                        )

                    move_rows.sort(
                        key=lambda row: (
                            (
                                row["Level"]
                                if row["Level"]
                                is not None
                                else 999
                            ),
                            row["Move"],
                        )
                    )

                    st.caption(
                        f"{selected_game_label} — "
                        f"{selected_method_label}"
                    )

                    st.dataframe(
                        move_rows,
                        use_container_width=True,
                        hide_index=True,
                    )

    # -------------------------------------------------
    # MOVES TAB
    # -------------------------------------------------            

    with moves_tab:
        st.subheader("Move Search")

        st.write(
            "Search for a Pokémon move "
            "by name or PokéAPI ID."
        )

        with st.form("move_search"):
            move_query = st.text_input(
                "Move name or PokéAPI ID",
                placeholder="Example: thunderbolt or thunder wave",
            )

            move_submitted = st.form_submit_button(
                "Search Move"
            )

        if st.button(
            "Clear Move",
            key="clear_move",
        ):
            st.session_state.selected_move_query = None

        if move_submitted:
            move_query = move_query.strip()

            if not move_query:
                st.session_state.selected_move_query = None
                st.warning(
                    "Please enter a move name or ID."
                )
            else:
                st.session_state.selected_move_query = move_query

        selected_move_query = (
            st.session_state.selected_move_query
        )

        if selected_move_query:
            try:
                move = move_service.find_move(
                    selected_move_query
                )

                st.divider()

                st.header(
                    format_label(move.name)
                )

                render_type_badges([move.type])

                metric_col1, metric_col2, metric_col3 = (
                    st.columns(3)
                )

                with metric_col1:
                    st.metric(
                        "Power",
                        move.power
                        if move.power is not None
                        else "—",
                    )

                with metric_col2:
                    st.metric(
                        "Accuracy",
                        move.accuracy
                        if move.accuracy is not None
                        else "—",
                    )

                with metric_col3:
                    st.metric(
                        "PP",
                        move.pp
                        if move.pp is not None
                        else "—",
                    )

                st.write(
                    f"**Damage Class:** "
                    f"{format_label(move.damage_class)}"
                )

            except PokeAPIError as exc:
                st.error(
                    f"Could not load move: {exc}"
                )

    # ---------------------------------------------------------
    # ITEMS TAB
    # ---------------------------------------------------------

    with items_tab:
        st.subheader("Item Search")

        st.write(
            "Search for a Pokémon item "
            "by name or PokéAPI ID."
        )

        with st.form("item_search"):
            item_query = st.text_input(
                "Item name or PokéAPI ID",
                placeholder=(
                    "Example: potion or rare candy"
                ),
            )
            
            item_submitted = (
             st.form_submit_button(
                "Search Item"
             )
            )

        if st.button(
             "Clear Item",
             key="clear_item",
        ):

              st.session_state.selected_item_query = None

        if item_submitted:
            item_query = item_query.strip()

            if not item_query:
                st.session_state.selected_item_query = None

                st.warning(
                    "Please enter an item name or ID."
                )

            else:
                st.session_state.selected_item_query = (
                    item_query
                )

        selected_item_query = (
            st.session_state.selected_item_query
        )

        if selected_item_query:
            try:
                item = item_service.find_item(
                    selected_item_query
                )

                st.divider()

                st.subheader("Item Details")

                image_col, item_col = st.columns(
                    [1, 2]
                )

                with image_col:
                    if item.image_url:
                        st.image(
                            item.image_url,
                            width=140,
                        )

                with item_col:
                    st.header(
                        format_label(
                            item.name
                        )
                    )

                    st.write(
                        f"**Category:** "
                        f"{format_label(item.category)}"
                    )

                    if item.effect:
                        st.info(
                            item.effect
                        )

                    else:
                        st.write(
                            "No effect description "
                            "available."
                        )

                    if item.prices:
                        st.write(
                            f"**Price records:** "
                            f"{len(item.prices)}"
                        )
            except PokeAPIError as exc:
                st.error(
                    f"Could not load item: {exc}"
                )
if __name__ == "__main__":
     main()