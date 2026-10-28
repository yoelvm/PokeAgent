from pokeagent.models import Pokemon
from pokeagent.repository import PokemonRepository
from pokeagent.service import PokedexService


def make_garchomp() -> Pokemon:
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


def test_repository_loads_national_pokemon_by_id(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "pokeagent.repository.get_pokemon",
        lambda pokemon_id: {
            "id": pokemon_id,
        },
    )

    monkeypatch.setattr(
        "pokeagent.repository.pokemon_from_api_data",
        lambda data: make_garchomp(),
    )

    repository = PokemonRepository()

    pokemon = repository.get_by_id(
        445
    )

    assert pokemon is not None
    assert pokemon.id == 445
    assert pokemon.name == "garchomp"
    assert pokemon.types == [
        "dragon",
        "ground",
    ]


def test_repository_loads_national_pokemon_by_name(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "pokeagent.repository.get_pokemon",
        lambda pokemon_id: {
            "id": pokemon_id,
        },
    )

    monkeypatch.setattr(
        "pokeagent.repository.pokemon_from_api_data",
        lambda data: make_garchomp(),
    )

    repository = PokemonRepository()

    pokemon = repository.get_by_name(
        "garchomp"
    )

    assert pokemon is not None
    assert pokemon.id == 445
    assert pokemon.name == "garchomp"


def test_repository_caches_remote_pokemon(
    monkeypatch,
) -> None:
    calls = []

    def fake_get_pokemon(
        pokemon_id: int,
    ) -> dict:
        calls.append(
            pokemon_id
        )

        return {
            "id": pokemon_id,
        }

    monkeypatch.setattr(
        "pokeagent.repository.get_pokemon",
        fake_get_pokemon,
    )

    monkeypatch.setattr(
        "pokeagent.repository.pokemon_from_api_data",
        lambda data: make_garchomp(),
    )

    repository = PokemonRepository()

    first = repository.get_by_id(
        445
    )

    second = repository.get_by_id(
        445
    )

    assert first is second

    assert calls == [
        445,
    ]


def test_find_by_two_types_uses_intersection(
    monkeypatch,
) -> None:
    service = PokedexService()

    entries = {
        "garchomp": {
            "id": 445,
            "name": "garchomp",
        },
        "flygon": {
            "id": 330,
            "name": "flygon",
        },
        "dragonite": {
            "id": 149,
            "name": "dragonite",
        },
        "diglett": {
            "id": 50,
            "name": "diglett",
        },
    }

    monkeypatch.setattr(
        service.repository,
        "get_index_entry_by_name",
        lambda name: entries.get(name),
    )

    def fake_get_type(
        pokemon_type: str,
    ) -> dict:
        if pokemon_type == "dragon":
            names = [
                "garchomp",
                "flygon",
                "dragonite",
            ]
        else:
            names = [
                "garchomp",
                "flygon",
                "diglett",
            ]

        return {
            "pokemon": [
                {
                    "pokemon": {
                        "name": name,
                    }
                }
                for name in names
            ]
        }

    monkeypatch.setattr(
        "pokeagent.service.get_type",
        fake_get_type,
    )

    results = service.find_by_types(
        "dragon",
        "ground",
    )

    assert results == [
        {
            "id": 330,
            "name": "flygon",
        },
        {
            "id": 445,
            "name": "garchomp",
        },
    ]


def test_find_by_single_type(
    monkeypatch,
) -> None:
    service = PokedexService()

    entries = {
        "pikachu": {
            "id": 25,
            "name": "pikachu",
        },
        "pichu": {
            "id": 172,
            "name": "pichu",
        },
    }

    monkeypatch.setattr(
        service.repository,
        "get_index_entry_by_name",
        lambda name: entries.get(name),
    )

    monkeypatch.setattr(
        "pokeagent.service.get_type",
        lambda pokemon_type: {
            "pokemon": [
                {
                    "pokemon": {
                        "name": "pikachu",
                    }
                },
                {
                    "pokemon": {
                        "name": "pichu",
                    }
                },
            ]
        },
    )

    results = service.find_by_types(
        "electric"
    )

    assert results == [
        {
            "id": 25,
            "name": "pikachu",
        },
        {
            "id": 172,
            "name": "pichu",
        },
    ]


def test_find_by_generation(
    monkeypatch,
) -> None:
    service = PokedexService()

    entries = {
        "gible": {
            "id": 443,
            "name": "gible",
        },
        "gabite": {
            "id": 444,
            "name": "gabite",
        },
        "garchomp": {
            "id": 445,
            "name": "garchomp",
        },
    }

    monkeypatch.setattr(
        service.repository,
        "get_index_entry_by_name",
        lambda name: entries.get(name),
    )

    monkeypatch.setattr(
        "pokeagent.service.get_generation",
        lambda generation: {
            "pokemon_species": [
                {
                    "name": "garchomp",
                },
                {
                    "name": "gible",
                },
                {
                    "name": "gabite",
                },
            ]
        },
    )

    results = service.find_by_generation(
        4
    )

    assert results == [
        {
            "id": 443,
            "name": "gible",
        },
        {
            "id": 444,
            "name": "gabite",
        },
        {
            "id": 445,
            "name": "garchomp",
        },
    ]