from pokeagent.models import Pokemon


def test_pokemon_from_dict() -> None:
    data = {
        "id": 25,
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "base_experience": 112,
        "types": ["electric"],
        "abilities": ["static", "lightning-rod"],
        "stats": {
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "special-attack": 50,
            "special-defense": 50,
            "speed": 90,
        },
    }

    pikachu = Pokemon.from_dict(data)

    assert pikachu.id == 25
    assert pikachu.name == "pikachu"
    assert pikachu.types == ["electric"]
    assert pikachu.stats["speed"] == 90


def test_pokemon_converts_height_and_weight() -> None:
    pikachu = Pokemon(
        id=25,
        name="pikachu",
        height=4,
        weight=60,
        base_experience=112,
        types=["electric"],
        abilities=["static"],
        stats={"speed": 90},
    )

    assert pikachu.height_m == 0.4
    assert pikachu.weight_kg == 6.0
def test_pokemon_from_dict_includes_image_url() -> None:
        data = {
            "id": 25,
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "base_experience": 112,
            "types": ["electric"],
            "abilities": ["static"],
            "stats": {"speed": 90},
            "image_url": "https://example.com/pikachu.png",
        }

        pikachu = Pokemon.from_dict(data)

        assert pikachu.image_url == "https://example.com/pikachu.png"    