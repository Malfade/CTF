# 🏴‍☠️ CTF Tools Collection

**Комплексный набор инструментов для CTF соревнований** - атака, защита, форензика и OSINT.

## 🎯 Что такое CTF?

**CTF (Capture The Flag)** - это соревнования по информационной безопасности, где участники решают задачи и получают "флаги" (специальные строки вида `CTF{flag_here}`).

### 📋 Типы CTF задач:
- **🔓 Web Exploitation** - взлом веб-приложений
- **🔐 Cryptography** - взлом шифрования
- **🔍 Forensics** - анализ файлов и данных
- **🌐 Network** - анализ сетевого трафика
- **🔍 OSINT** - поиск информации о людях
- **🛡️ Defense** - защита систем от атак

## 📁 Структура инструментов

### 🔓 Инструменты Атаки
- **network_tools.py** - Сканирование портов, перехват трафика, трассировка
- **web_exploit.py** - SQL инъекции, XSS, directory traversal, комплексное сканирование
- **crypto_tools.py** - Взлом хешей, шифров, кодирование/декодирование
- **advanced_crypto.py** - Продвинутые криптографические методы
- **payload_generator.py** - Генератор полезных нагрузок
- **social_engineering.py** - Фишинговые страницы и клонирование сайтов

### 🛡️ Инструменты Защиты
- **defense_monitor.py** - Мониторинг системы и обнаружение атак
- **log_analyzer.py** - Анализ логов и обнаружение аномалий

### 🔍 Инструменты Форензики
- **forensics.py** - Извлечение данных из файлов, метаданные, анализ хешей
- **steganography.py** - Скрытие и извлечение данных из изображений
- **malware_analysis.py** - Анализ вредоносного ПО

### 🌐 OSINT и Разведка
- **osint_tools.py** - WHOIS, DNS анализ, поиск в социальных сетях
- **osint_investigator.py** - Поиск информации о человеке через Tor
- **tor_integration.py** - Анонимность через Tor

### 🛠️ Утилиты
- **ctf_launcher.py** - Главное меню для запуска всех инструментов
- **wordlist_generator.py** - Генерация словарей для брутфорса
- **utils.py** - Общие функции и утилиты

## 🚀 Быстрый старт

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск главного меню
python3 ctf_launcher.py

# Или запуск отдельных инструментов
python3 network_tools.py --help
python3 web_exploit.py --help
```

## ⚠️ Предупреждение

Эти инструменты предназначены только для легальных CTF соревнований и образовательных целей.
Использование для несанкционированного доступа к системам является незаконным.

## 🎯 Как решать CTF задачи

### 🔓 Web Exploitation (Веб-взлом)
**Цель:** Найти уязвимости в веб-приложениях

```bash
# 1. Сканируем сайт на уязвимости
python3 web_exploit.py --url http://ctf.example.com/login --comprehensive-scan

# 2. Тестируем SQL инъекции
python3 web_exploit.py --url http://ctf.example.com/login?id=1 --test-sqli

# 3. Тестируем XSS
python3 web_exploit.py --url http://ctf.example.com/search?q=test --test-xss

# 4. Брутфорс директорий
python3 web_exploit.py --url http://ctf.example.com --bruteforce
```

**Что искать:**
- SQL Injection: `' OR 1=1--`
- XSS: `<script>alert('XSS')</script>`
- Directory Traversal: `../../../etc/passwd`
- Скрытые файлы: `/admin`, `/backup`, `/.env`

### 🔐 Cryptography (Криптография)
**Цель:** Взломать шифрование или найти скрытые сообщения

```bash
# 1. Пробуем разные методы расшифровки
python3 crypto_tools.py --decrypt "U2FsdGVkX1+vupppZksvRf5pq5g5XjFRlipRkwB0K1Y=" --method base64

# 2. Взламываем хеши
python3 crypto_tools.py --crack-hash "5f4dcc3b5aa765d61d8327deb882cf99" --hash-type md5

# 3. Продвинутые методы
python3 advanced_crypto.py --decrypt "encrypted_text" --method aes --key "secretkey"
```

**Что искать:**
- Base64: символы A-Z, a-z, 0-9, +, /
- ROT13: простой сдвиг букв
- MD5/SHA1: хеши для взлома
- AES/DES: симметричное шифрование

### 🔍 Forensics (Криминалистика)
**Цель:** Найти скрытые данные в файлах

```bash
# 1. Анализируем файл
python3 forensics.py --file suspicious.jpg --analyze

# 2. Ищем строки
python3 forensics.py --file suspicious.jpg --strings

# 3. Анализируем хеши
python3 forensics.py --file suspicious.jpg --hash

# 4. Стеганография
python3 steganography.py --file suspicious.jpg --extract
```

**Что искать:**
- Скрытые файлы в архивах
- Метаданные в изображениях
- Строки в бинарных файлах
- Стеганография в картинках

### 🌐 Network (Сетевые задачи)
**Цель:** Анализировать сетевой трафик или взламывать сетевые сервисы

```bash
# 1. Сканируем порты
python3 network_tools.py --target 192.168.1.100 --scan-ports

# 2. Анализируем трафик
python3 network_tools.py --capture capture.pcap --analyze-traffic

# 3. Трассировка
python3 network_tools.py --target 192.168.1.100 --traceroute
```

### 🔍 OSINT (Разведка)
**Цель:** Найти информацию о человеке или организации

```bash
# 1. Ищем в социальных сетях
python3 osint_investigator.py --username john_doe --html-report

# 2. Анализируем email
python3 osint_investigator.py --email john@example.com

# 3. Ищем утечки данных
python3 osint_investigator.py --email john@example.com --html-report
```

### 🛡️ Defense (Защита)
**Цель:** Защитить систему от атак

```bash
# 1. Мониторим систему
python3 defense_monitor.py --monitor-all

# 2. Анализируем логи
python3 defense_monitor.py --analyze-logs /var/log/auth.log

# 3. Проверяем открытые порты
python3 defense_monitor.py --check-ports
```

## 🎮 Практический пример CTF задачи

### Задача: "Слабый пароль"
```
Найди флаг на сайте: http://ctf.example.com/admin
Подсказка: Админ использует слабый пароль
```

### Пошаговое решение:

#### Шаг 1: Разведка
```bash
# Сканируем сайт
python3 web_exploit.py --url http://ctf.example.com --comprehensive-scan
```

#### Шаг 2: Поиск админки
```bash
# Ищем скрытые директории
python3 web_exploit.py --url http://ctf.example.com --bruteforce
```

#### Шаг 3: Брутфорс пароля
```bash
# Генерируем словарь паролей
python3 wordlist_generator.py --type popular-passwords --output passwords.txt
```

#### Шаг 4: Получаем флаг
После входа в админку находим флаг: `CTF{admin_password_123}`

## 🏆 Форматы флагов

```
CTF{this_is_a_flag}
flag{another_flag}
FLAG{uppercase_flag}
ctf{lowercase_flag}
```

## 💡 Советы для новичков

1. **Начинай с простого:** Web задачи самые понятные
2. **Читай внимательно:** Описание может содержать подсказки
3. **Используй подсказки:** Название задачи часто содержит намек
4. **Практикуйся:** TryHackMe, HackTheBox, OverTheWire

## 🛠️ Технологии

- **Python 3.8+** - основной язык
- **Scapy** - сетевые операции и анализ трафика
- **Beautiful Soup** - парсинг веб-страниц
- **Pillow** - работа с изображениями
- **Cryptography** - криптографические операции
- **Requests** - HTTP запросы
- **Tor/Stem** - анонимность через Tor
- **BeautifulSoup** - парсинг HTML/XML
- **PEFile** - анализ PE файлов
- **YARA** - сканирование вредоносного ПО

## 📊 Статистика проекта

- **12 инструментов** для различных типов CTF задач
- **~12000+ строк кода** с продвинутыми возможностями
- **Полная интеграция** всех инструментов
- **HTML отчеты** для детального анализа
- **Tor анонимность** для безопасного расследования

## 🚀 Запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск главного меню
python3 ctf_launcher.py

# Выберите нужный инструмент из меню

## 📚 Дополнительные ресурсы

### 🎯 CTF платформы для практики:
- **TryHackMe** - обучающие CTF с пошаговыми инструкциями
- **HackTheBox** - практические задачи разной сложности
- **OverTheWire** - классические CTF (Bandit, Natas, etc.)
- **PicoCTF** - соревнования для начинающих
- **CTFtime** - календарь CTF соревнований

### 📖 Полезные ресурсы:
- **OWASP** - веб-уязвимости и защита
- **NIST** - стандарты информационной безопасности
- **MITRE ATT&CK** - тактики и техники атак
- **CVE** - база данных уязвимостей

## ⚖️ Этические принципы

### ✅ Разрешенное использование:
- CTF соревнования и обучение
- Тестирование собственных систем
- Исследования в области безопасности
- Образовательные цели

### ❌ Запрещенное использование:
- Несанкционированный доступ к чужим системам
- Нарушение законов и этических норм
- Коммерческий шпионаж
- Харассмент и сталкинг

---

**🎯 Готов к CTF соревнованиям! Удачи в захвате флагов! 🏴‍☠️**
