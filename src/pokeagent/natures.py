from __future__ import annotations


NATURES: dict[str, tuple[str | None, str | None]] = {
    "hardy": (None, None),
    "lonely": ("attack", "defense"),
    "brave": ("attack", "speed"),
    "adamant": ("attack", "special-attack"),
    "naughty": ("attack", "special-defense"),

    "bold": ("defense", "attack"),
    "docile": (None, None),
    "relaxed": ("defense", "speed"),
    "impish": ("defense", "special-attack"),
    "lax": ("defense", "special-defense"),

    "timid": ("speed", "attack"),
    "hasty": ("speed", "defense"),
    "serious": (None, None),
    "jolly": ("speed", "special-attack"),
    "naive": ("speed", "special-defense"),

    "modest": ("special-attack", "attack"),
    "mild": ("special-attack", "defense"),
    "quiet": ("special-attack", "speed"),
    "bashful": (None, None),
    "rash": ("special-attack", "special-defense"),

    "calm": ("special-defense", "attack"),
    "gentle": ("special-defense", "defense"),
    "sassy": ("special-defense", "speed"),
    "careful": ("special-defense", "special-attack"),
    "quirky": (None, None),
}


def get_nature_modifier(
    nature: str,
    stat_name: str,
) -> float:
    """Return the nature multiplier for a stat."""
    normalized_nature = nature.strip().lower()

    if normalized_nature not in NATURES:
        raise ValueError(
            f"Unknown Pokémon nature: {nature}"
        )

    increased_stat, decreased_stat = NATURES[
        normalized_nature
    ]

    if stat_name == increased_stat:
        return 1.1

    if stat_name == decreased_stat:
        return 0.9

    return 1.0