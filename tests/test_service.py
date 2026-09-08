import pytest

from pokeagent.service import PokedexService


def test_find_pokemon_by_id_name_and_numeric_string() -> None:
    service = PokedexService()

    by_id = service.find_pokemon(25)
    by_name = service.find_pokemon("PIKACHU")
    by_numeric_string = service.find_pokemon("25")

    assert by_id is not None
    assert by_name is not None
    assert by_numeric_string is not None

    assert by_id.name == "pikachu"
    assert by_name.id == 25
    assert by_numeric_string.name == "pikachu"


def test_find_pokemon_by_type() -> None:
    service = PokedexService()

    pokemon = service.find_by_type("ELECTRIC")
    names = [item.name for item in pokemon]

    assert len(pokemon) == 9
    assert "pikachu" in names
    assert "jolteon" in names
    assert "zapdos" in names


def test_find_by_type_and_min_stat() -> None:
    service = PokedexService()

    pokemon = service.find_by_type_and_min_stat(
        "electric",
        "speed",
        120,
    )

    assert [item.name for item in pokemon] == [
        "electrode",
        "jolteon",
    ]


def test_invalid_stat_raises_value_error() -> None:
    service = PokedexService()

    with pytest.raises(ValueError, match="Unknown stat"):
        service.find_by_type_and_min_stat(
            "electric",
            "speeed",
            100,
        )