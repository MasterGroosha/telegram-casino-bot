[<img src="https://img.shields.io/badge/Telegram-%40DifichentoBot-blue">](https://t.me/DifichentoBot)

# Виртуальное казино в Telegram

В конце октября 2020 года команда Telegram выпустила [очередное обновление](https://telegram.org/blog/pinned-messages-locations-playlists/ru?ln=a) 
мессенджера с поддержкой дайса игрового автомата. Вот он:

![игровой автомат](repo_images/slot_machine.png)

Согласно [документации на тип Dice](https://core.telegram.org/bots/api#dice) в Bot API, слот-машина 
может принимать значения от 1 до 64 включительно. В файле `casino.py` вы найдёте функции для сопоставления значения дайса 
с тройкой выпавших элементов игрового автомата. Для демонстрации создан бот [@DifichentoBot](https://t.me/difichentobot) с 
ведением счёта на виртуальные очки, начиная с 50.  
Важным отличием от «традиционного» казино является невозможность влиять 
на выпадающие комбинации, т.к. итоговое значение генерируется на стороне Telegram.

## Технологии

* [aiogram](https://github.com/aiogram/aiogram) — работа с Telegram Bot API;
* [redis](https://redis.io) — персистентное хранение данных;
* [cachetools](https://cachetools.readthedocs.io/en/stable) — реализация троттлинга для борьбы с флудом;
* [Docker](https://www.docker.com) и [Docker-Compose](https://docs.docker.com/compose) — быстрое разворачивание бота \
в изолированном контейнере.

Исходные тексты расположены на [GitLab](https://git.groosha.space/shared/telegram-casino-bot) с автоматическим 
зеркалированием на [GitHub](https://github.com/MasterGroosha/telegram-casino-bot).

## Установка

Скопируйте файл `env_example` как `.env` (с точкой в начале), откройте и отредактируйте содержимое. Создайте каталоги 
`redis-data` и `redis-config`, в последнем можете подсунуть свой конфиг как `redis.conf`.   
Запустите бота командой `docker-compose up -d`. 

Альтернативный вариант с использованием [MemoryStorage](https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/contrib/fsm_storage/memory.py#L7) 
вместо Redis (**внимание:** в этом случае все данные будут сбрасываться при остановке бота, т.к. хранятся в оперативной памяти):  
* замените импорт `RedisStorage2`: `from aiogram.contrib.fsm_storage.memory import MemoryStorage`
* замените инициализацию диспетчера: `dp = Dispatcher(bot, storage=MemoryStorage())`  

Для запуска без Docker воспользуйтесь командой `python -m bot`, установив переменную окружения `BOT_TOKEN` 
токеном вашего бота.

## Благодарности

* [@Tishka17](https://t.me/Tishka17) за изначальный вектор направления
* [@svinerus](https://t.me/svinerus) за компактную реализацию определения выпавшей комбинации (f6f42a841d3c1778f0e32)
