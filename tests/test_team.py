from pokeagent.models import Pokemon, Team
from pokeagent.team_service import TeamService


def make_pokemon(
    pokemon_id: int,
    name: str,
    types: list[str],
) -> Pokemon:
    return Pokemon(
        id=pokemon_id,
        name=name,
        height=10,
        weight=100,
        base_experience=100,
        types=types,
        abilities=[],
        stats={},
    )


def test_team_add_and_remove() -> None:
    team = Team()
    pikachu = make_pokemon(
        25,
        "pikachu",
        ["electric"],
    )

    assert team.add(pikachu) is True
    assert len(team.members) == 1

    assert team.remove(25) is True
    assert team.members == []


def test_team_rejects_duplicates() -> None:
    team = Team()
    pikachu = make_pokemon(
        25,
        "pikachu",
        ["electric"],
    )

    assert team.add(pikachu) is True
    assert team.add(pikachu) is False
    assert len(team.members) == 1


def test_team_has_maximum_six_members() -> None:
    team = Team()

    for pokemon_id in range(1, 7):
        pokemon = make_pokemon(
            pokemon_id,
            f"pokemon-{pokemon_id}",
            ["normal"],
        )

        assert team.add(pokemon) is True

    seventh = make_pokemon(
        7,
        "pokemon-7",
        ["normal"],
    )

    assert team.is_full is True
    assert team.add(seventh) is False
    assert len(team.members) == 6


def test_team_service_rejects_duplicate(
    monkeypatch,
) -> None:
    team = Team()
    service = TeamService()

    pikachu = make_pokemon(
        25,
        "pikachu",
        ["electric"],
    )

    monkeypatch.setattr(
        service.pokedex,
        "find_pokemon",
        lambda query: pikachu,
    )

    first_result = service.add_pokemon(
        team,
        "pikachu",
    )

    second_result = service.add_pokemon(
        team,
        "pikachu",
    )

    assert first_result[0] is True
    assert second_result[0] is False
    assert len(team.members) == 1


def test_shared_weaknesses(
    monkeypatch,
) -> None:
    team = Team(
        members=[
            make_pokemon(
                1,
                "pokemon-one",
                ["fire"],
            ),
            make_pokemon(
                2,
                "pokemon-two",
                ["flying"],
            ),
        ]
    )

    service = TeamService()

    def fake_multipliers(
        pokemon_types: list[str],
    ) -> dict[str, float]:
        if pokemon_types == ["fire"]:
            return {
                "rock": 2.0,
                "water": 2.0,
            }

        return {
            "rock": 2.0,
            "electric": 2.0,
        }

    monkeypatch.setattr(
        "pokeagent.team_service."
        "get_type_defensive_multipliers",
        fake_multipliers,
    )

    shared = service.get_shared_weaknesses(
        team
    )

    assert shared == {
        "rock": 2,
    }