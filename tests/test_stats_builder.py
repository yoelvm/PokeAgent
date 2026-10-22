import pytest

from pokeagent.models import Pokemon, StatTraining
from pokeagent.natures import get_nature_modifier
from pokeagent.stat_calculator import (
    calculate_hp,
    calculate_pokemon_stats,
    calculate_stat,
)


def make_pikachu() -> Pokemon:
    return Pokemon(
        id=25,
        name="pikachu",
        height=4,
        weight=60,
        base_experience=112,
        types=["electric"],
        abilities=["static"],
        stats={
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "special-attack": 50,
            "special-defense": 50,
            "speed": 90,
        },
    )


def test_timid_nature_modifiers() -> None:
    assert get_nature_modifier(
        "timid",
        "attack",
    ) == 0.9

    assert get_nature_modifier(
        "timid",
        "speed",
    ) == 1.1

    assert get_nature_modifier(
        "timid",
        "defense",
    ) == 1.0


def test_stat_training_rejects_invalid_iv() -> None:
    training = StatTraining(
        ivs={
            "speed": 32,
        }
    )

    with pytest.raises(
        ValueError,
        match="IV for speed must be between 0 and 31",
    ):
        training.validate()


def test_stat_training_rejects_too_many_evs() -> None:
    training = StatTraining(
        evs={
            "hp": 252,
            "attack": 252,
            "speed": 252,
        }
    )

    with pytest.raises(
        ValueError,
        match="Total EVs cannot exceed 510",
    ):
        training.validate()


def test_calculate_pikachu_hp() -> None:
    assert calculate_hp(
        35,
        31,
        0,
        50,
    ) == 110


def test_calculate_pikachu_speed_with_timid() -> None:
    assert calculate_stat(
        90,
        31,
        252,
        50,
        "timid",
        "speed",
    ) == 156


def test_calculate_full_pikachu_stats() -> None:
    pikachu = make_pikachu()

    training = StatTraining(
        ivs={
            "hp": 31,
            "attack": 31,
            "defense": 31,
            "special-attack": 31,
            "special-defense": 31,
            "speed": 31,
        },
        evs={
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "special-attack": 252,
            "special-defense": 4,
            "speed": 252,
        },
    )

    stats = calculate_pokemon_stats(
        pikachu,
        training,
        50,
        "timid",
    )

    assert stats == {
        "hp": 110,
        "attack": 67,
        "defense": 60,
        "special-attack": 102,
        "special-defense": 71,
        "speed": 156,
    }


def test_calculate_stats_rejects_invalid_level() -> None:
    pikachu = make_pikachu()

    training = StatTraining()

    with pytest.raises(
        ValueError,
        match="Level must be between 1 and 100",
    ):
        calculate_pokemon_stats(
            pikachu,
            training,
            101,
            "hardy",
        )