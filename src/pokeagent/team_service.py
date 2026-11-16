from __future__ import annotations

from pokeagent.models import StatTraining, Team
from pokeagent.service import PokedexService
from pokeagent.item_service import ItemService
from pokeagent.move_service import MoveService
from pokeagent.natures import NATURES
from pokeagent.type_effectiveness import (
    get_type_defensive_multipliers,
)


class TeamService:
    """Provide Pokémon team operations."""

    def __init__(self) -> None:
        self.pokedex = PokedexService()
        self.items = ItemService()
        self.moves = MoveService()

    def add_pokemon(
        self,
        team: Team,
        query: str | int,
     ) -> tuple[bool, str]:
        """Find and add a Pokémon to a team."""
        pokemon = self.pokedex.find_pokemon(query)

        if pokemon is None:
            return False, "Pokémon not found."

        if team.is_full:
            return False, "The team already has six Pokémon."

        if any(
            member.id == pokemon.id
            for member in team.members
        ):
            return False, (
                f"{pokemon.name} is already in the team."
            )

        team.add(pokemon)

        return True, (
            f"{pokemon.name} added to the team."
        )

    def remove_pokemon(
        self,
        team: Team,
        pokemon_id: int,
     ) -> tuple[bool, str]:
        """Remove a Pokémon from a team."""
        removed = team.remove(pokemon_id)

        if not removed:
            return False, "Pokémon not found in the team."

        return True, "Pokémon removed from the team."

    def clear_team(
        self,
        team: Team,
     ) -> None:
        """Remove every Pokémon from a team."""
        team.clear()

    def set_ability(
        self,
        team: Team,
        pokemon_id: int,
        ability_name: str,
     ) -> tuple[bool, str]:
        """Set the selected ability for a team member."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        normalized_ability = (
            ability_name.strip()
            .lower()
            .replace(" ", "-")
        )

        if (
            normalized_ability
            not in pokemon_set.pokemon.abilities
        ):
            return False, (
                f"{ability_name} is not available "
                f"for {pokemon_set.pokemon.name}."
            )

        pokemon_set.ability = (
            normalized_ability
        )

        return True, (
            f"{pokemon_set.pokemon.name} ability "
            f"set to {normalized_ability}."
        )
    def set_item(
        self,
        team: Team,
        pokemon_id: int,
        item_query: str | int,
     ) -> tuple[bool, str]:
        """Set the held item for a team member."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        item = self.items.find_item(
            item_query
        )

        pokemon_set.item = item.name

        return True, (
            f"{pokemon_set.pokemon.name} item "
            f"set to {item.name}."
        )
    def clear_item(
        self,
        team: Team,
        pokemon_id: int,
     ) -> tuple[bool, str]:
        """Remove the held item from a team member."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        pokemon_set.item = None

        return True, (
            f"{pokemon_set.pokemon.name} item cleared."
        )
    def add_move(
        self,
        team: Team,
        pokemon_id: int,
        move_query: str | int,
     ) -> tuple[bool, str]:
        """Add a compatible move to a team member set."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        if len(pokemon_set.moves) >= 4:
            return False, (
                "A Pokémon cannot have more than four moves."
            )

        move = self.moves.find_move(
            move_query
        )

        if move.name in pokemon_set.moves:
            return False, (
                f"{move.name} is already in the set."
            )

        can_learn = (
            self.moves.can_learn_move(
                pokemon_set.pokemon.id,
                move.name,
            )
        )

        if not can_learn:
            return False, (
                f"{pokemon_set.pokemon.name} "
                f"cannot learn {move.name}."
            )

        pokemon_set.moves.append(
            move.name
        )

        return True, (
            f"{move.name} added to "
            f"{pokemon_set.pokemon.name}."
        )
    def remove_move(
        self,
        team: Team,
        pokemon_id: int,
        move_name: str,
     ) -> tuple[bool, str]:
        """Remove a move from a team member set."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        normalized_move = (
            move_name.strip()
            .lower()
            .replace(" ", "-")
        )

        if normalized_move not in pokemon_set.moves:
            return False, (
                f"{normalized_move} is not in the set."
            )

        pokemon_set.moves.remove(
            normalized_move
        )

        return True, (
            f"{normalized_move} removed from "
            f"{pokemon_set.pokemon.name}."
        )
    def set_level(
        self,
        team: Team,
        pokemon_id: int,
        level: int,
     ) -> tuple[bool, str]:
        """Set the level for a team member."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        if level < 1 or level > 100:
            return False, (
                "Level must be between 1 and 100."
            )

        pokemon_set.level = level

        return True, (
            f"{pokemon_set.pokemon.name} level "
            f"set to {level}."
        )
    def analyze_type_defense(
        self,
        team: Team,
     ) -> dict[str, dict[str, int]]:
        """Analyze team weaknesses, resistances and immunities."""
        analysis: dict[str, dict[str, int]] = {}

        for member in team.members:
            multipliers = get_type_defensive_multipliers(
                member.types
            )

            for attacking_type, multiplier in multipliers.items():
                if attacking_type not in analysis:
                    analysis[attacking_type] = {
                        "weak": 0,
                        "resist": 0,
                        "immune": 0,
                    }

                if multiplier > 1:
                    analysis[attacking_type]["weak"] += 1

                elif multiplier == 0:
                    analysis[attacking_type]["immune"] += 1

                elif multiplier < 1:
                    analysis[attacking_type]["resist"] += 1

        return analysis

    def set_nature(
        self,
        team: Team,
        pokemon_id: int,
        nature: str,
     ) -> tuple[bool, str]:
        """Set the nature for a team member."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        normalized_nature = (
            nature.strip().lower()
        )

        if normalized_nature not in NATURES:
            return False, (
                f"Unknown nature: {nature}."
            )

        pokemon_set.nature = (
            normalized_nature
        )

        return True, (
            f"{pokemon_set.pokemon.name} nature "
            f"set to {normalized_nature}."
        )
    def set_training(
        self,
        team: Team,
        pokemon_id: int,
        ivs: dict[str, int],
        evs: dict[str, int],
     ) -> tuple[bool, str]:
        """Set IVs and EVs for a team member."""
        pokemon_set = team.get_set(
            pokemon_id
        )

        if pokemon_set is None:
            return False, (
                "Pokémon not found in the team."
            )

        training = StatTraining(
            ivs=dict(ivs),
            evs=dict(evs),
        )

        try:
            training.validate()

        except ValueError as exc:
            return False, str(exc)

        pokemon_set.training = training

        return True, (
            f"{pokemon_set.pokemon.name} "
            "training updated."
        )
    def get_shared_weaknesses(
        self,
        team: Team,
        minimum_count: int = 2,
     ) -> dict[str, int]:
        """Return attacking types that threaten multiple team members."""
        analysis = self.analyze_type_defense(team)

        return {
            attacking_type: values["weak"]
            for attacking_type, values in analysis.items()
            if values["weak"] >= minimum_count
        }