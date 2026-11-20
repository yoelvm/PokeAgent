from __future__ import annotations
from pokeagent.game_data_service import GameDataService
from pokeagent.move_service import MoveService

from pokeagent.item_service import ItemService
from pokeagent.api import PokeAPIError

from pokeagent.models import (
    LegalityResult,
    PokemonSet,
    Team,
    TeamLegalityResult,
)


class LegalityService:
    """Validate Pokémon sets against game data."""

    def __init__(self) -> None:
       self.game_data = GameDataService()
       self.moves = MoveService()
       self.items = ItemService()

    def validate_team(
        self,
        team: Team,
        version_group: str,
     ) -> TeamLegalityResult:
        """Validate every competitive set in a team."""
        result = TeamLegalityResult()

        if not team.members:
            result.add_warning(
                "empty-team",
                "The team does not contain any Pokémon.",
            )

            return result

        if len(team.members) > 6:
            result.add_error(
                "too-many-members",
                "A team cannot contain more than six Pokémon.",
            )

        elif len(team.members) < 6:
            result.add_warning(
                "incomplete-team",
                (
                    f"The team contains "
                    f"{len(team.members)} / 6 Pokémon."
                ),
            )

        member_ids = [
            member.id
            for member in team.members
        ]

        if len(member_ids) != len(
            set(member_ids)
        ):
            result.add_error(
                "duplicate-pokemon",
                "The team contains duplicate Pokémon.",
            )

        for member in team.members:
            pokemon_set = team.get_set(
                member.id
            )

            if pokemon_set is None:
                member_result = (
                    LegalityResult()
                )

                member_result.add_error(
                    "missing-set",
                    (
                        f"{member.name} does not "
                        "have a competitive set."
                    ),
                )

            else:
                member_result = (
                    self.validate_set(
                        pokemon_set,
                        version_group,
                    )
                )

            result.member_results[
                member.id
            ] = member_result

        return result

    def validate_pokemon_availability(
        self,
        pokemon_set: PokemonSet,
        version_group: str,
        result: LegalityResult | None = None,
     ) -> LegalityResult:
        """Validate whether the Pokémon exists in a version group."""
        legality_result = (
            result
            if result is not None
            else LegalityResult()
        )

        available = (
            self.game_data
            .is_pokemon_available(
                pokemon_set.pokemon.id,
                version_group,
            )
        )

        if not available:
            legality_result.add_error(
                "pokemon-unavailable",
                (
                    f"{pokemon_set.pokemon.name} "
                    f"is not available in "
                    f"{version_group}."
                ),
            )

        return legality_result

    def validate_moves(
        self,
        pokemon_set: PokemonSet,
        version_group: str,
        result: LegalityResult | None = None,
      ) -> LegalityResult:
        """Validate moves for a specific version group."""
        legality_result = (
            result
            if result is not None
            else LegalityResult()
        )

        normalized_version = "-".join(
            version_group.strip()
            .lower()
            .split()
        )

        learnable_moves = set(
            self.moves.get_learnable_move_names(
                pokemon_set.pokemon.id,
                normalized_version,
            )
        )

        for move_name in pokemon_set.moves:
            if move_name not in learnable_moves:
                legality_result.add_error(
                    "illegal-move",
                    (
                        f"{pokemon_set.pokemon.name} "
                        f"cannot learn {move_name} "
                        f"in {normalized_version}."
                    ),
                )

        return legality_result
    def validate_ability(
        self,
        pokemon_set: PokemonSet,
        result: LegalityResult | None = None,
     ) -> LegalityResult:
        """Validate the selected Pokémon ability."""
        legality_result = (
            result
            if result is not None
            else LegalityResult()
        )

        ability = pokemon_set.ability

        if ability is None:
            legality_result.add_warning(
                "missing-ability",
                (
                    f"{pokemon_set.pokemon.name} "
                    "does not have a selected ability."
                ),
            )

            return legality_result

        normalized_ability = (
            ability.strip()
            .lower()
            .replace(" ", "-")
        )

        if (
            normalized_ability
            not in pokemon_set.pokemon.abilities
        ):
            legality_result.add_error(
                "illegal-ability",
                (
                    f"{normalized_ability} "
                    f"is not a valid ability for "
                    f"{pokemon_set.pokemon.name}."
                ),
            )

        return legality_result
    def validate_item(
        self,
        pokemon_set: PokemonSet,
        result: LegalityResult | None = None,
     ) -> LegalityResult:
        """Validate the selected held item."""
        legality_result = (
            result
            if result is not None
            else LegalityResult()
        )

        if pokemon_set.item is None:
            legality_result.add_warning(
                "missing-item",
                (
                    f"{pokemon_set.pokemon.name} "
                    "does not have a held item."
                ),
            )

            return legality_result

        try:
            self.items.find_item(
                pokemon_set.item
            )

        except PokeAPIError:
            legality_result.add_error(
                "invalid-item",
                (
                    f"{pokemon_set.item} "
                    "is not a valid item."
                ),
            )

        return legality_result
    def validate_set(
        self,
        pokemon_set: PokemonSet,
        version_group: str,
     ) -> LegalityResult:
        """Validate a complete Pokémon set."""
        result = LegalityResult()

        # -----------------------------------------------------
        # BASIC SET STRUCTURE
        # -----------------------------------------------------

        if pokemon_set.level < 1 or pokemon_set.level > 100:
            result.add_error(
                "invalid-level",
                (
                    f"{pokemon_set.pokemon.name} "
                    "must have a level between 1 and 100."
                ),
            )

        try:
            pokemon_set.training.validate()

        except ValueError as exc:
            result.add_error(
                "invalid-training",
                str(exc),
            )

        if len(pokemon_set.moves) > 4:
            result.add_error(
                "too-many-moves",
                (
                    f"{pokemon_set.pokemon.name} "
                    "cannot have more than four moves."
                ),
            )

        if len(set(pokemon_set.moves)) != len(
            pokemon_set.moves
        ):
            result.add_error(
                "duplicate-moves",
                (
                    f"{pokemon_set.pokemon.name} "
                    "has duplicate moves."
                ),
            )

        if not pokemon_set.moves:
            result.add_warning(
                "missing-moves",
                (
                    f"{pokemon_set.pokemon.name} "
                    "does not have any selected moves."
                ),
            )

        # -----------------------------------------------------
        # GAME-SPECIFIC VALIDATION
        # -----------------------------------------------------

        self.validate_pokemon_availability(
            pokemon_set,
            version_group,
            result,
        )

        self.validate_moves(
            pokemon_set,
            version_group,
            result,
        )

        self.validate_ability(
            pokemon_set,
            result,
        )

        self.validate_item(
            pokemon_set,
            result,
        )

        return result