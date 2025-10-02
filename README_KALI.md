# 🐉 CTF Tools for Kali Linux

Специальная версия CTF инструментов, адаптированная для Kali Linux с интеграцией популярных инструментов безопасности.

## 🚀 Быстрый старт

### 1. Установка
```bash
cd /home/malfade/Worl/cybersecurity/CTF
chmod +x setup_kali.sh
./setup_kali.sh
```

### 2. Запуск
```bash
# Главное меню Kali
python3 kali_launcher.py

# Или через алиас (если создали)
ctf
```

## 🛠️ Интеграция с Kali Linux

### **Kali Integration Tool** (`kali_integration.py`)

Интеграция с популярными инструментами Kali Linux:

#### **Разведка:**
```bash
# Nmap сканирование
python3 kali_integration.py --nmap 192.168.1.1 --scan-type aggressive

# TheHarvester для сбора информации
python3 kali_integration.py --theharvester example.com

# DNS разведка
python3 kali_integration.py --dnsrecon example.com
python3 kali_integration.py --fierce example.com
```

#### **Веб-тестирование:**
```bash
# Nikto сканирование
python3 kali_integration.py --nikto http://target.com

# SQLMap тестирование
python3 kali_integration.py --sqlmap http://target.com/page.php?id=1

# WPScan для WordPress
python3 kali_integration.py --wpscan http://target.com

# Dirb брутфорс
python3 kali_integration.py --dirb http://target.com
```

#### **Атаки на пароли:**
```bash
# John the Ripper
python3 kali_integration.py --john hashes.txt --wordlist /usr/share/wordlists/rockyou.txt

# Hashcat
python3 kali_integration.py --hashcat hashes.txt --hash-type 0 --wordlist rockyou.txt

# Hydra брутфорс
python3 kali_integration.py --hydra 192.168.1.1 --hydra-service ssh --hydra-user admin --hydra-wordlist passwords.txt

# Crunch генерация словарей
python3 kali_integration.py --crunch 4 6 abc123 passwords.txt
```

#### **Форензика:**
```bash
# Volatility анализ памяти
python3 kali_integration.py --volatility memory.dmp --volatility-plugin pslist

# Binwalk извлечение
python3 kali_integration.py --binwalk suspicious.bin

# Foremost восстановление
python3 kali_integration.py --foremost image.dd recovery/

# ExifTool анализ метаданных
python3 kali_integration.py --exiftool photo.jpg
```

#### **Стеганография:**
```bash
# Steghide извлечение
python3 kali_integration.py --steghide image.jpg

# Zsteg анализ
python3 kali_integration.py --zsteg image.png

# Outguess извлечение
python3 kali_integration.py --outguess image.jpg output.txt
```

## 🎯 Быстрые команды

### **Сканирование сети:**
```bash
# Быстрое сканирование
python3 kali_integration.py --nmap 192.168.1.0/24 --scan-type basic

# Полное сканирование
python3 kali_integration.py --nmap target.com --scan-type aggressive

# Скрытое сканирование
python3 kali_integration.py --nmap target.com --scan-type stealth
```

### **Веб-атаки:**
```bash
# Полное веб-сканирование
python3 kali_integration.py --nikto http://target.com
python3 kali_integration.py --sqlmap http://target.com/page.php?id=1
python3 kali_integration.py --dirb http://target.com
```

### **Взлом паролей:**
```bash
# Взлом хешей
python3 kali_integration.py --john hashes.txt --wordlist /usr/share/wordlists/rockyou.txt
python3 kali_integration.py --hashcat hashes.txt --hash-type 0

# Брутфорс сервисов
python3 kali_integration.py --hydra 192.168.1.1 --hydra-service ssh --hydra-user admin --hydra-wordlist passwords.txt
```

## 🔧 Алиасы (если создали)

```bash
ctf              # Главное меню
ctf-kali         # Список Kali инструментов
ctf-network      # Сетевые инструменты
ctf-web          # Веб-эксплуатация
ctf-crypto       # Криптография
ctf-osint        # OSINT разведка
ctf-tor          # Tor интеграция
```

## 📁 Структура проекта

```
CTF/
├── kali_launcher.py          # Главное меню для Kali
├── kali_integration.py       # Интеграция с Kali инструментами
├── network_tools.py          # Сетевые инструменты (улучшенные)
├── web_exploit.py            # Веб-эксплуатация
├── crypto_tools.py           # Криптография
├── osint_tools.py            # OSINT разведка
├── tor_integration.py        # Tor интеграция
├── payload_generator.py      # Генератор пейлоадов
├── steganography.py          # Стеганография
├── forensics.py              # Форензика
├── defense_monitor.py        # Мониторинг защиты
├── wordlist_generator.py     # Генератор словарей
├── utils.py                  # Общие утилиты
├── setup_kali.sh             # Установочный скрипт для Kali
├── requirements_kali.txt     # Зависимости для Kali
├── ctf_results/              # Результаты сканирования
├── ctf_logs/                 # Логи
├── wordlists/                # Словари
└── payloads/                 # Пейлоады
```

## 🐉 Преимущества для Kali Linux

### **1. Интеграция с Kali инструментами:**
- Nmap, Nikto, SQLMap, John, Hashcat
- TheHarvester, DNSrecon, Fierce
- Volatility, Binwalk, Steghide
- И многие другие!

### **2. Автоматическая установка:**
- Проверка и установка недостающих пакетов
- Настройка виртуального окружения
- Создание алиасов для быстрого доступа

### **3. Специальные возможности:**
- Быстрые команды для типичных CTF задач
- Интеграция с системными инструментами
- Автоматическое определение доступных инструментов

### **4. Оптимизация для Kali:**
- Использование системных пакетов
- Интеграция с /usr/share/wordlists
- Совместимость с Kali инструментами

## 🎯 CTF сценарии для Kali

### **1. Полная разведка цели:**
```bash
# 1. OSINT разведка
python3 osint_tools.py --whois target.com
python3 osint_tools.py --subdomains target.com

# 2. Nmap сканирование
python3 kali_integration.py --nmap target.com --scan-type aggressive

# 3. Веб-сканирование
python3 kali_integration.py --nikto http://target.com
python3 kali_integration.py --sqlmap http://target.com/page.php?id=1
```

### **2. Взлом паролей:**
```bash
# 1. Генерация словаря
python3 wordlist_generator.py --numeric --min 4 --max 6 -o pins.txt

# 2. Взлом хешей
python3 kali_integration.py --john hashes.txt --wordlist pins.txt

# 3. Брутфорс сервисов
python3 kali_integration.py --hydra 192.168.1.1 --hydra-service ssh --hydra-user admin --hydra-wordlist passwords.txt
```

### **3. Форензика:**
```bash
# 1. Анализ файла
python3 forensics.py --file suspicious.bin --analyze

# 2. Извлечение данных
python3 kali_integration.py --binwalk suspicious.bin

# 3. Анализ метаданных
python3 kali_integration.py --exiftool photo.jpg
```

### **4. Стеганография:**
```bash
# 1. Анализ изображения
python3 steganography.py --analyze image.png

# 2. Извлечение данных
python3 kali_integration.py --steghide image.jpg
python3 kali_integration.py --zsteg image.png
```

## 🔧 Настройка

### **Конфигурационный файл** (`.ctf_config`):
```bash
DEFAULT_TIMEOUT=30
DEFAULT_THREADS=50
SAVE_RESULTS=true
LOG_LEVEL=INFO
TOR_PROXY=127.0.0.1:9050
SHODAN_API_KEY=your_key_here
CENSYS_API_ID=your_id_here
CENSYS_API_SECRET=your_secret_here
```

### **Переменные окружения:**
```bash
export SHODAN_API_KEY="your_key_here"
export CENSYS_API_ID="your_id_here"
export CENSYS_API_SECRET="your_secret_here"
```

## 🚨 Важные замечания

1. **Используйте только в легальных целях** - для CTF соревнований и тестирования собственных систем
2. **Получите разрешение** перед тестированием любых систем
3. **Соблюдайте законы** вашей юрисдикции
4. **Используйте ответственно** - не наносите вред

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте что все зависимости установлены: `./setup_kali.sh`
2. Убедитесь что инструменты Kali доступны: `python3 kali_integration.py --list-tools`
3. Проверьте права доступа: `chmod +x *.py *.sh`
4. Перезапустите терминал после создания алиасов

## 🏆 Удачи на CTF!

Теперь у вас есть мощный набор инструментов, специально адаптированный для Kali Linux! 🐉

**Помните:** С большой силой приходит большая ответственность. Используйте эти инструменты этично и законно!

