# Деплой проекта в режиме Телеграм Бота на сервере 

1. Склонировать репозиторий на сервер

```sh
git clone git@github.com:ApostolFet/HangManGame.git
cd HangManGame
```

2. Создать виртуальное окружение

```sh
python -m venv .venv
```
3. Активировать виртуальное окружение

```sh
. .venv/bin/activate
```

4. Установить пакет и опциональные зависиости для бота

```sh
pip install ".[bot]"
```

5. Скопировать пример конфига в config.toml
```sh
cp config.example.toml config.toml
```

6. Откройте кофиг и отредактируйте параметры (обязательно установите свой токен для бота)
```sh
nano config.toml
```

7. Выполните миграции базы данных:
```sh
hangman-migrations-up
```

Пример с использованием [пользовательских служб](https://wiki.archlinux.org/title/Systemd_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)/User_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)) (для системных служб команды могут отличаться, также нужно будет добавить `User` в блок [Service])

8. Скопируйте шаблон сервисного файла в директорию, где находятся ваши сервисы.

8.1 Создать папки с пользовательскими службами (если еще не созданы)
  ```sh
  mkdir ~/.config/systemd
  mkdir ~/.config/systemd/user
  ```
8.2 Скопировать шаблон в папку
  ```sh
  cp ./systemd/hangman_bot.service ~/.config/systemd/user/
  ```

9. Изменить в шаблоне путь до рабочей категории и до виртуального окружения
  ```sh
  nano ~/.config/systemd/user/hangman_bot.service
  ```

Пример заполненного шаблона:
```service
[Unit]
Description=HangMan Telegram Bot
After=network.target


[Service]
WorkingDirectory=/home/user_name/projects/HangManGame/
ExecStart=/home/user_name/projects/HangManGame/.venv/bin/hangman-bot
Restart=on-failure


[Install]
WantedBy=default.target
```

10. После сохранения сервисного файла включите службу
```sh
systemctl --user enable hangman_bot.service
```
Если вы изменяете сервисный файл, то для обновлния конфигурации нужно выполнить следующую команду
```sh
systemctl --user daemon-reload
```

11. Запустите службу: 
```sh
systemctl --user start hangman_bot.service 
```

После запуска службы, бот должен начать корректно работать

Полезные команды:

- Просмотр журнала службы:
```sh
journalctl --user -u hangman_bot.service
```


- Просмотр статуса службы:
```sh
systemctl --user status hangman_bot.service
```
