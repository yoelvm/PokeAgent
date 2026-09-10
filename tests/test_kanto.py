from pokeagent.kanto import simplify_pokemon


def test_simplify_pokemon_includes_official_artwork() -> None:
    raw_pokemon = {
        "id": 25,
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "base_experience": 112,
        "types": [
            {"type": {"name": "electric"}},
        ],
        "abilities": [
            {"ability": {"name": "static"}},
        ],
        "stats": [
            {
                "base_stat": 90,
                "stat": {"name": "speed"},
            },
        ],
        "sprites": {
            "front_default": "https://example.com/sprite.png",
            "other": {
                "official-artwork": {
                    "front_default": (
                        "https://example.com/official.png"
                    ),
                },
            },
        },
    }

    pokemon = simplify_pokemon(raw_pokemon)

    assert pokemon["id"] == 25
    assert pokemon["name"] == "pikachu"
    assert pokemon["image_url"] == "https://example.com/official.png"