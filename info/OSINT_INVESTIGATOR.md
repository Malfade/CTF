# 🔍 OSINT Investigator - Поиск информации о человеке через Tor

## 📋 **Описание**

**OSINT Investigator** - это мощный инструмент для поиска информации о человеке через Tor браузер. Предназначен для CTF соревнований по расследованию и OSINT (Open Source Intelligence).

## ⚠️ **ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ**

```
⚠️  ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!
⚠️  НЕ ИСПОЛЬЗУЙТЕ ДЛЯ НЕЗАКОННЫХ ЦЕЛЕЙ!
⚠️  СОБЛЮДАЙТЕ ЗАКОНЫ И ЭТИЧЕСКИЕ СТАНДАРТЫ!
```

---

## 🚀 **Возможности**

### **🔍 Поиск в социальных сетях:**
- Facebook, Twitter, Instagram, LinkedIn
- GitHub, Reddit, YouTube, TikTok
- Snapchat, Discord, Steam, Twitch
- Pinterest, Tumblr, Flickr

### **📧 Анализ email:**
- Поиск утечек данных
- Проверка в базах Have I Been Pwned
- Анализ связанных аккаунтов

### **📞 Информация о телефоне:**
- Определение оператора связи
- Геолокация номера
- Тип номера (мобильный/стационарный)

### **👤 Поиск по username:**
- Поиск на всех популярных платформах
- Статус аккаунта (активный/неактивный)
- Количество подписчиков
- Дата последней активности

### **🌐 Анализ доменов:**
- WHOIS информация
- DNS записи
- История регистрации

### **📋 Публичные записи:**
- Судебные записи
- Бизнес-регистрации
- Профессиональные лицензии
- Регистрация избирателей

---

## 🛠️ **Установка зависимостей**

```bash
# Установка Python зависимостей
pip install -r requirements.txt

# Установка Tor (Ubuntu/Debian)
sudo apt update
sudo apt install tor

# Запуск Tor
sudo systemctl start tor
sudo systemctl enable tor

# Проверка работы Tor
curl --socks5 127.0.0.1:9050 https://check.torproject.org/
```

---

## 📖 **Использование**

### **Базовые команды:**

```bash
# Поиск по username
python3 osint_investigator.py --username john_doe

# Поиск по email
python3 osint_investigator.py --email john@example.com

# Поиск по номеру телефона
python3 osint_investigator.py --phone +1234567890

# Поиск по имени
python3 osint_investigator.py --name "John Doe"

# Анализ домена
python3 osint_investigator.py --domain example.com
```

### **Комплексное расследование:**

```bash
# Полное расследование с несколькими параметрами
python3 osint_investigator.py \
    --username john_doe \
    --email john@example.com \
    --phone +1234567890 \
    --name "John Doe" \
    --domain example.com \
    --location "New York"
```

### **Создание HTML отчета:**

```bash
# Создание детального HTML отчета
python3 osint_investigator.py \
    --username target_user \
    --email target@example.com \
    --html-report \
    --output investigation_report.html
```

### **Сохранение результатов:**

```bash
# Сохранение результатов в JSON
python3 osint_investigator.py \
    --username john_doe \
    --save
```

---

## 📊 **Примеры результатов**

### **Поиск в социальных сетях:**
```
[+] Найден профиль на GitHub: https://github.com/john_doe
[+] Найден профиль на Twitter: https://twitter.com/john_doe
[+] Найден профиль на LinkedIn: https://linkedin.com/in/john_doe
```

### **Утечки данных:**
```
[!] Найдена утечка: Have I Been Pwned (2023-12-15)
[!] Найдена утечка: DeHashed (2023-11-20)
```

### **Информация о телефоне:**
```
[+] Найдена информация в TrueCaller: Verizon
[+] Найдена информация в SpyDialer: New York
```

### **Публичные записи:**
```
[+] Найдена запись: Property Records
[+] Найдена запись: Court Records
[+] Найдена запись: Business Records
```

---

## 📄 **HTML отчеты**

Инструмент создает детальные HTML отчеты с:

- **🎯 Информация о цели** - все введенные данные
- **📱 Социальные сети** - найденные профили с ссылками
- **📧 Email информация** - результаты анализа
- **📞 Телефон** - оператор, локация, тип
- **👤 Username совпадения** - все найденные аккаунты
- **🌐 Домен** - WHOIS, DNS записи
- **🔓 Утечки данных** - найденные бреши
- **📋 Публичные записи** - судебные и бизнес записи

### **Пример HTML отчета:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>OSINT Investigation Report</title>
    <style>
        /* Профессиональный дизайн */
        body { font-family: Arial, sans-serif; }
        .header { background: #2c3e50; color: white; }
        .section { margin-bottom: 30px; }
        .found { color: #27ae60; }
        .warning { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 OSINT Investigation Report</h1>
        </div>
        <!-- Детальная информация -->
    </div>
</body>
</html>
```

---

## 🔧 **Технические детали**

### **Tor интеграция:**
- Автоматическое обновление идентичности
- SOCKS5 проксирование через Tor
- Случайные User-Agent для анонимности
- Задержки между запросами

### **Источники данных:**
- **Социальные сети:** Прямые API и веб-скрапинг
- **Утечки:** Симуляция поиска в базах данных
- **Телефон:** Интеграция с сервисами поиска
- **Домены:** WHOIS и DNS запросы
- **Публичные записи:** Государственные базы данных

### **Безопасность:**
- Все запросы через Tor
- Ротация User-Agent
- Случайные задержки
- Логирование для CTF

---

## 🎯 **CTF сценарии**

### **Сценарий 1: Поиск информации о цели**
```bash
# Получаем username от жертвы
python3 osint_investigator.py --username victim_user --html-report

# Анализируем HTML отчет
# Находим связанные аккаунты
# Определяем паттерны поведения
```

### **Сценарий 2: Расследование утечки данных**
```bash
# Анализируем email жертвы
python3 osint_investigator.py \
    --email victim@company.com \
    --name "Victim Name" \
    --html-report

# Проверяем утечки данных
# Анализируем связанные аккаунты
```

### **Сценарий 3: Геолокация по телефону**
```bash
# Анализируем номер телефона
python3 osint_investigator.py \
    --phone +1234567890 \
    --name "Target Name" \
    --html-report

# Определяем оператора
# Получаем примерную локацию
```

---

## 📈 **Статистика и метрики**

### **Пример вывода:**
```
🎯 OSINT РАССЛЕДОВАНИЕ ЗАВЕРШЕНО
Всего найдено: 15 записей
Социальные сети: 6
Утечки данных: 2
Информация о телефоне: 3
Совпадения username: 4
Информация о домене: 2
Публичные записи: 3
```

---

## ⚙️ **Конфигурация**

### **Tor настройки:**
```bash
# /etc/tor/torrc
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
```

### **Прокси настройки:**
```python
tor_proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}
```

---

## 🚨 **Этические принципы**

### **✅ Разрешенное использование:**
- CTF соревнования
- Образовательные цели
- Собственные исследования
- Легальные расследования

### **❌ Запрещенное использование:**
- Харассмент и сталкинг
- Незаконный сбор данных
- Нарушение приватности
- Коммерческий шпионаж

---

## 🔍 **Примеры команд**

### **Быстрый поиск:**
```bash
python3 osint_investigator.py --username john_doe
```

### **Детальное расследование:**
```bash
python3 osint_investigator.py \
    --username john_doe \
    --email john@example.com \
    --phone +1234567890 \
    --name "John Doe" \
    --domain example.com \
    --location "New York" \
    --html-report \
    --save
```

### **Только утечки данных:**
```bash
python3 osint_investigator.py --email target@example.com
```

### **Только социальные сети:**
```bash
python3 osint_investigator.py --username target_user
```

---

## 🏆 **Результат**

**OSINT Investigator** предоставляет:

- **🔍 Комплексный поиск** информации о человеке
- **🌐 Tor анонимность** для безопасного расследования
- **📊 Детальные отчеты** в HTML формате
- **🎯 CTF готовность** для соревнований
- **⚖️ Этическое использование** только для образования

**Идеальный инструмент для CTF соревнований по расследованию! 🎯**

