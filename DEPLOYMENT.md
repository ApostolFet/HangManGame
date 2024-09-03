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


8. Скопируйте шаблон сервисного файла в директорию, где находятся ваши сервисы.
  ```sh
  cp ./systemd/hangman_bot.service /etc/systemd/system/
  ```

9. Изменить в шаблоне путь до рабочей категории и до виртуального окружения
  ```sh
  nano /etc/systemd/system/hangman_bot.service
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
WantedBy=multi-user.target
```

10. После сохранения сервисного файла включите службу
```sh
systemctl enable hangman_bot.service
```
Если вы изменяете сервисный файл, то для обновлния конфигурации нужно выполнить следующую команду
```sh
systemctl daemon-reload
```

11. Запустите службу: 
```sh
systemctl start hangman_bot.service 
```

После запуска службы, бот должен начать корректно работать

Полезные команды:

- Просмотр журнала службы:
```sh
journalctl -u hangman_bot.service
```


- Просмотр статуса службы:
```sh
systemctl status hangman_bot.service
```
