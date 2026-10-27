
from pokeagent.game_data_service import GameDataService
from pokeagent.models import GameVersionGroup


def test_game_version_group_from_dict() -> None:
    data = {
        "id": 25,
        "name": "scarlet-violet",
        "generation": {
            "name": "generation-ix",
        },
        "versions": [
            {
                "name": "scarlet",
            },
            {
                "name": "violet",
            },
        ],
    }

    group = GameVersionGroup.from_dict(data)

    assert group.id == 25
    assert group.name == "scarlet-violet"
    assert group.generation == "generation-ix"
    assert group.versions == [
        "scarlet",
        "violet",
    ]


def test_game_data_service_returns_version_group(
    monkeypatch,
) -> None:
    data = {
        "id": 1,
        "name": "red-blue",
        "generation": {
            "name": "generation-i",
        },
        "versions": [
            {
                "name": "red",
            },
            {
                "name": "blue",
            },
        ],
    }

    monkeypatch.setattr(
        "pokeagent.game_data_service.get_version_group",
        lambda query: data,
    )

    service = GameDataService()

    group = service.find_version_group(
        "red blue"
    )

    assert group.name == "red-blue"
    assert group.generation == "generation-i"
    assert group.versions == [
        "red",
        "blue",
    ]


def test_contains_version() -> None:
    service = GameDataService()

    group = GameVersionGroup(
        id=25,
        name="scarlet-violet",
        generation="generation-ix",
        versions=[
            "scarlet",
            "violet",
        ],
    )

    assert (
        service.contains_version(
            group,
            "scarlet",
        )
        is True
    )

    assert (
        service.contains_version(
            group,
            "violet",
        )
        is True
    )

    assert (
        service.contains_version(
            group,
            "sword",
        )
        is False
    )


def test_pokemon_availability(
    monkeypatch,
) -> None:
    service = GameDataService()

    group = GameVersionGroup(
        id=25,
        name="scarlet-violet",
        generation="generation-ix",
        versions=[
            "scarlet",
            "violet",
        ],
    )

    monkeypatch.setattr(
        service,
        "find_version_group",
        lambda query: group,
    )

    monkeypatch.setattr(
        "pokeagent.game_data_service."
        "get_pokemon_version_names",
        lambda query: [
            "scarlet",
            "violet",
        ],
    )

    assert (
        service.is_pokemon_available(
            "pikachu",
            "scarlet violet",
        )
        is True
    )


def test_pokemon_not_available(
    monkeypatch,
) -> None:
    service = GameDataService()

    group = GameVersionGroup(
        id=1,
        name="red-blue",
        generation="generation-i",
        versions=[
            "red",
            "blue",
        ],
    )

    monkeypatch.setattr(
        service,
        "find_version_group",
        lambda query: group,
    )

    monkeypatch.setattr(
        "pokeagent.game_data_service."
        "get_pokemon_version_names",
        lambda query: [
            "scarlet",
            "violet",
        ],
    )

    assert (
        service.is_pokemon_available(
            "garchomp",
            "red blue",
        )
        is False
    )