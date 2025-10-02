# 🎯 CTF Tools - Обзор инструментов

## ✅ Созданные инструменты

### 🔴 АТАКА (6 инструментов)

#### 1. **network_tools.py** - Сетевые инструменты
- Сканирование портов (отдельные, диапазоны, популярные)
- Ping sweep (поиск живых хостов)
- Захват баннеров сервисов
- Многопоточное сканирование

#### 2. **web_exploit.py** - Веб-эксплуатация
- SQL Injection тестирование
- XSS (Cross-Site Scripting) тестирование
- Directory/File брутфорс
- Анализ заголовков безопасности
- Поддержка параметров из URL

#### 3. **crypto_tools.py** - Криптография
- Взлом хешей (MD5, SHA1, SHA256, SHA512)
- Шифр Цезаря (шифрование/дешифрование/брутфорс)
- ROT13
- Шифр Виженера
- XOR шифрование
- Кодирование/декодирование (Base64, Base32, HEX, URL)
- Автоопределение типа кодирования

#### 4. **payload_generator.py** - Генератор пейлоадов
- XSS пейлоады (HTML, JavaScript, Attribute, URL)
- SQL Injection (MySQL, MSSQL, PostgreSQL)
- Command Injection (Linux, Windows)
- LFI (Local File Inclusion)
- XXE (XML External Entity)
- Reverse Shell (Bash, Python, PHP, Perl, Ruby, NC)
- Кодирование пейлоадов

#### 5. **wordlist_generator.py** - Генератор словарей
- Числовые комбинации
- Буквенные комбинации
- Алфавитно-числовые
- Пользовательские наборы символов
- Генерация по паттерну
- Популярные пароли с вариациями
- Правила трансформации (leet speak)

#### 6. **steganography.py** - Стеганография
- Скрытие текста в изображениях (LSB метод)
- Извлечение текста из изображений
- Скрытие файлов в изображениях
- Извлечение файлов из изображений
- Анализ изображений на стеганографию
- LSB статистический анализ

### 🔵 ЗАЩИТА (1 инструмент)

#### 7. **defense_monitor.py** - Мониторинг и защита
- Мониторинг сетевых соединений
- Обнаружение подозрительных процессов
- Мониторинг открытых портов (baseline + обнаружение изменений)
- Мониторинг изменений файлов
- Информация о системе
- Анализ логов на brute-force атаки

### 🟢 ФОРЕНЗИКА (1 инструмент)

#### 8. **forensics.py** - Цифровая форензика
- Вычисление хешей файлов
- Полная информация о файле
- Поиск строк в бинарных файлах
- Hex dump
- Поиск магических байтов (сигнатур файлов)
- Анализ энтропии (обнаружение шифрования)
- Извлечение данных из дампов памяти

### 🟡 УТИЛИТЫ

#### 9. **utils.py** - Общие функции
- Цветной вывод (успех, ошибка, предупреждение, инфо)
- Баннеры инструментов
- Сохранение результатов (TXT, JSON)
- Вычисление хешей
- Base64/HEX кодирование/декодирование
- Логирование
- Валидация IP/URL
- Progress bar
- Rate limiter

#### 10. **ctf_launcher.py** - Главное меню
- Интерактивное меню всех инструментов
- Описания и примеры использования
- Быстрый запуск инструментов
- Справка по каждому инструменту

---

## 📦 Файлы конфигурации

- **requirements.txt** - Все зависимости Python
- **setup.sh** - Скрипт автоматической установки
- **README.md** - Основная документация
- **QUICKSTART.md** - Быстрое руководство с примерами
- **OVERVIEW.md** - Этот файл (обзор)

---

## 🚀 Быстрый старт

### 1. Установка
```bash
cd /home/malfade/Worl/cybersecurity/CTF
./setup.sh
```

### 2. Запуск главного меню
```bash
python3 ctf_launcher.py
```

### 3. Или использование отдельных инструментов
```bash
# Сканирование сети
python3 network_tools.py --scan-common 192.168.1.1

# Тест веб-уязвимостей
python3 web_exploit.py --url http://target.com --test-all

# Взлом хеша
python3 crypto_tools.py --crack-hash <HASH> --type md5

# Генерация пейлоадов
python3 payload_generator.py --xss --context html

# Мониторинг системы
python3 defense_monitor.py --check-processes

# Анализ файла
python3 forensics.py --file suspicious.bin --analyze

# Стеганография
python3 steganography.py --extract-text image.png

# Генерация словаря
python3 wordlist_generator.py --numeric --min 4 --max 6 -o pins.txt
```

---

## 📊 Статистика

- **Всего инструментов**: 10
- **Строк кода**: ~3500+
- **Функций и классов**: 80+
- **Поддерживаемых атак**: 15+
- **Типов пейлоадов**: 50+

---

## 🎓 CTF сценарии использования

### Атака (Red Team)
1. **Разведка**: network_tools → сканирование портов и сервисов
2. **Анализ**: web_exploit → поиск уязвимостей
3. **Эксплуатация**: payload_generator → создание эксплойтов
4. **Пост-эксплуатация**: forensics → анализ добытых данных

### Защита (Blue Team)
1. **Мониторинг**: defense_monitor → отслеживание системы
2. **Обнаружение**: defense_monitor → поиск аномалий
3. **Анализ**: forensics → исследование инцидентов
4. **Форензика**: steganography → поиск скрытых данных

---

## 🔥 Основные возможности

✅ **Многопоточность** - быстрое сканирование и брутфорс
✅ **Stealth режим** - избегание обнаружения
✅ **Логирование** - сохранение всех результатов
✅ **Цветной вывод** - удобный интерфейс
✅ **Модульность** - независимые инструменты
✅ **Расширяемость** - легко добавлять новые функции
✅ **Документация** - подробные примеры и справка

---

## ⚠️ ВАЖНО

Все инструменты созданы **исключительно** для:
- ✅ Легальных CTF соревнований
- ✅ Собственных систем с разрешением
- ✅ Образовательных целей
- ✅ Тестирования безопасности с авторизацией

❌ **НЕЗАКОННО** использовать для:
- Несанкционированного доступа к чужим системам
- Атак на реальные сервисы без разрешения
- Любой незаконной деятельности

---

## 📚 Дополнительные ресурсы

**CTF Платформы:**
- HackTheBox (hackthebox.eu)
- TryHackMe (tryhackme.com)
- PicoCTF (picoctf.org)
- CTFtime (ctftime.org)

**Обучение:**
- OWASP Top 10
- PortSwigger Web Security Academy
- Cybrary
- Offensive Security

**Инструменты:**
- Burp Suite
- Metasploit
- Wireshark
- John the Ripper

---

## 🛠️ Техническое

**Технологии:**
- Python 3.8+
- Requests (HTTP клиент)
- BeautifulSoup (парсинг HTML)
- Scapy (сетевые пакеты)
- Pillow (работа с изображениями)
- Cryptography (криптография)
- PSUtil (системный мониторинг)

**Архитектура:**
```
CTF/
├── Атака/
│   ├── network_tools.py
│   ├── web_exploit.py
│   ├── crypto_tools.py
│   ├── payload_generator.py
│   ├── wordlist_generator.py
│   └── steganography.py
├── Защита/
│   └── defense_monitor.py
├── Форензика/
│   └── forensics.py
├── Утилиты/
│   ├── utils.py
│   └── ctf_launcher.py
└── Документация/
    ├── README.md
    ├── QUICKSTART.md
    └── OVERVIEW.md
```

---

## ✨ Готово к использованию!

Все инструменты созданы и готовы к работе. Начните с:

```bash
python3 ctf_launcher.py
```
 1. Установка
cd /home/malfade/Worl/cybersecurity/CTF
./setup.sh

# 2. Запуск главного меню
python3 ctf_launcher.py

# 3. Или отдельные инструменты:
python3 network_tools.py --help
python3 web_exploit.py --help
python3 crypto_tools.py --help

 Сканирование сети
python3 network_tools.py --scan-common 192.168.1.1

# Взлом MD5
python3 crypto_tools.py --crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5

# Генерация reverse shell
python3 payload_generator.py --reverse-shell 10.10.10.1 4444 --shell-type bash

# Мониторинг защиты
python3 defense_monitor.py --monitor-network --duration 120

**Удачи на CTF соревнованиях! 🏆**







