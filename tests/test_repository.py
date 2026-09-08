from pokeagent.repository import PokemonRepository


def test_repository_loads_all_kanto_pokemon() -> None:
    repo = PokemonRepository()
    pokemon = repo.get_all()

    assert len(pokemon) == 151
    assert pokemon[0].id == 1
    assert pokemon[0].name == "bulbasaur"
    assert pokemon[-1].id == 151
    assert pokemon[-1].name == "mew"


def test_get_pokemon_by_id() -> None:
    repo = PokemonRepository()

    pikachu = repo.get_by_id(25)

    assert pikachu is not None
    assert pikachu.id == 25
    assert pikachu.name == "pikachu"
    assert pikachu.types == ["electric"]


def test_get_pokemon_by_name_is_case_insensitive() -> None:
    repo = PokemonRepository()

    pikachu = repo.get_by_name("PIKACHU")

    assert pikachu is not None
    assert pikachu.id == 25
    assert pikachu.name == "pikachu"


def test_missing_pokemon_returns_none() -> None:
    repo = PokemonRepository()

    assert repo.get_by_id(999) is None
    assert repo.get_by_name("inventadomon") is None