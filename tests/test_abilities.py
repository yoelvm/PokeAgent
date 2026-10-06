from pokeagent.ability_service import AbilityService
from pokeagent.api import get_ability
from pokeagent.models import Ability, Pokemon


class FakeResponse:
    status_code = 200

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {}


def test_ability_from_dict() -> None:
    data = {
        "id": 9,
        "name": "static",
        "generation": {
            "name": "generation-iii",
        },
        "effect_entries": [
            {
                "short_effect": (
                    "Has a 30% chance of paralyzing "
                    "attacking Pokémon on contact."
                ),
                "language": {
                    "name": "en",
                },
            },
        ],
    }

    ability = Ability.from_dict(data)

    assert ability.id == 9
    assert ability.name == "static"
    assert ability.generation == "generation-iii"
    assert (
        ability.effect
        == (
            "Has a 30% chance of paralyzing "
            "attacking Pokémon on contact."
        )
    )


def test_ability_handles_missing_english_effect() -> None:
    data = {
        "id": 9,
        "name": "static",
        "generation": {
            "name": "generation-iii",
        },
        "effect_entries": [],
    }

    ability = Ability.from_dict(data)

    assert ability.effect == ""


def test_ability_service_returns_ability(
    monkeypatch,
) -> None:
    data = {
        "id": 31,
        "name": "lightning-rod",
        "generation": {
            "name": "generation-iii",
        },
        "effect_entries": [
            {
                "short_effect": (
                    "Redirects Electric moves."
                ),
                "language": {
                    "name": "en",
                },
            },
        ],
    }

    monkeypatch.setattr(
        "pokeagent.ability_service.get_ability",
        lambda query: data,
    )

    service = AbilityService()

    ability = service.find_ability(
        "lightning rod"
    )

    assert ability.id == 31
    assert ability.name == "lightning-rod"
    assert ability.generation == "generation-iii"


def test_get_ability_converts_spaces_to_hyphens(
    monkeypatch,
) -> None:
    requested_urls = []

    def fake_get(url, timeout):
        requested_urls.append(url)
        return FakeResponse()

    monkeypatch.setattr(
        "pokeagent.api.requests.get",
        fake_get,
    )

    get_ability("lightning rod")

    assert requested_urls[0].endswith(
        "/ability/lightning-rod"
    )


def test_pokemon_from_dict_includes_hidden_abilities() -> None:
    data = {
        "id": 25,
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "base_experience": 112,
        "types": ["electric"],
        "abilities": [
            "static",
            "lightning-rod",
        ],
        "hidden_abilities": [
            "lightning-rod",
        ],
        "stats": {
            "speed": 90,
        },
        "image_url": (
            "https://example.com/pikachu.png"
        ),
        "evolutions": [
            "pikachu",
            "raichu",
        ],
    }

    pikachu = Pokemon.from_dict(data)

    assert pikachu.abilities == [
        "static",
        "lightning-rod",
    ]

    assert pikachu.hidden_abilities == [
        "lightning-rod",
    ]