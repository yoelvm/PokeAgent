# PokeAgent

PokeAgent is a modular Pokémon Pokédex project built with Python.

The project currently focuses on the original 151 Kanto Pokémon and provides a command-line interface for searching and filtering Pokémon using locally stored data.

This project is designed as a foundation for future features such as a visual web interface, additional Pokémon generations, team building, legality tools, and AI-powered agent capabilities.

## Features

- Search Pokémon by name
- Search Pokémon by National Pokédex number
- List Pokémon by type
- Filter Pokémon by type and minimum base stat
- Display height and weight in readable units
- Display abilities and base stats
- Local Kanto Pokédex with 151 Pokémon
- Data obtained from PokéAPI
- Automated tests with pytest
- Modular architecture prepared for future expansion

## Requirements

- Python 3.11 or newer

## Installation

Clone the repository and enter the project directory.

Install PokeAgent and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Running PokeAgent

Start the interactive Pokédex with:

```bash
pokeagent
```

You should see:

```text
PokeAgent - Kanto Pokedex
Search by Pokemon name or Pokedex number.
Type 'q' to quit.

Search Pokemon:
```

## Commands

### Search by name

```text
pikachu
```

### Search by Pokédex number

```text
25
```

### Search by type

```text
type electric
```

### Filter by type and minimum base stat

Syntax:

```text
stat <type> <stat> <minimum>
```

Example:

```text
stat electric speed 120
```

This returns Electric-type Pokémon with a base Speed of at least 120.

### Show help

```text
help
```

You can also use:

```text
h
?
```

### Quit

```text
q
```

The following commands also exit PokeAgent:

```text
quit
exit
```

## Example

```text
Search Pokemon: pikachu

#025 Pikachu
Type: Electric
Height: 0.4 m
Weight: 6.0 kg
Abilities: Static, Lightning Rod
Base stats:
  Hp: 35
  Attack: 55
  Defense: 40
  Special Attack: 50
  Special Defense: 50
  Speed: 90
```

## Project Structure

```text
PokeAgent/
├── data/
│   └── kanto.json
├── src/
│   └── pokeagent/
│       ├── __init__.py
│       ├── api.py
│       ├── cli.py
│       ├── kanto.py
│       ├── models.py
│       ├── repository.py
│       └── service.py
├── tests/
│   ├── test_cli.py
│   ├── test_models.py
│   ├── test_repository.py
│   └── test_service.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Architecture

PokeAgent separates responsibilities into several layers:

- `api.py` communicates with PokéAPI.
- `kanto.py` builds the local Kanto dataset.
- `models.py` defines the Pokémon data model.
- `repository.py` loads and queries the local Pokédex.
- `service.py` provides higher-level search operations.
- `cli.py` provides the interactive command-line interface.

This separation allows future interfaces and agents to reuse the same core logic.

## Running Tests

Run the complete automated test suite with:

```bash
python -m pytest -q
```

The current test suite verifies repository loading, Pokémon models, search services, validation, and CLI formatting.

## Data

The local Kanto Pokédex contains Pokémon with National Pokédex IDs:

```text
#001 Bulbasaur
...
#151 Mew
```

Pokémon data is sourced from PokéAPI and simplified before being stored locally.

> Note: PokeAgent currently uses modern PokéAPI metadata for the 151 Kanto species. This means some information, such as abilities or modern typings, may differ from the original Generation I game mechanics.

## Roadmap

Planned future improvements include:

- Visual web interface
- Pokémon images and sprites
- Additional search and filtering options
- Johto and later generations
- Moves
- Items
- Evolutions
- Type effectiveness
- Game-specific Pokémon data
- Team builder
- Pokémon legality tools
- AI-powered natural-language interaction

## License

This project is licensed under the MIT License.

## Disclaimer

Pokémon and Pokémon character names are trademarks of Nintendo, Game Freak, and The Pokémon Company.

PokeAgent is an independent educational project and is not affiliated with or endorsed by Nintendo, Game Freak, or The Pokémon Company.
