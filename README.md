# Discord Bot

A simple Discord bot built with Python using `discord.py`.

## Features

- `/hello` slash command
- custom help command
- prefix-based help support
- bot prefix configuration in `config.py`

## Setup

1. Install dependencies:

```bash
pip install -r requirement.txt
```

2. Update your token in `config.py`:

```python
token = "BOT_TOKEN"
prefix = "!p"
```

3. Run the bot:

```bash
python main.py
```

## Project Structure

```text
.
├── main.py
├── config.py
├── requirement.txt
├── comds/
│   └── help.py
├── README.md
```

## Commands

- `/hello`
- `!p help`

## Notes

This project is a small starter bot and can be expanded with more commands and cogs.

this code have so many bug i will fix as soon as possible 
