from __future__ import annotations

import streamlit as st

from pokeagent.ability_service import AbilityService
from pokeagent.api import PokeAPIError
from pokeagent.game_data_service import GameDataService
from pokeagent.item_service import ItemService
from pokeagent.models import StatTraining, Team
from pokeagent.move_service import MoveService
from pokeagent.natures import NATURES
from pokeagent.service import PokedexService
from pokeagent.stat_calculator import calculate_pokemon_stats
from pokeagent.team_service import TeamService


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
    "Gold / Silver": "gold-silver",
    "Crystal": "crystal",
    "Ruby / Sapphire": "ruby-sapphire",
    "Emerald": "emerald",
    "FireRed / LeafGreen": "firered-leafgreen",
    "Diamond / Pearl": "diamond-pearl",
    "Platinum": "platinum",
    "HeartGold / SoulSilver": "heartgold-soulsilver",
    "Black / White": "black-white",
    "Black 2 / White 2": "black-2-white-2",
    "X / Y": "x-y",
    "Omega Ruby / Alpha Sapphire": "omega-ruby-alpha-sapphire",
    "Sun / Moon": "sun-moon",
    "Ultra Sun / Ultra Moon": "ultra-sun-ultra-moon",
    "Let's Go Pikachu / Eevee": "lets-go-pikachu-lets-go-eevee",
    "Sword / Shield": "sword-shield",
    "Brilliant Diamond / Shining Pearl": "brilliant-diamond-shining-pearl",
    "Legends: Arceus": "legends-arceus",
    "Scarlet / Violet": "scarlet-violet",
}

GAME_AVAILABILITY_OPTIONS = {
    "Red / Blue": "red-blue",
    "Yellow": "yellow",
    "Gold / Silver": "gold-silver",
    "Crystal": "crystal",
    "Ruby / Sapphire": "ruby-sapphire",
    "Emerald": "emerald",
    "Diamond / Pearl": "diamond-pearl",
    "Platinum": "platinum",
    "Black / White": "black-white",
    "X / Y": "x-y",
    "Sun / Moon": "sun-moon",
    "Sword / Shield": "sword-shield",
    "Scarlet / Violet": "scarlet-violet",
}

MOVE_METHOD_OPTIONS = {
    "All Methods": None,
    "Level Up": "level-up",
    "Machine": "machine",
    "Tutor": "tutor",
}

STAT_NAMES = [
    "hp",
    "attack",
    "defense",
    "special-attack",
    "special-defense",
    "speed",
]


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


def render_ability_details(
    ability_names: list[str],
    ability_service: AbilityService,
    hidden_abilities: list[str] | None = None,
) -> None:
    """Render detailed Pokémon ability information."""
    hidden_abilities = hidden_abilities or []

    for ability_name in ability_names:
        try:
            ability = ability_service.find_ability(
                ability_name
            )

            label = format_label(ability.name)

            if ability_name in hidden_abilities:
                label += " — Hidden Ability"

            with st.expander(label):
                generation = (
                    ability.generation
                    .removeprefix("generation-")
                    .upper()
                )

                st.write(
                    f"**Generation:** {generation}"
                )

                if ability_name in hidden_abilities:
                    st.write(
                        "**Hidden Ability:** Yes"
                    )

                if ability.effect:
                    st.write(ability.effect)
                else:
                    st.write(
                        "No effect description available."
                    )

        except PokeAPIError as exc:
            st.warning(
                f"Could not load "
                f"{format_label(ability_name)}: {exc}"
            )


def render_national_type_browser(
    service: PokedexService,
 ) -> None:
    """Render National Pokédex browsing by one or two types."""
    st.subheader("Browse by Type")

    type_options = [""] + list(TYPE_COLORS.keys())

    type_col1, type_col2 = st.columns(2)

    with type_col1:
        primary_type = st.selectbox(
            "Primary type",
            options=type_options,
            format_func=lambda value: (
                "Any"
                if not value
                else format_label(value)
            ),
            key="browse_primary_type",
        )

    with type_col2:
        secondary_type = st.selectbox(
            "Secondary type",
            options=type_options,
            format_func=lambda value: (
                "Any"
                if not value
                else format_label(value)
            ),
            key="browse_secondary_type",
        )

    first_type = primary_type or None
    second_type = secondary_type or None

    # Allow users to use only the second selector.
    if first_type is None and second_type is not None:
        first_type = second_type
        second_type = None

    if first_type is None:
        st.caption(
            "Choose one type, or combine two types "
            "to search the National Pokédex."
        )
        return

    try:
        with st.spinner(
            "Searching the National Pokédex..."
        ):
            type_results = service.find_by_types(
                first_type,
                second_type,
            )

    except PokeAPIError as exc:
        st.warning(
            f"Type search could not be loaded: {exc}"
        )
        return

    if second_type and second_type != first_type:
        st.write(
            f"**{len(type_results)} Pokémon with "
            f"{format_label(first_type)} + "
            f"{format_label(second_type)} typing**"
        )
    else:
        st.write(
            f"**{len(type_results)} Pokémon with "
            f"{format_label(first_type)} typing**"
        )

    if not type_results:
        st.info(
            "No Pokémon found with that type combination."
        )
        return

    type_rows = [
        {
            "National #": f"#{pokemon['id']:04d}",
            "Pokémon": format_label(
                str(pokemon["name"])
            ),
        }
        for pokemon in type_results
    ]

    st.dataframe(
        type_rows,
        use_container_width=True,
        hide_index=True,
    )

    result_names = {
        int(pokemon["id"]): str(pokemon["name"])
        for pokemon in type_results
    }

    selected_type_pokemon = st.selectbox(
        "Open Pokémon",
        options=list(result_names.keys()),
        format_func=lambda pokemon_id: (
            f"#{pokemon_id:04d} "
            f"{format_label(result_names[pokemon_id])}"
        ),
        key="type_result_pokemon",
    )

    if st.button(
        "View Pokémon",
        key="view_type_pokemon",
        use_container_width=True,
    ):
        st.session_state.selected_pokemon_id = (
            selected_type_pokemon
        )
        st.rerun()
def render_generation_browser(
    service: PokedexService,
 ) -> None:
    """Render National Pokédex browsing by generation."""
    st.subheader("Browse by Generation")

    generation_options = {
        "Any": None,
        "Generation I": 1,
        "Generation II": 2,
        "Generation III": 3,
        "Generation IV": 4,
        "Generation V": 5,
        "Generation VI": 6,
        "Generation VII": 7,
        "Generation VIII": 8,
        "Generation IX": 9,
    }

    selected_generation_label = st.selectbox(
        "Generation",
        options=list(
            generation_options.keys()
        ),
        key="browse_generation",
    )

    selected_generation = (
        generation_options[
            selected_generation_label
        ]
    )

    if selected_generation is None:
        st.caption(
            "Choose a generation to browse "
            "its Pokémon."
        )
        return

    try:
        with st.spinner(
            "Loading generation..."
        ):
            generation_results = (
                service.find_by_generation(
                    selected_generation
                )
            )

    except PokeAPIError as exc:
        st.warning(
            f"Generation could not be loaded: {exc}"
        )
        return

    st.write(
        f"**{len(generation_results)} Pokémon "
        f"in {selected_generation_label}**"
    )

    generation_rows = [
        {
            "National #": (
                f"#{pokemon['id']:04d}"
            ),
            "Pokémon": format_label(
                str(pokemon["name"])
            ),
        }
        for pokemon in generation_results
    ]

    st.dataframe(
        generation_rows,
        use_container_width=True,
        hide_index=True,
    )

    if not generation_results:
        return

    generation_names = {
        int(pokemon["id"]): str(
            pokemon["name"]
        )
        for pokemon in generation_results
    }

    selected_generation_pokemon = (
        st.selectbox(
            "Open Pokémon from generation",
            options=list(
                generation_names.keys()
            ),
            format_func=lambda pokemon_id: (
                f"#{pokemon_id:04d} "
                f"{format_label(
                    generation_names[pokemon_id]
                )}"
            ),
            key="generation_result_pokemon",
        )
    )

    if st.button(
        "View Generation Pokémon",
        key="view_generation_pokemon",
        use_container_width=True,
    ):
        st.session_state.selected_pokemon_id = (
            selected_generation_pokemon
        )
        st.rerun()


def render_pokemon_profile(
    pokemon,
    service: PokedexService,
    move_service: MoveService,
    ability_service: AbilityService,
    game_data_service: GameDataService,
) -> None:
    """Render the complete Pokémon profile."""
    st.divider()

    st.header(
        f"#{pokemon.id:04d} "
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

        render_ability_details(
            pokemon.abilities,
            ability_service,
            pokemon.hidden_abilities,
        )

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

    # ---------------------------------------------------------
    # GAME AVAILABILITY
    # ---------------------------------------------------------

    st.divider()
    st.subheader("Game Availability")

    selected_game_label = st.selectbox(
        "Check game availability",
        options=list(
            GAME_AVAILABILITY_OPTIONS.keys()
        ),
        key=f"availability_game_{pokemon.id}",
    )

    selected_game_group = (
        GAME_AVAILABILITY_OPTIONS[
            selected_game_label
        ]
    )

    try:
        with st.spinner(
            "Checking game availability..."
        ):
            available = (
                game_data_service
                .is_pokemon_available(
                    pokemon.id,
                    selected_game_group,
                )
            )

        if available:
            st.success(
                f"{format_label(pokemon.name)} "
                f"is available in "
                f"{selected_game_label}."
            )
        else:
            st.warning(
                f"{format_label(pokemon.name)} "
                f"is not available in "
                f"{selected_game_label}."
            )

    except PokeAPIError as exc:
        st.warning(
            "Game availability could not "
            f"be checked: {exc}"
        )

    # ---------------------------------------------------------
    # BASE STATS
    # ---------------------------------------------------------

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
                    format_label(stat_name),
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

    # ---------------------------------------------------------
    # TYPE EFFECTIVENESS
    # ---------------------------------------------------------

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
            st.write("**Weaknesses**")
            render_effectiveness_badges(
                effectiveness[
                    "weaknesses"
                ]
            )

        with resistance_col:
            st.write("**Resistances**")
            render_effectiveness_badges(
                effectiveness[
                    "resistances"
                ]
            )

        with immunity_col:
            st.write("**Immunities**")
            render_effectiveness_badges(
                effectiveness[
                    "immunities"
                ]
            )

    # ---------------------------------------------------------
    # EVOLUTION CHAIN
    # ---------------------------------------------------------

    if pokemon.evolutions:
        st.divider()
        st.subheader(
            "Evolution Chain"
        )

        evolution_labels = [
            format_label(name)
            for name in pokemon.evolutions
        ]

        st.write(
            " → ".join(
                evolution_labels
            )
        )

    # ---------------------------------------------------------
    # MOVES
    # ---------------------------------------------------------

    st.divider()
    st.subheader("Moves")

    game_col, method_col = st.columns(2)

    with game_col:
        selected_move_game_label = st.selectbox(
            "Game",
            options=list(
                VERSION_GROUP_OPTIONS.keys()
            ),
            key=f"move_game_{pokemon.id}",
        )

    with method_col:
        selected_method_label = st.selectbox(
            "Learn Method",
            options=list(
                MOVE_METHOD_OPTIONS.keys()
            ),
            key=f"move_method_{pokemon.id}",
        )

    selected_version_group = (
        VERSION_GROUP_OPTIONS[
            selected_move_game_label
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
        return

    move_rows = []

    for learnset_move in moves:
        move = learnset_move.move

        level = (
            learnset_move.level_learned_at
            if learnset_move.method == "level-up"
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
                "Accuracy": move.accuracy,
                "PP": move.pp,
            }
        )

    move_rows.sort(
        key=lambda row: (
            (
                row["Level"]
                if row["Level"] is not None
                else 999
            ),
            row["Move"],
        )
    )

    st.caption(
        f"{selected_move_game_label} — "
        f"{selected_method_label}"
    )

    st.dataframe(
        move_rows,
        use_container_width=True,
        hide_index=True,
    )


def render_team_builder(
    team_service: TeamService,
) -> None:
    """Render the Team Builder tab."""
    st.subheader("Team Builder")

    team = st.session_state.team

    st.write(
        f"**Team size: {len(team.members)} / 6**"
    )

    with st.form("team_add_pokemon"):
        team_query = st.text_input(
            "Pokémon name or Pokédex number",
            placeholder=(
                "Example: Pikachu, Garchomp or 658"
            ),
        )

        add_submitted = st.form_submit_button(
            "Add Pokémon"
        )

    if add_submitted:
        team_query = team_query.strip()

        if not team_query:
            st.warning(
                "Please enter a Pokémon name "
                "or Pokédex number."
            )
        else:
            try:
                success, message = (
                    team_service.add_pokemon(
                        team,
                        team_query,
                    )
                )

                if success:
                    st.success(message)
                else:
                    st.warning(message)

            except PokeAPIError as exc:
                st.error(
                    f"Could not add Pokémon: {exc}"
                )

    if not team.members:
        st.info(
            "Your team is empty. "
            "Add up to six Pokémon."
        )
        return

    st.divider()

    team_columns = st.columns(3)

    for index, member in enumerate(
        list(team.members)
    ):
        column = team_columns[index % 3]

        with column:
            st.markdown(
                f"### #{member.id:04d} "
                f"{format_label(member.name)}"
            )

            if member.image_url:
                st.image(
                    member.image_url,
                    use_container_width=True,
                )

            render_type_badges(
                member.types
            )

            if st.button(
                "Remove",
                key=f"remove_team_{member.id}",
                use_container_width=True,
            ):
                team_service.remove_pokemon(
                    team,
                    member.id,
                )
                st.rerun()

    # ---------------------------------------------------------
    # STAT BUILDER
    # ---------------------------------------------------------

    st.divider()
    st.subheader("Stat Builder")

    selected_member_id = st.selectbox(
        "Configure Pokémon",
        options=[
            member.id
            for member in team.members
        ],
        format_func=lambda pokemon_id: (
            format_label(
                next(
                    member.name
                    for member in team.members
                    if member.id == pokemon_id
                )
            )
        ),
        key="stat_builder_member",
    )

    selected_member = next(
        member
        for member in team.members
        if member.id == selected_member_id
    )

    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        level = st.number_input(
            "Level",
            min_value=1,
            max_value=100,
            value=50,
            step=1,
            key=f"level_{selected_member.id}",
        )

    with settings_col2:
        nature = st.selectbox(
            "Nature",
            options=list(NATURES.keys()),
            index=list(NATURES.keys()).index(
                "hardy"
            ),
            format_func=format_label,
            key=f"nature_{selected_member.id}",
        )

    st.write("### IVs")

    iv_columns = st.columns(3)
    ivs = {}

    for index, stat_name in enumerate(
        STAT_NAMES
    ):
        with iv_columns[index % 3]:
            ivs[stat_name] = st.number_input(
                f"{format_label(stat_name)} IV",
                min_value=0,
                max_value=31,
                value=31,
                step=1,
                key=(
                    f"iv_{selected_member.id}_"
                    f"{stat_name}"
                ),
            )

    st.write("### EVs")

    ev_columns = st.columns(3)
    evs = {}

    for index, stat_name in enumerate(
        STAT_NAMES
    ):
        with ev_columns[index % 3]:
            evs[stat_name] = st.number_input(
                f"{format_label(stat_name)} EV",
                min_value=0,
                max_value=252,
                value=0,
                step=4,
                key=(
                    f"ev_{selected_member.id}_"
                    f"{stat_name}"
                ),
            )

    total_evs = sum(evs.values())

    st.write(
        f"**Total EVs: {total_evs} / 510**"
    )

    st.progress(
        min(total_evs / 510, 1.0)
    )

    if total_evs > 510:
        st.error(
            f"EV limit exceeded by "
            f"{total_evs - 510} points."
        )
    elif total_evs == 510:
        st.success(
            "Maximum EV total reached."
        )
    else:
        st.caption(
            f"{510 - total_evs} EVs remaining."
        )

    training = StatTraining(
        ivs=ivs,
        evs=evs,
    )

    try:
        calculated_stats = (
            calculate_pokemon_stats(
                selected_member,
                training,
                int(level),
                nature,
            )
        )

        st.write("### Calculated Stats")

        stat_columns = st.columns(3)

        for index, stat_name in enumerate(
            STAT_NAMES
        ):
            with stat_columns[index % 3]:
                st.metric(
                    format_label(stat_name),
                    calculated_stats[
                        stat_name
                    ],
                )

    except ValueError as exc:
        st.error(str(exc))

    # ---------------------------------------------------------
    # TEAM TYPE ANALYSIS
    # ---------------------------------------------------------

    st.divider()
    st.subheader("Team Type Analysis")

    st.caption(
        "Defensive overview against each attacking type."
    )

    try:
        with st.spinner(
            "Analyzing team type matchups..."
        ):
            analysis = (
                team_service.analyze_type_defense(
                    team
                )
            )

        analysis_rows = []

        for attacking_type, values in analysis.items():
            analysis_rows.append(
                {
                    "Attack Type": format_label(
                        attacking_type
                    ),
                    "Weak": values["weak"],
                    "Resist": values["resist"],
                    "Immune": values["immune"],
                }
            )

        analysis_rows.sort(
            key=lambda row: (
                -row["Weak"],
                row["Attack Type"],
            )
        )

        st.dataframe(
            analysis_rows,
            use_container_width=True,
            hide_index=True,
        )

        shared_weaknesses = (
            team_service.get_shared_weaknesses(
                team
            )
        )

        if shared_weaknesses:
            st.subheader("Shared Weaknesses")

            shared_rows = [
                {
                    "Type": format_label(
                        attacking_type
                    ),
                    "Pokémon Weak": count,
                }
                for attacking_type, count
                in shared_weaknesses.items()
            ]

            shared_rows.sort(
                key=lambda row: (
                    -row["Pokémon Weak"],
                    row["Type"],
                )
            )

            for row in shared_rows:
                st.warning(
                    f"{row['Type']}: "
                    f"{row['Pokémon Weak']} "
                    "team members are weak"
                )

        else:
            st.success(
                "No shared weaknesses detected."
            )

    except PokeAPIError as exc:
        st.warning(
            "Team type analysis could not "
            f"be loaded: {exc}"
        )

    st.divider()

    if st.button(
        "Clear Team",
        key="clear_team",
    ):
        team_service.clear_team(team)
        st.rerun()


def render_moves_tab(
    move_service: MoveService,
) -> None:
    """Render the independent move search."""
    st.subheader("Move Search")

    st.write(
        "Search for a Pokémon move "
        "by name or PokéAPI ID."
    )

    with st.form("move_search"):
        move_query = st.text_input(
            "Move name or PokéAPI ID",
            placeholder=(
                "Example: thunderbolt or thunder wave"
            ),
        )

        move_submitted = (
            st.form_submit_button(
                "Search Move"
            )
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
            st.session_state.selected_move_query = (
                move_query
            )

    selected_move_query = (
        st.session_state.selected_move_query
    )

    if not selected_move_query:
        return

    try:
        move = move_service.find_move(
            selected_move_query
        )

        st.divider()
        st.header(
            format_label(move.name)
        )

        render_type_badges(
            [move.type]
        )

        metric_col1, metric_col2, metric_col3 = (
            st.columns(3)
        )

        with metric_col1:
            st.metric(
                "Power",
                (
                    move.power
                    if move.power is not None
                    else "—"
                ),
            )

        with metric_col2:
            st.metric(
                "Accuracy",
                (
                    move.accuracy
                    if move.accuracy is not None
                    else "—"
                ),
            )

        with metric_col3:
            st.metric(
                "PP",
                (
                    move.pp
                    if move.pp is not None
                    else "—"
                ),
            )

        st.write(
            f"**Damage Class:** "
            f"{format_label(move.damage_class)}"
        )

    except PokeAPIError as exc:
        st.error(
            f"Could not load move: {exc}"
        )


def render_abilities_tab(
    ability_service: AbilityService,
) -> None:
    """Render the independent ability search."""
    st.subheader("Ability Search")

    st.write(
        "Search for a Pokémon ability "
        "by name or PokéAPI ID."
    )

    with st.form("ability_search"):
        ability_query = st.text_input(
            "Ability name or PokéAPI ID",
            placeholder=(
                "Example: static or lightning rod"
            ),
        )

        ability_submitted = (
            st.form_submit_button(
                "Search Ability"
            )
        )

    if st.button(
        "Clear Ability",
        key="clear_ability",
    ):
        st.session_state.selected_ability_query = None

    if ability_submitted:
        ability_query = ability_query.strip()

        if not ability_query:
            st.session_state.selected_ability_query = None
            st.warning(
                "Please enter an ability name or ID."
            )
        else:
            st.session_state.selected_ability_query = (
                ability_query
            )

    selected_ability_query = (
        st.session_state.selected_ability_query
    )

    if not selected_ability_query:
        return

    try:
        ability = ability_service.find_ability(
            selected_ability_query
        )

        st.divider()
        st.header(
            format_label(ability.name)
        )

        generation_number = (
            ability.generation
            .removeprefix("generation-")
            .upper()
        )

        st.write(
            f"**Generation:** "
            f"{generation_number}"
        )

        if ability.effect:
            st.info(
                ability.effect
            )
        else:
            st.write(
                "No effect description available."
            )

    except PokeAPIError as exc:
        st.error(
            f"Could not load ability: {exc}"
        )


def render_games_tab(
    game_data_service: GameDataService,
) -> None:
    """Render the game version-group search."""
    st.subheader("Game Version Groups")

    st.write(
        "Search for a Pokémon game version group "
        "by name or PokéAPI ID."
    )

    with st.form("game_search"):
        game_query = st.text_input(
            "Version group name or ID",
            placeholder=(
                "Example: red blue or scarlet violet"
            ),
        )

        game_submitted = (
            st.form_submit_button(
                "Search Game"
            )
        )

    if st.button(
        "Clear Game",
        key="clear_game",
    ):
        st.session_state.selected_game_query = None

    if game_submitted:
        game_query = game_query.strip()

        if not game_query:
            st.session_state.selected_game_query = None
            st.warning(
                "Please enter a version group name or ID."
            )
        else:
            st.session_state.selected_game_query = (
                game_query
            )

    selected_game_query = (
        st.session_state.selected_game_query
    )

    if not selected_game_query:
        return

    try:
        game_group = (
            game_data_service.find_version_group(
                selected_game_query
            )
        )

        st.divider()
        st.header(
            format_label(game_group.name)
        )

        generation = (
            game_group.generation
            .removeprefix("generation-")
            .upper()
        )

        st.metric(
            "Generation",
            generation,
        )

        st.write("**Versions:**")

        version_columns = st.columns(
            len(game_group.versions)
        )

        for column, version in zip(
            version_columns,
            game_group.versions,
        ):
            with column:
                st.info(
                    format_label(version)
                )

    except PokeAPIError as exc:
        st.error(
            f"Could not load game data: {exc}"
        )


def render_items_tab(
    item_service: ItemService,
) -> None:
    """Render the independent item search."""
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

    if not selected_item_query:
        return

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
                    "No effect description available."
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
    team_service = TeamService()
    ability_service = AbilityService()
    game_data_service = GameDataService()

    if "selected_pokemon_id" not in st.session_state:
        st.session_state.selected_pokemon_id = None

    if "selected_item_query" not in st.session_state:
        st.session_state.selected_item_query = None

    if "selected_move_query" not in st.session_state:
        st.session_state.selected_move_query = None

    if "selected_ability_query" not in st.session_state:
        st.session_state.selected_ability_query = None

    if "selected_game_query" not in st.session_state:
        st.session_state.selected_game_query = None

    if "team" not in st.session_state:
        st.session_state.team = Team()

    st.title("PokeAgent")
    st.caption("National Pokédex")

    (
        pokedex_tab,
        team_tab,
        moves_tab,
        abilities_tab,
        games_tab,
        items_tab,
    ) = st.tabs(
        [
            "Pokédex",
            "Team Builder",
            "Moves",
            "Abilities",
            "Games",
            "Items",
        ]
    )

    # ---------------------------------------------------------
    # POKÉDEX TAB
    # ---------------------------------------------------------

    with pokedex_tab:
        st.write(
            "Search for any Pokémon by name "
            "or National Pokédex number."
        )

        render_national_type_browser(
            service
        )

        st.divider()
        
        render_generation_browser(
            service
        )
        st.divider()

        with st.form("pokemon_search"):
            query = st.text_input(
                "Pokémon name or Pokédex number",
                placeholder=(
                    "Example: Pikachu, Garchomp or 445"
                ),
            )

            submitted = (
                st.form_submit_button(
                    "Search"
                )
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
                try:
                    searched_pokemon = (
                        service.find_pokemon(
                            query
                        )
                    )

                except PokeAPIError as exc:
                    searched_pokemon = None
                    st.error(
                        f"Could not load Pokémon: {exc}"
                    )

                if searched_pokemon is None:
                    st.error(
                        f"No Pokémon matching '{query}' "
                        "was found in the National Pokédex."
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
            try:
                pokemon = service.find_pokemon(
                    selected_pokemon_id
                )
            except PokeAPIError as exc:
                st.error(
                    f"Could not load Pokémon: {exc}"
                )

        if pokemon is not None:
            render_pokemon_profile(
                pokemon,
                service,
                move_service,
                ability_service,
                game_data_service,
            )

    # ---------------------------------------------------------
    # TEAM BUILDER TAB
    # ---------------------------------------------------------

    with team_tab:
        render_team_builder(
            team_service
        )

    # ---------------------------------------------------------
    # MOVES TAB
    # ---------------------------------------------------------

    with moves_tab:
        render_moves_tab(
            move_service
        )

    # ---------------------------------------------------------
    # ABILITIES TAB
    # ---------------------------------------------------------

    with abilities_tab:
        render_abilities_tab(
            ability_service
        )

    # ---------------------------------------------------------
    # GAMES TAB
    # ---------------------------------------------------------

    with games_tab:
        render_games_tab(
            game_data_service
        )

    # ---------------------------------------------------------
    # ITEMS TAB
    # ---------------------------------------------------------

    with items_tab:
        render_items_tab(
            item_service
        )


if __name__ == "__main__":
    main()
