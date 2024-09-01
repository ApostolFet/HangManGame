# Разработка проекта

## Подготовка рабочего окружения

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

  4. Установить пакет и опциональные зависиости для разработки и тестирования

  ```sh
  pip install -e ".[bot,test,dev]"
  ```


## Запуск тестов
```sh
pytest
```

## Запукс линтеров

### MYPY
```sh
mypy .
```

### RUFF
```sh
ruff check . 
```

## Запуск форматера

```sh
ruff format .
```
