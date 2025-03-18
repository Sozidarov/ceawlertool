# Ceawler

Ceawler — это инструмент для поиска информации по имени пользователя, email, телефону и запросам в браузере. Использует API DaData для проверки номеров телефона и другие открытые источники для сбора данных.

## Возможности
- Поиск по имени пользователя (`--username`) на различных платформах (GitHub, Instagram, Twitter и др.).
- Проверка email (`--email`) через сервисы вроде HaveIBeenPwned.
- Поиск через браузер (`--cbrowser`) с использованием Google Custom Search API.
- Проверка номера телефона (`--phone`) через DaData API.

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/g2jt3/ceawlertool.git
   cd ceawler
   pip install -r requirements.txt
   python main.py