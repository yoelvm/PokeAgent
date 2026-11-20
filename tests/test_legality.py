from pokeagent.api import PokeAPIError
from pokeagent.legality_service import LegalityService
from pokeagent.models import (
    LegalityResult,
    Pokemon,
    PokemonSet,
    Team,
)


def make_pokemon(
    pokemon_id: int = 25,
    name: str = "pikachu",
) -> Pokemon:
    return Pokemon(
        id=pokemon_id,
        name=name,
        height=4,
        weight=60,
        base_experience=112,
        types=["electric"],
        abilities=[
            "static",
            "lightning-rod",
        ],
        stats={
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "special-attack": 50,
            "special-defense": 50,
            "speed": 90,
        },
        hidden_abilities=[
            "lightning-rod",
        ],
    )


def test_legality_result_distinguishes_warnings_and_errors() -> None:
    result = LegalityResult()

    result.add_warning(
        "test-warning",
        "Warning.",
    )

    assert result.is_legal is True
    assert len(result.warnings) == 1
    assert len(result.errors) == 0

    result.add_error(
        "test-error",
        "Error.",
    )

    assert result.is_legal is False
    assert len(result.warnings) == 1
    assert len(result.errors) == 1


def test_unavailable_pokemon_is_illegal(
    monkeypatch,
) -> None:
    pokemon_set = PokemonSet(
        make_pokemon(
            445,
            "garchomp",
        )
    )

    service = LegalityService()

    monkeypatch.setattr(
        service.game_data,
        "is_pokemon_available",
        lambda pokemon_id, version_group: False,
    )

    result = (
        service.validate_pokemon_availability(
            pokemon_set,
            "red-blue",
        )
    )

    assert result.is_legal is False

    assert [
        issue.code
        for issue in result.errors
    ] == [
        "pokemon-unavailable",
    ]


def test_move_must_be_legal_in_version_group(
    monkeypatch,
) -> None:
    pokemon_set = PokemonSet(
        make_pokemon()
    )

    pokemon_set.moves = [
        "quick-attack",
        "spore",
    ]

    service = LegalityService()

    monkeypatch.setattr(
        service.moves,
        "get_learnable_move_names",
        lambda pokemon_id, version_group: [
            "quick-attack",
        ],
    )

    result = service.validate_moves(
        pokemon_set,
        "red-blue",
    )

    assert result.is_legal is False

    assert len(result.errors) == 1
    assert result.errors[0].code == "illegal-move"

    assert "spore" in (
        result.errors[0].message
    )


def test_ability_validation() -> None:
    pokemon_set = PokemonSet(
        make_pokemon()
    )

    service = LegalityService()

    pokemon_set.ability = (
        "lightning-rod"
    )

    valid_result = (
        service.validate_ability(
            pokemon_set
        )
    )

    assert valid_result.is_legal is True
    assert valid_result.issues == []

    pokemon_set.ability = "blaze"

    invalid_result = (
        service.validate_ability(
            pokemon_set
        )
    )

    assert invalid_result.is_legal is False

    assert invalid_result.errors[
        0
    ].code == "illegal-ability"


def test_item_validation(
    monkeypatch,
) -> None:
    pokemon_set = PokemonSet(
        make_pokemon()
    )

    service = LegalityService()

    pokemon_set.item = None

    missing_result = (
        service.validate_item(
            pokemon_set
        )
    )

    assert missing_result.is_legal is True

    assert missing_result.warnings[
        0
    ].code == "missing-item"

    pokemon_set.item = (
        "not-a-real-item"
    )

    def raise_invalid_item(
        item_query,
    ):
        raise PokeAPIError(
            "Item not found."
        )

    monkeypatch.setattr(
        service.items,
        "find_item",
        raise_invalid_item,
    )

    invalid_result = (
        service.validate_item(
            pokemon_set
        )
    )

    assert invalid_result.is_legal is False

    assert invalid_result.errors[
        0
    ].code == "invalid-item"


def test_validate_set_accumulates_problems(
    monkeypatch,
) -> None:
    pokemon_set = PokemonSet(
        make_pokemon(
            445,
            "garchomp",
        )
    )

    pokemon_set.level = 101
    pokemon_set.ability = "blaze"
    pokemon_set.item = None

    pokemon_set.moves = [
        "earthquake",
        "earthquake",
        "spore",
        "protect",
        "tackle",
    ]

    pokemon_set.training.evs = {
        "hp": 252,
        "attack": 252,
        "defense": 0,
        "special-attack": 0,
        "special-defense": 0,
        "speed": 252,
    }

    service = LegalityService()

    monkeypatch.setattr(
        service.game_data,
        "is_pokemon_available",
        lambda pokemon_id, version_group: False,
    )

    monkeypatch.setattr(
        service.moves,
        "get_learnable_move_names",
        lambda pokemon_id, version_group: [],
    )

    result = service.validate_set(
        pokemon_set,
        "red-blue",
    )

    codes = {
        issue.code
        for issue in result.issues
    }

    assert result.is_legal is False

    assert "invalid-level" in codes
    assert "invalid-training" in codes
    assert "too-many-moves" in codes
    assert "duplicate-moves" in codes
    assert "pokemon-unavailable" in codes
    assert "illegal-move" in codes
    assert "illegal-ability" in codes
    assert "missing-item" in codes


def test_incomplete_team_can_remain_legal(
    monkeypatch,
) -> None:
    team = Team()

    pokemon = make_pokemon()

    team.add(
        pokemon
    )

    pokemon_set = team.get_set(
        pokemon.id
    )

    pokemon_set.moves = [
        "quick-attack",
    ]

    pokemon_set.item = "potion"

    service = LegalityService()

    monkeypatch.setattr(
        service.game_data,
        "is_pokemon_available",
        lambda pokemon_id, version_group: True,
    )

    monkeypatch.setattr(
        service.moves,
        "get_learnable_move_names",
        lambda pokemon_id, version_group: [
            "quick-attack",
        ],
    )

    monkeypatch.setattr(
        service.items,
        "find_item",
        lambda item_query: object(),
    )

    result = service.validate_team(
        team,
        "red-blue",
    )

    assert result.is_legal is True

    assert result.warnings[
        0
    ].code == "incomplete-team"

    assert result.member_results[
        25
    ].is_legal is True


def test_illegal_member_makes_team_illegal(
    monkeypatch,
) -> None:
    team = Team()

    pikachu = make_pokemon(
        25,
        "pikachu",
    )

    garchomp = make_pokemon(
        445,
        "garchomp",
    )

    team.add(
        pikachu
    )

    team.add(
        garchomp
    )

    team.get_set(
        25
    ).moves = [
        "quick-attack",
    ]

    team.get_set(
        25
    ).item = "potion"

    team.get_set(
        445
    ).moves = [
        "earthquake",
    ]

    team.get_set(
        445
    ).item = "leftovers"

    service = LegalityService()

    def fake_availability(
        pokemon_id,
        version_group,
    ):
        return pokemon_id == 25

    def fake_learnset(
        pokemon_id,
        version_group,
    ):
        if pokemon_id == 25:
            return [
                "quick-attack",
            ]

        return []

    monkeypatch.setattr(
        service.game_data,
        "is_pokemon_available",
        fake_availability,
    )

    monkeypatch.setattr(
        service.moves,
        "get_learnable_move_names",
        fake_learnset,
    )

    monkeypatch.setattr(
        service.items,
        "find_item",
        lambda item_query: object(),
    )

    result = service.validate_team(
        team,
        "red-blue",
    )

    assert result.is_legal is False

    assert result.member_results[
        25
    ].is_legal is True

    assert result.member_results[
        445
    ].is_legal is False

    garchomp_codes = {
        issue.code
        for issue
        in result.member_results[
            445
        ].issues
    }

    assert (
        "pokemon-unavailable"
        in garchomp_codes
    )

    assert (
        "illegal-move"
        in garchomp_codes
    )
