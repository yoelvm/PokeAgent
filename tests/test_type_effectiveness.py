from pokeagent.type_effectiveness import (
    classify_type_effectiveness,
    get_type_defensive_multipliers,
)


def test_dual_type_defensive_multipliers(
    monkeypatch,
) -> None:
    type_data = {
        "fire": {
            "damage_relations": {
                "double_damage_from": [
                    {"name": "ground"},
                    {"name": "rock"},
                    {"name": "water"},
                ],
                "half_damage_from": [
                    {"name": "bug"},
                    {"name": "steel"},
                    {"name": "fire"},
                    {"name": "grass"},
                    {"name": "ice"},
                    {"name": "fairy"},
                ],
                "no_damage_from": [],
            },
        },
        "flying": {
            "damage_relations": {
                "double_damage_from": [
                    {"name": "rock"},
                    {"name": "electric"},
                    {"name": "ice"},
                ],
                "half_damage_from": [
                    {"name": "fighting"},
                    {"name": "bug"},
                    {"name": "grass"},
                ],
                "no_damage_from": [
                    {"name": "ground"},
                ],
            },
        },
    }

    monkeypatch.setattr(
        "pokeagent.type_effectiveness.get_type",
        lambda pokemon_type: type_data[pokemon_type],
    )

    multipliers = get_type_defensive_multipliers(
        ["fire", "flying"]
    )

    assert multipliers["rock"] == 4.0
    assert multipliers["water"] == 2.0
    assert multipliers["electric"] == 2.0
    assert multipliers["grass"] == 0.25
    assert multipliers["bug"] == 0.25
    assert multipliers["ice"] == 1.0
    assert multipliers["ground"] == 0.0


def test_classify_type_effectiveness() -> None:
    multipliers = {
        "water": 2.0,
        "rock": 4.0,
        "fire": 0.5,
        "grass": 0.25,
        "ground": 0.0,
        "normal": 1.0,
    }

    effectiveness = classify_type_effectiveness(
        multipliers
    )

    assert effectiveness["weaknesses"] == {
        "water": 2.0,
        "rock": 4.0,
    }

    assert effectiveness["resistances"] == {
        "fire": 0.5,
        "grass": 0.25,
    }

    assert effectiveness["immunities"] == {
        "ground": 0.0,
    }