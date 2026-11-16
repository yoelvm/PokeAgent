from pokeagent.models import (
    Item,
    Move,
    Pokemon,
    PokemonSet,
    Team,
)
from pokeagent.team_service import TeamService


def make_pokemon() -> Pokemon:
    """Create a Pokémon for advanced team tests."""
    return Pokemon(
        id=445,
        name="garchomp",
        height=19,
        weight=950,
        base_experience=300,
        types=[
            "dragon",
            "ground",
        ],
        abilities=[
            "sand-veil",
            "rough-skin",
        ],
        stats={
            "hp": 108,
            "attack": 130,
            "defense": 95,
            "special-attack": 80,
            "special-defense": 85,
            "speed": 102,
        },
        hidden_abilities=[
            "rough-skin",
        ],
    )


def make_move(
    name: str,
) -> Move:
    """Create a move for team tests."""
    return Move(
        id=1,
        name=name,
        type="normal",
        power=80,
        accuracy=100,
        pp=15,
        damage_class="physical",
    )


def test_pokemon_set_has_competitive_defaults() -> None:
    pokemon = make_pokemon()

    pokemon_set = PokemonSet(
        pokemon=pokemon
    )

    assert pokemon_set.pokemon is pokemon
    assert pokemon_set.level == 50
    assert pokemon_set.nature == "hardy"
    assert pokemon_set.ability == "sand-veil"
    assert pokemon_set.item is None
    assert pokemon_set.moves == []

    assert pokemon_set.training.ivs == {
        "hp": 31,
        "attack": 31,
        "defense": 31,
        "special-attack": 31,
        "special-defense": 31,
        "speed": 31,
    }

    assert pokemon_set.training.evs == {
        "hp": 0,
        "attack": 0,
        "defense": 0,
        "special-attack": 0,
        "special-defense": 0,
        "speed": 0,
    }


def test_team_creates_and_removes_pokemon_set() -> None:
    pokemon = make_pokemon()
    team = Team()

    assert team.add(pokemon) is True

    pokemon_set = team.get_set(
        445
    )

    assert pokemon_set is not None
    assert pokemon_set.pokemon is pokemon

    assert team.remove(445) is True

    assert team.members == []
    assert team.get_set(445) is None


def test_team_service_sets_ability() -> None:
    pokemon = make_pokemon()
    team = Team()
    service = TeamService()

    team.add(pokemon)

    success, _ = service.set_ability(
        team,
        445,
        "rough skin",
    )

    assert success is True
    assert (
        team.get_set(445).ability
        == "rough-skin"
    )

    success, _ = service.set_ability(
        team,
        445,
        "blaze",
    )

    assert success is False

    assert (
        team.get_set(445).ability
        == "rough-skin"
    )


def test_team_service_sets_and_clears_item(
    monkeypatch,
) -> None:
    pokemon = make_pokemon()
    team = Team()
    service = TeamService()

    team.add(pokemon)

    leftovers = Item(
        id=234,
        name="leftovers",
        category="held-items",
        effect="Restores HP.",
        image_url=None,
    )

    monkeypatch.setattr(
        service.items,
        "find_item",
        lambda query: leftovers,
    )

    success, _ = service.set_item(
        team,
        445,
        "leftovers",
    )

    assert success is True

    assert (
        team.get_set(445).item
        == "leftovers"
    )

    success, _ = service.clear_item(
        team,
        445,
    )

    assert success is True
    assert team.get_set(445).item is None


def test_team_service_adds_compatible_move(
    monkeypatch,
) -> None:
    pokemon = make_pokemon()
    team = Team()
    service = TeamService()

    team.add(pokemon)

    monkeypatch.setattr(
        service.moves,
        "find_move",
        lambda query: make_move(
            "earthquake"
        ),
    )

    monkeypatch.setattr(
        service.moves,
        "can_learn_move",
        lambda pokemon_id, move_name: True,
    )

    success, _ = service.add_move(
        team,
        445,
        "earthquake",
    )

    assert success is True

    assert team.get_set(445).moves == [
        "earthquake",
    ]

    duplicate_success, _ = (
        service.add_move(
            team,
            445,
            "earthquake",
        )
    )

    assert duplicate_success is False

    assert team.get_set(445).moves == [
        "earthquake",
    ]


def test_team_service_rejects_incompatible_move(
    monkeypatch,
) -> None:
    pokemon = make_pokemon()
    team = Team()
    service = TeamService()

    team.add(pokemon)

    monkeypatch.setattr(
        service.moves,
        "find_move",
        lambda query: make_move(
            "spore"
        ),
    )

    monkeypatch.setattr(
        service.moves,
        "can_learn_move",
        lambda pokemon_id, move_name: False,
    )

    success, message = service.add_move(
        team,
        445,
        "spore",
    )

    assert success is False

    assert message == (
        "garchomp cannot learn spore."
    )

    assert team.get_set(445).moves == []


def test_team_service_limits_moves_to_four(
    monkeypatch,
) -> None:
    pokemon = make_pokemon()
    team = Team()
    service = TeamService()

    team.add(pokemon)

    monkeypatch.setattr(
        service.moves,
        "find_move",
        lambda query: make_move(
            str(query)
        ),
    )

    monkeypatch.setattr(
        service.moves,
        "can_learn_move",
        lambda pokemon_id, move_name: True,
    )

    for move_name in [
        "earthquake",
        "dragon-claw",
        "stone-edge",
        "iron-head",
    ]:
        success, _ = service.add_move(
            team,
            445,
            move_name,
        )

        assert success is True

    success, message = service.add_move(
        team,
        445,
        "protect",
    )

    assert success is False

    assert message == (
        "A Pokémon cannot have "
        "more than four moves."
    )

    assert len(
        team.get_set(445).moves
    ) == 4


def test_team_service_sets_level_and_nature() -> None:
    pokemon = make_pokemon()
    team = Team()
    service = TeamService()

    team.add(pokemon)

    level_success, _ = (
        service.set_level(
            team,
            445,
            100,
        )
    )

    nature_success, _ = (
        service.set_nature(
            team,
            445,
            "jolly",
        )
    )

    pokemon_set = team.get_set(
        445
    )

    assert level_success is True
    assert nature_success is True

    assert pokemon_set.level == 100
    assert pokemon_set.nature == "jolly"

    invalid_level, _ = (
        service.set_level(
            team,
            445,
            101,
        )
    )

    assert invalid_level is False
    assert pokemon_set.level == 100


def test_team_service_validates_training() -> None:
    pokemon = make_pokemon()
    team = Team()
    service = TeamService()

    team.add(pokemon)

    ivs = {
        "hp": 31,
        "attack": 31,
        "defense": 31,
        "special-attack": 31,
        "special-defense": 31,
        "speed": 31,
    }

    evs = {
        "hp": 0,
        "attack": 252,
        "defense": 0,
        "special-attack": 0,
        "special-defense": 4,
        "speed": 252,
    }

    success, _ = service.set_training(
        team,
        445,
        ivs,
        evs,
    )

    assert success is True

    pokemon_set = team.get_set(
        445
    )

    assert pokemon_set.training.ivs == ivs
    assert pokemon_set.training.evs == evs

    invalid_evs = {
        "hp": 252,
        "attack": 252,
        "defense": 0,
        "special-attack": 0,
        "special-defense": 0,
        "speed": 252,
    }

    success, message = (
        service.set_training(
            team,
            445,
            ivs,
            invalid_evs,
        )
    )

    assert success is False

    assert message == (
        "Total EVs cannot exceed 510."
    )

    # Previous valid training must remain untouched.
    assert pokemon_set.training.evs == evs