from pokeagent.models import (
    LearnsetEntry,
    Move,
)
from pokeagent.move_service import MoveService


def test_move_from_dict() -> None:
    data = {
        "id": 85,
        "name": "thunderbolt",
        "type": {"name": "electric"},
        "power": 90,
        "accuracy": 100,
        "pp": 15,
        "damage_class": {"name": "special"},
    }

    move = Move.from_dict(data)

    assert move.id == 85
    assert move.name == "thunderbolt"
    assert move.type == "electric"
    assert move.power == 90
    assert move.accuracy == 100
    assert move.pp == 15
    assert move.damage_class == "special"


def test_move_supports_status_moves() -> None:
    data = {
        "id": 86,
        "name": "thunder-wave",
        "type": {"name": "electric"},
        "power": None,
        "accuracy": 90,
        "pp": 20,
        "damage_class": {"name": "status"},
    }

    move = Move.from_dict(data)

    assert move.power is None
    assert move.damage_class == "status"


def test_get_learnset_filters_game_and_method(
    monkeypatch,
) -> None:
    pokemon_data = {
        "moves": [
            {
                "move": {"name": "quick-attack"},
                "version_group_details": [
                    {
                        "level_learned_at": 16,
                        "version_group": {
                            "name": "red-blue",
                        },
                        "move_learn_method": {
                            "name": "level-up",
                        },
                    },
                    {
                        "level_learned_at": 11,
                        "version_group": {
                            "name": "yellow",
                        },
                        "move_learn_method": {
                            "name": "level-up",
                        },
                    },
                ],
            },
            {
                "move": {"name": "mega-punch"},
                "version_group_details": [
                    {
                        "level_learned_at": 0,
                        "version_group": {
                            "name": "red-blue",
                        },
                        "move_learn_method": {
                            "name": "machine",
                        },
                    },
                ],
            },
        ],
    }

    monkeypatch.setattr(
        "pokeagent.move_service.get_pokemon",
        lambda query: pokemon_data,
    )

    service = MoveService()

    entries = service.get_learnset(
        "pikachu",
        "red-blue",
        "level-up",
    )

    assert len(entries) == 1
    assert entries[0].move_name == "quick-attack"
    assert entries[0].version_group == "red-blue"
    assert entries[0].method == "level-up"
    assert entries[0].level_learned_at == 16


def test_get_detailed_learnset_combines_move_data(
    monkeypatch,
) -> None:
    service = MoveService()

    monkeypatch.setattr(
        MoveService,
        "get_learnset",
        lambda self, pokemon_query, version_group, method=None: [
            LearnsetEntry(
                move_name="quick-attack",
                version_group="red-blue",
                method="level-up",
                level_learned_at=16,
            )
        ],
    )

    monkeypatch.setattr(
        MoveService,
        "find_move",
        lambda self, name_or_id: Move(
            id=98,
            name="quick-attack",
            type="normal",
            power=40,
            accuracy=100,
            pp=30,
            damage_class="physical",
        ),
    )

    moves = service.get_detailed_learnset(
        "pikachu",
        "red-blue",
        "level-up",
    )

    assert len(moves) == 1

    learnset_move = moves[0]

    assert learnset_move.move.name == "quick-attack"
    assert learnset_move.move.power == 40
    assert learnset_move.version_group == "red-blue"
    assert learnset_move.method == "level-up"
    assert learnset_move.level_learned_at == 16