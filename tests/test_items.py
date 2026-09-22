from pokeagent.item_service import ItemService
from pokeagent.models import Item


def test_item_from_dict() -> None:
    data = {
        "id": 17,
        "name": "potion",
        "category": {
            "name": "healing",
        },
        "effect_entries": [
            {
                "short_effect": "Restores 20 HP.",
                "language": {
                    "name": "en",
                },
            },
        ],
        "sprites": {
            "default": "https://example.com/potion.png",
        },
        "prices": [],
    }

    item = Item.from_dict(data)

    assert item.id == 17
    assert item.name == "potion"
    assert item.category == "healing"
    assert item.effect == "Restores 20 HP."
    assert item.image_url == "https://example.com/potion.png"
    assert item.prices == []


def test_item_handles_missing_optional_data() -> None:
    data = {
        "id": 1,
        "name": "test-item",
        "category": {
            "name": "other",
        },
        "effect_entries": [],
        "sprites": {},
    }

    item = Item.from_dict(data)

    assert item.effect == ""
    assert item.image_url is None
    assert item.prices == []


def test_item_service_returns_item(
    monkeypatch,
) -> None:
    data = {
        "id": 17,
        "name": "potion",
        "category": {
            "name": "healing",
        },
        "effect_entries": [
            {
                "short_effect": "Restores 20 HP.",
                "language": {
                    "name": "en",
                },
            },
        ],
        "sprites": {
            "default": "https://example.com/potion.png",
        },
        "prices": [],
    }

    monkeypatch.setattr(
        "pokeagent.item_service.get_item",
        lambda query: data,
    )

    service = ItemService()

    item = service.find_item("potion")

    assert item.name == "potion"
    assert item.category == "healing"
    assert item.effect == "Restores 20 HP."