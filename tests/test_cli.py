from pokeagent.cli import format_label, format_pokemon
from pokeagent.models import Pokemon


def test_format_label() -> None:
    assert format_label("special-attack") == "Special Attack"
    assert format_label("lightning-rod") == "Lightning Rod"
    assert format_label("pikachu") == "Pikachu"


def test_format_pokemon() -> None:
    pikachu = Pokemon(
        id=25,
        name="pikachu",
        height=4,
        weight=60,
        base_experience=112,
        types=["electric"],
        abilities=["static", "lightning-rod"],
        stats={
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "special-attack": 50,
            "special-defense": 50,
            "speed": 90,
        },
    )

    output = format_pokemon(pikachu)

    assert "#025 Pikachu" in output
    assert "Type: Electric" in output
    assert "Height: 0.4 m" in output
    assert "Weight: 6.0 kg" in output
    assert "Abilities: Static, Lightning Rod" in output
    assert "Speed: 90" in output
    