[<img src="https://img.shields.io/badge/Telegram-%40DifichentoBot-blue">](https://t.me/DifichentoBot)

# Виртуальное казино в Telegram

В конце октября 2020 года команда Telegram выпустила [очередное обновление](https://telegram.org/blog/pinned-messages-locations-playlists/ru?ln=a) 
мессенджера с поддержкой дайса игрового автомата. Вот он:

![игровой автомат](repo_images/slot_machine.png)

Согласно [документации на тип Dice](https://core.telegram.org/bots/api#dice) в Bot API, слот-машина 
может принимать значения от 1 до 64 включительно. В файле [dice_check.py](bot/dice_check.py) вы найдёте функции 
для сопоставления значения дайса с тройкой выпавших элементов игрового автомата. 
Для демонстрации создан бот [@DifichentoBot](https://t.me/difichentobot) с ведением счёта на виртуальные очки.  
Важным отличием от «традиционного» казино является невозможность влиять 
на выпадающие комбинации, т.к. итоговое значение генерируется на стороне Telegram.

## Технологии

* [aiogram](https://github.com/aiogram/aiogram) — работа с Telegram Bot API;
* [redis](https://redis.io) — персистентное хранение данных (персистентность включается отдельно);
* [cachetools](https://cachetools.readthedocs.io/en/stable) — реализация троттлинга для борьбы с флудом;
* [Docker](https://www.docker.com) и [Docker-Compose](https://docs.docker.com/compose) — быстрое разворачивание бота в изолированном контейнере.
* Systemd

## Установка

Скопируйте файл `env_example` как `.env` (с точкой в начале), откройте и отредактируйте содержимое. Создайте каталоги 
`redis_data` и `redis_config`, в последний подложите свой конфиг `redis.conf` 
(в репозитории есть [пример](redis.example.conf)). Также создайте каталог `locales`, и положите туда подкатологи 
с файлами локализаций для нужных языков (одновременно бот будет использовать только один язык). 
В директории [bot/locales/example](bot/locales/example) есть пример переводов для двух языков и инструкция.

Наконец, запустите бота командой `docker-compose up -d`. 

Альтернативный вариант: используйте Systemd, пример службы тоже есть в [репозитории](casino-bot.example.service).

## Благодарности

* [@Tishka17](https://t.me/Tishka17) за изначальный вектор направления
* [@svinerus](https://t.me/svinerus) за компактную реализацию определения выпавшей комбинации (f6f42a841d3c1778f0e32)
