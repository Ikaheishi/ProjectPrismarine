PrismarineCo. Ltd. Presents...
# Project Prismarine!
*`ProjectPrismarine`*

An experimental moderation and Splatoon 2 discord bot!

[![Discord Bots](https://discordbots.org/api/widget/568469437284614174.svg)](https://discordbots.org/bot/568469437284614174)

## Dependencies:
- `discord.py` (1.1.0 or later)
- `SQLAlchemy` (1.3.4 or later)
- `dbl` (0.3.0)

## Running:
1. Create a `config.json` file in the project root directory.
2. Add the key `token` with your bot token string.
3. Add the key `owner` with your user ID integer.
4. Add the key `dbl_token` with the API token for a Discord Bot List bot. If you do not have one, just leave this as an empty string.
5. Add the key `prefix` with the prefix of your choice.
6. Initialize the bot by running `core.py`.
7. Profit!

#### Footnote:
- Make sure any file you run is ran from the project root directory *(ex. `python bin/create_asset_db.py`)*
