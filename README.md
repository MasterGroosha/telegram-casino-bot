[<img src="https://img.shields.io/badge/Telegram-%40DifichentoBot-blue">](https://t.me/DifichentoBot) (Ru)

> 🇷🇺 README на русском доступен [здесь](README.ru.md)

# Telegram Virtual Casino

In October 2020 Telegram team released [yet another update](https://telegram.org/blog/pinned-messages-locations-playlists) 
with slot machine dice. Here it is:

![slot machine dice](repo_images/slot_machine.png)

According to [Dice type documentation](https://core.telegram.org/bots/api#dice) in Bot API, slot machine 
emits values 1 to 64. In [dice_check.py](bot/dice_check.py) file you can find all the logic regarding 
matching dice integer value with visual three-icons representation. There is also a test bot [@DifichentoBot](https://t.me/difichentobot) 
in Russian to test how it works.  
Dice are generated on Telegram server-side, you your bot cannot affect the result.

## Technology

* [aiogram](https://github.com/aiogram/aiogram) — asyncio Telegram Bot API framework;
* [redis](https://redis.io) — persistent data storage (persistency enabled separately);
* [cachetools](https://cachetools.readthedocs.io/en/stable) — for anti-flood throttling mechanism;
* [Docker](https://www.docker.com) and [Docker-Compose](https://docs.docker.com/compose) — quickly deploy bot in containers.
* Systemd

## Installation

Copy `settings.example.toml` file to `settings.toml`, open and edit it.  
To change bot's language, overwrite `bot/locale/current` directory contents with a chosen language. For example, you want 
to use English language in your bot. Then, in `bot/locale/current` create a directory named `en` and place your `.ftl` 
files inside. Check [this directory](bot/locales/example) for samples. 
Please note that only one language can be active at a time.

Finally, run the bot with `docker-compose --profile "all" up -d` command.

Alternative way: you can use Systemd services, there is also an [example](casino-bot.example.service) available.

## Credits to

* [@Tishka17](https://t.me/Tishka17) for initial inspiration
* [@svinerus](https://t.me/svinerus) for compact dice combination check (f6f42a841d3c1778f0e32)


## Note on versioning

For most of my Telegram bots, I plan to use Calendar Versioning with the following rules:

* Versions should look like `vAAAA.BB.C`, where:
* * `vAAAA` is the letter "v" followed by the 4-digit year of release, e.g., `v2025`.
* * `BB` is the 2-digit month number, e.g., `06` for June.
* * `C` is the release number for that month, not zero-padded, e.g., 1 for the first release in June.
For example, the first release to use the new versioning schema will be tagged as `v2025.06.1`.

This scheme makes it easier to understand which Bot API features might be supported in a given release and which are definitely not.