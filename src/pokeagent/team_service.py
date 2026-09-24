from __future__ import annotations

from pokeagent.models import Team
from pokeagent.service import PokedexService
from pokeagent.type_effectiveness import (
    get_type_defensive_multipliers,
)


class TeamService:
    """Provide Pokémon team operations."""

    def __init__(self) -> None:
        self.pokedex = PokedexService()

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