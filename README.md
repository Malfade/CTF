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


