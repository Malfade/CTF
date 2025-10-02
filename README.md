# CTF Tools Collection

Комплексный набор инструментов для CTF соревнований - атака и защита.

## 📁 Структура

### Инструменты Атаки
- **network_tools.py** - Сканирование портов, перехват трафика
- **web_exploit.py** - SQL инъекции, XSS, directory traversal
- **crypto_tools.py** - Взлом хешей, шифров, кодирование/декодирование
- **password_cracker.py** - Брутфорс паролей, генерация словарей
- **payload_generator.py** - Генератор полезных нагрузок

### Инструменты Защиты
- **defense_monitor.py** - Мониторинг системы и обнаружение атак
- **log_analyzer.py** - Анализ логов и обнаружение аномалий
- **firewall_manager.py** - Управление правилами firewall

### Инструменты Форензики
- **forensics.py** - Извлечение данных из файлов, метаданные
- **steganography.py** - Скрытие и извлечение данных из изображений

### Утилиты
- **ctf_launcher.py** - Главное меню для запуска всех инструментов
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

## 📚 Примеры использования

### Сканирование сети
```bash
python3 network_tools.py --scan 192.168.1.0/24
```

### Тестирование веб-уязвимостей
```bash
python3 web_exploit.py --url http://target.com --test-all
```

### Взлом хеша
```bash
python3 crypto_tools.py --crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5
```

### Мониторинг защиты
```bash
python3 defense_monitor.py --monitor-network --alert
```

## 🛠️ Технологии

- Python 3.8+
- Scapy (сетевые операции)
- Beautiful Soup (парсинг веб-страниц)
- Pillow (работа с изображениями)
- Cryptography (криптография)




# CTF

rise and shine 

Web Exploitation

# 1. Сканируем сайт на уязвимости
python3 web_exploit.py --url http://ctf.example.com/login --comprehensive-scan

# 2. Тестируем SQL инъекции
python3 web_exploit.py --url http://ctf.example.com/login?id=1 --test-sqli

# 3. Тестируем XSS
python3 web_exploit.py --url http://ctf.example.com/search?q=test --test-xss

# 4. Брутфорс директорий
python3 web_exploit.py --url http://ctf.example.com --bruteforce

Cryptography 

# 1. Пробуем разные методы расшифровки
python3 crypto_tools.py --decrypt "U2FsdGVkX1+vupppZksvRf5pq5g5XjFRlipRkwB0K1Y=" --method base64

# 2. Взламываем хеши
python3 crypto_tools.py --crack-hash "5f4dcc3b5aa765d61d8327deb882cf99" --hash-type md5

# 3. Продвинутые методы
python3 advanced_crypto.py --decrypt "encrypted_text" --method aes --key "secretkey"

Forensics

# 1. Анализируем файл
python3 forensics.py --file suspicious.jpg --analyze

# 2. Ищем строки
python3 forensics.py --file suspicious.jpg --strings

# 3. Анализируем хеши
python3 forensics.py --file suspicious.jpg --hash

# 4. Стеганография
python3 steganography.py --file suspicious.jpg --extract

Network 

# 1. Сканируем порты
python3 network_tools.py --target 192.168.1.100 --scan-ports

# 2. Анализируем трафик
python3 network_tools.py --capture capture.pcap --analyze-traffic

# 3. Трассировка
python3 network_tools.py --target 192.168.1.100 --traceroute


Defense

# 1. Мониторим систему
python3 defense_monitor.py --monitor-all

# 2. Анализируем логи
python3 defense_monitor.py --analyze-logs /var/log/auth.log

# 3. Проверяем открытые порты
python3 defense_monitor.py --check-ports


CTF{this_is_a_flag}
flag{another_flag}
FLAG{uppercase_flag}
ctf{lowercase_flag}
