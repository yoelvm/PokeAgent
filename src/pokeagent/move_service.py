from __future__ import annotations

from pokeagent.api import get_move, get_pokemon
from pokeagent.models import (
    LearnsetEntry,
    LearnsetMove,
    Move,
)

class MoveService:
    """Provide Pokémon move operations."""

    def find_move(
        self,
        name_or_id: str | int,
     ) -> Move:
        """Find a move by name or PokéAPI ID."""
        data = get_move(name_or_id)

        return Move.from_dict(data)
    def get_learnable_move_names(
        self,
        pokemon_query: str | int,
        version_group: str,
        method: str | None = None,
     ) -> list[str]:
        """Return moves learnable in a specific game version group."""
        pokemon_data = get_pokemon(pokemon_query)

        normalized_version = version_group.strip().lower()
        normalized_method = (
            method.strip().lower()
            if method is not None
            else None
        )

        move_names = []

        for move_data in pokemon_data["moves"]:
            for detail in move_data["version_group_details"]:
                detail_version = detail["version_group"]["name"]
                detail_method = detail["move_learn_method"]["name"]

                version_matches = (
                    detail_version == normalized_version
                )

                method_matches = (
                    normalized_method is None
                    or detail_method == normalized_method
                )

                if version_matches and method_matches:
                    move_names.append(
                        move_data["move"]["name"]
                    )
                    break

        return move_names
    def get_learnset(
        self,
        pokemon_query: str | int,
        version_group: str,
        method: str | None = None,
     ) -> list[LearnsetEntry]:
        """Return detailed learnset entries for a version group."""
        pokemon_data = get_pokemon(pokemon_query)

        normalized_version = version_group.strip().lower()
        normalized_method = (
            method.strip().lower()
            if method is not None
            else None
        )

        entries = []

        for move_data in pokemon_data["moves"]:
            move_name = move_data["move"]["name"]

            for detail in move_data["version_group_details"]:
                detail_version = detail["version_group"]["name"]
                detail_method = detail["move_learn_method"]["name"]

                version_matches = (
                    detail_version == normalized_version
                )

                method_matches = (
                    normalized_method is None
                    or detail_method == normalized_method
                )

                if version_matches and method_matches:
                    entries.append(
                        LearnsetEntry(
                            move_name=move_name,
                            version_group=detail_version,
                            method=detail_method,
                            level_learned_at=detail["level_learned_at"],
                        )
                    )

        return entries
    def get_detailed_learnset(
        self,
        pokemon_query: str | int,
        version_group: str,
        method: str | None = None,
     ) -> list[LearnsetMove]:
        """Return learnset entries with complete move data."""
        entries = self.get_learnset(
            pokemon_query,
            version_group,
            method,
        )

        detailed_entries = []

        for entry in entries:
            move = self.find_move(entry.move_name)

            detailed_entries.append(
                LearnsetMove(
                    move=move,
                    version_group=entry.version_group,
                    method=entry.method,
                    level_learned_at=entry.level_learned_at,
                )
            )

        return detailed_entries