#!/usr/bin/env python3
"""
Enhanced Kali Linux CTF Launcher - Улучшенный launcher для Kali Linux
Версия 3.0 с полной интеграцией CTF инструментов
"""

import sys
import subprocess
import os
import json
import time
import shutil
import readline
from datetime import datetime
from pathlib import Path
from utils import *

class EnhancedKaliCTFLauncher:
    """Улучшенный launcher для Kali Linux с полной интеграцией CTF инструментов"""
    
    def __init__(self):
        self.version = "3.0"
        self.config_file = "launcher_config.json"
        self.history_file = "command_history.json"
        self.profiles_file = "user_profiles.json"
        self.current_profile = "default"
        self.command_history = []
        self.user_profiles = {}
        self.ctf_tools_dir = Path(__file__).parent
        
        # Загружаем конфигурацию
        self.load_config()
        self.load_history()
        self.load_profiles()
        
        # Полный список CTF инструментов
        self.ctf_tools = {
            # 🔓 Инструменты Атаки
            '1': {
                'name': 'Network Tools (Enhanced)',
                'desc': 'Сканирование портов, перехват трафика, трассировка',
                'script': 'network_tools.py',
                'category': 'Network',
                'examples': [
                    '--target 192.168.1.1 --scan-ports',
                    '--capture capture.pcap --analyze-traffic',
                    '--target 192.168.1.1 --traceroute'
                ]
            },
            '2': {
                'name': 'Web Exploitation',
                'desc': 'SQL injection, XSS, Directory brute-force',
                'script': 'web_exploit.py',
                'category': 'Web',
                'examples': [
                    '--url http://target.com --comprehensive-scan',
                    '--url http://target.com/page.php?id=1 --test-sqli',
                    '--url http://target.com/search?q=test --test-xss'
                ]
            },
            '3': {
                'name': 'Crypto Tools',
                'desc': 'Взлом хешей, шифрование/дешифрование',
                'script': 'crypto_tools.py',
                'category': 'Crypto',
                'examples': [
                    '--crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5',
                    '--decrypt "U2FsdGVkX1+vupppZksvRf5pq5g5XjFRlipRkwB0K1Y=" --method base64',
                    '--caesar-bruteforce "KHOOR"'
                ]
            },
            '4': {
                'name': 'Advanced Crypto',
                'desc': 'Продвинутые криптографические методы',
                'script': 'advanced_crypto.py',
                'category': 'Crypto',
                'examples': [
                    '--decrypt "encrypted_text" --method aes --key "secretkey"',
                    '--rsa-crack public.pem --private-key private.pem',
                    '--frequency-analysis ciphertext.txt'
                ]
            },
            '5': {
                'name': 'Payload Generator',
                'desc': 'Генерация пейлоадов для эксплуатации',
                'script': 'payload_generator.py',
                'category': 'Exploitation',
                'examples': [
                    '--xss --context html',
                    '--reverse-shell 10.10.10.1 4444 --shell-type bash',
                    '--sql-injection --type union'
                ]
            },
            '6': {
                'name': 'Social Engineering',
                'desc': 'Фишинговые страницы и клонирование сайтов',
                'script': 'social_engineering.py',
                'category': 'Social',
                'examples': [
                    '--clone-site http://target.com --output cloned_site',
                    '--phishing-email --template corporate --target user@company.com'
                ]
            },
            
            # 🛡️ Инструменты Защиты
            '7': {
                'name': 'Defense Monitor',
                'desc': 'Мониторинг системы и обнаружение атак',
                'script': 'defense_monitor.py',
                'category': 'Defense',
                'examples': [
                    '--monitor-all',
                    '--analyze-logs /var/log/auth.log',
                    '--check-ports'
                ]
            },
            
            # 🔍 Инструменты Форензики
            '8': {
                'name': 'Forensics',
                'desc': 'Извлечение данных из файлов, метаданные, анализ хешей',
                'script': 'forensics.py',
                'category': 'Forensics',
                'examples': [
                    '--file suspicious.jpg --analyze',
                    '--file suspicious.jpg --strings',
                    '--file suspicious.jpg --hash'
                ]
            },
            '9': {
                'name': 'Steganography',
                'desc': 'Скрытие и извлечение данных из изображений',
                'script': 'steganography.py',
                'category': 'Forensics',
                'examples': [
                    '--file suspicious.jpg --extract',
                    '--file image.png --analyze',
                    '--hide-text "secret message" --image photo.jpg --output hidden.png'
                ]
            },
            '10': {
                'name': 'Malware Analysis',
                'desc': 'Анализ вредоносного ПО',
                'script': 'malware_analysis.py',
                'category': 'Forensics',
                'examples': [
                    '--file suspicious.exe --analyze',
                    '--file malware.bin --strings --min-length 6',
                    '--file virus.exe --yara-scan'
                ]
            },
            
            # 🌐 OSINT и Разведка
            '11': {
                'name': 'OSINT Tools',
                'desc': 'WHOIS, DNS анализ, поиск в социальных сетях',
                'script': 'osint_tools.py',
                'category': 'OSINT',
                'examples': [
                    '--whois example.com',
                    '--subdomains example.com',
                    '--username john_doe'
                ]
            },
            '12': {
                'name': 'OSINT Investigator',
                'desc': 'Поиск информации о человеке через Tor',
                'script': 'osint_investigator.py',
                'category': 'OSINT',
                'examples': [
                    '--username john_doe --html-report',
                    '--email john@example.com',
                    '--phone +1234567890 --deep-search'
                ]
            },
            '13': {
                'name': 'Tor Integration',
                'desc': 'Анонимность через Tor',
                'script': 'tor_integration.py',
                'category': 'Privacy',
                'examples': [
                    '--check-tor',
                    '--scan-url https://target.com',
                    '--scan-onion facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion'
                ]
            },
            
            # 🛠️ Утилиты
            '14': {
                'name': 'Wordlist Generator',
                'desc': 'Генерация словарей для брутфорса',
                'script': 'wordlist_generator.py',
                'category': 'Utilities',
                'examples': [
                    '--numeric --min 4 --max 6 -o pins.txt',
                    '--common --apply-rules -o passwords.txt',
                    '--custom --input names.txt --output custom_wordlist.txt'
                ]
            },
            '15': {
                'name': 'Kali Integration',
                'desc': 'Интеграция с инструментами Kali Linux',
                'script': 'kali_integration.py',
                'category': 'Integration',
                'examples': [
                    '--list-tools',
                    '--nmap 192.168.1.1 --scan-type aggressive',
                    '--nikto http://target.com',
                    '--john hashes.txt --wordlist /usr/share/wordlists/rockyou.txt'
                ]
            }
        }
        
        self.kali_quick_commands = {
            '1': {
                'name': 'Быстрое сканирование сети',
                'command': 'python3 kali_integration.py --nmap 192.168.1.0/24 --scan-type basic',
                'desc': 'Быстрое сканирование локальной сети'
            },
            '2': {
                'name': 'Полное сканирование цели',
                'command': 'python3 kali_integration.py --nmap TARGET --scan-type aggressive',
                'desc': 'Агрессивное сканирование с OS detection'
            },
            '3': {
                'name': 'Веб-сканирование',
                'command': 'python3 kali_integration.py --nikto http://TARGET',
                'desc': 'Сканирование веб-сервера на уязвимости'
            },
            '4': {
                'name': 'SQL Injection тест',
                'command': 'python3 kali_integration.py --sqlmap http://TARGET/page.php?id=1',
                'desc': 'Тестирование на SQL injection'
            },
            '5': {
                'name': 'Взлом хешей',
                'command': 'python3 kali_integration.py --john hashes.txt --wordlist /usr/share/wordlists/rockyou.txt',
                'desc': 'Взлом хешей с помощью John the Ripper'
            },
            '6': {
                'name': 'Анализ стеганографии',
                'command': 'python3 kali_integration.py --steghide image.jpg',
                'desc': 'Извлечение скрытых данных из изображения'
            },
            '7': {
                'name': 'Форензика файла',
                'command': 'python3 kali_integration.py --binwalk suspicious.bin',
                'desc': 'Анализ и извлечение данных из файла'
            },
            '8': {
                'name': 'Генерация словаря',
                'command': 'python3 wordlist_generator.py --numeric --min 4 --max 6 -o pins.txt',
                'desc': 'Генерация числового словаря'
            }
        }
    
    def load_config(self):
        """Загрузка конфигурации"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_profile = config.get('current_profile', 'default')
        except Exception as e:
            print_warning(f"Ошибка загрузки конфигурации: {e}")
    
    def save_config(self):
        """Сохранение конфигурации"""
        try:
            config = {
                'current_profile': self.current_profile,
                'version': self.version,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print_warning(f"Ошибка сохранения конфигурации: {e}")
    
    def load_history(self):
        """Загрузка истории команд"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.command_history = json.load(f)
        except Exception as e:
            print_warning(f"Ошибка загрузки истории: {e}")
            self.command_history = []
    
    def save_history(self):
        """Сохранение истории команд"""
        try:
            # Ограничиваем историю 100 командами
            if len(self.command_history) > 100:
                self.command_history = self.command_history[-100:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.command_history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print_warning(f"Ошибка сохранения истории: {e}")
    
    def add_to_history(self, command: str):
        """Добавление команды в историю"""
        timestamp = datetime.now().isoformat()
        self.command_history.append({
            'command': command,
            'timestamp': timestamp,
            'profile': self.current_profile
        })
        self.save_history()
    
    def load_profiles(self):
        """Загрузка профилей пользователей"""
        try:
            if os.path.exists(self.profiles_file):
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    self.user_profiles = json.load(f)
        except Exception as e:
            print_warning(f"Ошибка загрузки профилей: {e}")
            self.user_profiles = {'default': {'name': 'Default Profile', 'favorites': []}}
    
    def save_profiles(self):
        """Сохранение профилей пользователей"""
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_profiles, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print_warning(f"Ошибка сохранения профилей: {e}")
    
    def check_tool_exists(self, script_name: str) -> bool:
        """Проверка существования инструмента"""
        script_path = self.ctf_tools_dir / script_name
        return script_path.exists()
    
    def show_banner(self):
        """Показать баннер Kali Linux"""
        banner = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║            🐉 ENHANCED KALI LINUX CTF LAUNCHER 🐉            ║
║                    Version {self.version} - Enhanced Edition                ║
║                                                               ║
║  Полная интеграция CTF инструментов с продвинутыми           ║
║  функциями: профили, история, автодополнение                 ║
║                                                               ║
║  Профиль: {self.current_profile:<20} Инструментов: {len(self.ctf_tools):<2}        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)
    
    def show_main_menu(self):
        """Показать главное меню"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}ГЛАВНОЕ МЕНЮ:{Colors.RESET}\n")
        
        print(f"{Colors.SUCCESS}[1-15]{Colors.RESET} CTF Инструменты ({len(self.ctf_tools)} доступно)")
        print(f"{Colors.SUCCESS}[C]{Colors.RESET} Поиск по категориям")
        print(f"{Colors.SUCCESS}[F]{Colors.RESET} Избранные инструменты")
        print(f"{Colors.SUCCESS}[H]{Colors.RESET} История команд")
        print(f"{Colors.SUCCESS}[P]{Colors.RESET} Управление профилями")
        print(f"{Colors.SUCCESS}[Q]{Colors.RESET} Быстрые команды Kali")
        print(f"{Colors.SUCCESS}[K]{Colors.RESET} Kali инструменты")
        print(f"{Colors.SUCCESS}[S]{Colors.RESET} Системная информация")
        print(f"{Colors.SUCCESS}[T]{Colors.RESET} Проверка инструментов")
        print(f"{Colors.WARNING}[0]{Colors.RESET} Выход\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_tools_menu(self):
        """Показать меню инструментов с категориями"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}CTF ИНСТРУМЕНТЫ:{Colors.RESET}\n")
        
        # Группируем инструменты по категориям
        categories = {}
        for key, tool in self.ctf_tools.items():
            category = tool.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append((key, tool))
        
        # Показываем инструменты по категориям
        for category, tools in sorted(categories.items()):
            print(f"{Colors.HEADER}📁 {category}:{Colors.RESET}")
            for key, tool in sorted(tools):
                exists = "✅" if self.check_tool_exists(tool['script']) else "❌"
                print(f"  {Colors.SUCCESS}[{key}]{Colors.RESET} {exists} {tool['name']}")
                print(f"      {Colors.INFO}{tool['desc']}{Colors.RESET}")
            print()
        
        print(f"{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_categories_menu(self):
        """Показать меню категорий"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}КАТЕГОРИИ ИНСТРУМЕНТОВ:{Colors.RESET}\n")
        
        # Группируем инструменты по категориям
        categories = {}
        for key, tool in self.ctf_tools.items():
            category = tool.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append((key, tool))
        
        # Показываем категории
        category_keys = {}
        for i, (category, tools) in enumerate(sorted(categories.items()), 1):
            category_keys[str(i)] = category
            print(f"{Colors.SUCCESS}[{i}]{Colors.RESET} {category} ({len(tools)} инструментов)")
            for key, tool in tools:
                exists = "✅" if self.check_tool_exists(tool['script']) else "❌"
                print(f"    {Colors.INFO}{exists} {tool['name']}{Colors.RESET}")
            print()
        
        print(f"{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        
        return category_keys
    
    def show_favorites_menu(self):
        """Показать избранные инструменты"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}ИЗБРАННЫЕ ИНСТРУМЕНТЫ:{Colors.RESET}\n")
        
        if self.current_profile not in self.user_profiles:
            self.user_profiles[self.current_profile] = {'name': self.current_profile, 'favorites': []}
        
        favorites = self.user_profiles[self.current_profile].get('favorites', [])
        
        if not favorites:
            print(f"{Colors.WARNING}Нет избранных инструментов в профиле '{self.current_profile}'{Colors.RESET}")
            print(f"{Colors.INFO}Добавьте инструменты в избранное через меню инструментов{Colors.RESET}")
        else:
            for i, tool_key in enumerate(favorites, 1):
                if tool_key in self.ctf_tools:
                    tool = self.ctf_tools[tool_key]
                    exists = "✅" if self.check_tool_exists(tool['script']) else "❌"
                    print(f"{Colors.SUCCESS}[{i}]{Colors.RESET} {exists} {tool['name']}")
                    print(f"    {Colors.INFO}{tool['desc']}{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}[{i}] Инструмент не найден: {tool_key}{Colors.RESET}")
        
        print(f"\n{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_history_menu(self):
        """Показать историю команд"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}ИСТОРИЯ КОМАНД:{Colors.RESET}\n")
        
        if not self.command_history:
            print(f"{Colors.WARNING}История команд пуста{Colors.RESET}")
        else:
            # Показываем последние 20 команд
            recent_history = self.command_history[-20:]
            for i, entry in enumerate(reversed(recent_history), 1):
                timestamp = entry.get('timestamp', 'Unknown')
                command = entry.get('command', 'Unknown')
                profile = entry.get('profile', 'default')
                
                # Форматируем время
                try:
                    dt = datetime.fromisoformat(timestamp)
                    time_str = dt.strftime("%H:%M:%S")
                except:
                    time_str = "Unknown"
                
                print(f"{Colors.SUCCESS}[{i}]{Colors.RESET} {time_str} | {profile}")
                print(f"    {Colors.INFO}{command}{Colors.RESET}")
        
        print(f"\n{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_profiles_menu(self):
        """Показать меню управления профилями"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}УПРАВЛЕНИЕ ПРОФИЛЯМИ:{Colors.RESET}\n")
        
        print(f"{Colors.INFO}Текущий профиль: {Colors.SUCCESS}{self.current_profile}{Colors.RESET}\n")
        
        print(f"{Colors.SUCCESS}[1]{Colors.RESET} Создать новый профиль")
        print(f"{Colors.SUCCESS}[2]{Colors.RESET} Переключить профиль")
        print(f"{Colors.SUCCESS}[3]{Colors.RESET} Удалить профиль")
        print(f"{Colors.SUCCESS}[4]{Colors.RESET} Показать все профили")
        print(f"{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_tools_check(self):
        """Проверка доступности инструментов"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}ПРОВЕРКА ИНСТРУМЕНТОВ:{Colors.RESET}\n")
        
        available = 0
        missing = 0
        
        for key, tool in self.ctf_tools.items():
            script_path = self.ctf_tools_dir / tool['script']
            if script_path.exists():
                print(f"{Colors.SUCCESS}✅{Colors.RESET} {tool['name']} - {tool['script']}")
                available += 1
            else:
                print(f"{Colors.ERROR}❌{Colors.RESET} {tool['name']} - {tool['script']} (НЕ НАЙДЕН)")
                missing += 1
        
        print(f"\n{Colors.HEADER}Статистика:{Colors.RESET}")
        print(f"{Colors.SUCCESS}Доступно: {available}{Colors.RESET}")
        print(f"{Colors.ERROR}Отсутствует: {missing}{Colors.RESET}")
        print(f"{Colors.INFO}Всего: {available + missing}{Colors.RESET}")
        
        print(f"\n{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_quick_commands(self):
        """Показать быстрые команды"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}БЫСТРЫЕ КОМАНДЫ KALI:{Colors.RESET}\n")
        
        for key, cmd in self.kali_quick_commands.items():
            print(f"{Colors.SUCCESS}[{key}]{Colors.RESET} {cmd['name']}")
            print(f"    {Colors.INFO}{cmd['desc']}{Colors.RESET}")
            print(f"    {Colors.WARNING}Команда: {cmd['command']}{Colors.RESET}\n")
        
        print(f"{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_kali_tools(self):
        """Показать доступные Kali инструменты"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}KALI ИНСТРУМЕНТЫ:{Colors.RESET}\n")
        
        try:
            subprocess.run(['python3', 'kali_integration.py', '--list-tools'], check=True)
        except:
            print_error("Не удалось получить список Kali инструментов")
        
        print(f"\n{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_system_info(self):
        """Показать системную информацию"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}СИСТЕМНАЯ ИНФОРМАЦИЯ:{Colors.RESET}\n")
        
        try:
            # Информация о системе
            print_info("Информация о системе:")
            subprocess.run(['uname', '-a'], check=True)
            
            print_info("\nВерсия Kali Linux:")
            subprocess.run(['cat', '/etc/os-release'], check=True)
            
            print_info("\nДоступные сетевые интерфейсы:")
            subprocess.run(['ip', 'addr', 'show'], check=True)
            
            print_info("\nАктивные сетевые соединения:")
            subprocess.run(['netstat', '-tuln'], check=True)
            
        except Exception as e:
            print_error(f"Ошибка получения системной информации: {e}")
        
        print(f"\n{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def run_tool(self, tool_key: str):
        """Запустить инструмент"""
        if tool_key not in self.ctf_tools:
            print_error("Неверный выбор!")
            return
        
        tool = self.ctf_tools[tool_key]
        
        # Проверяем существование инструмента
        if not self.check_tool_exists(tool['script']):
            print_error(f"Инструмент {tool['script']} не найден!")
            print_info("Используйте 'T' для проверки всех инструментов")
            input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
            return
        
        clear_screen()
        print_banner(tool['name'])
        
        print(f"\n{Colors.INFO}Описание:{Colors.RESET}")
        print(f"  {tool['desc']}")
        print(f"\n{Colors.INFO}Категория:{Colors.RESET}")
        print(f"  {tool.get('category', 'Other')}")
        print(f"\n{Colors.INFO}Скрипт:{Colors.RESET}")
        print(f"  {tool['script']}")
        
        print(f"\n{Colors.INFO}Примеры использования:{Colors.RESET}")
        for i, example in enumerate(tool['examples'], 1):
            print(f"  {i}. python3 {tool['script']} {example}")
        
        print(f"\n{Colors.INFO}Для справки используйте:{Colors.RESET}")
        print(f"  python3 {tool['script']} --help\n")
        
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.WARNING}Выберите действие:{Colors.RESET}\n")
        print(f"{Colors.SUCCESS}[1]{Colors.RESET} Запустить с параметрами")
        print(f"{Colors.SUCCESS}[2]{Colors.RESET} Показать справку (--help)")
        print(f"{Colors.SUCCESS}[3]{Colors.RESET} Добавить в избранное")
        print(f"{Colors.SUCCESS}[4]{Colors.RESET} Запустить с примером")
        print(f"{Colors.SUCCESS}[0]{Colors.RESET} Вернуться в главное меню\n")
        
        choice = input(f"{Colors.INFO}Ваш выбор: {Colors.RESET}").strip()
        
        if choice == '1':
            params = input(f"\n{Colors.INFO}Введите параметры: {Colors.RESET}").strip()
            cmd = f"python3 {tool['script']} {params}"
            print(f"\n{Colors.INFO}Запуск: {cmd}{Colors.RESET}\n")
            print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}\n")
            
            # Добавляем в историю
            self.add_to_history(cmd)
            
            try:
                subprocess.run(cmd, shell=True)
            except KeyboardInterrupt:
                print_warning("\nПрервано пользователем")
            except Exception as e:
                print_error(f"Ошибка: {e}")
        
        elif choice == '2':
            cmd = f"python3 {tool['script']} --help"
            print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}\n")
            subprocess.run(cmd, shell=True)
        
        elif choice == '3':
            self.add_to_favorites(tool_key)
        
        elif choice == '4':
            self.run_with_example(tool)
        
        input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
    
    def add_to_favorites(self, tool_key: str):
        """Добавить инструмент в избранное"""
        if self.current_profile not in self.user_profiles:
            self.user_profiles[self.current_profile] = {'name': self.current_profile, 'favorites': []}
        
        favorites = self.user_profiles[self.current_profile]['favorites']
        if tool_key not in favorites:
            favorites.append(tool_key)
            self.save_profiles()
            print_success(f"Инструмент добавлен в избранное профиля '{self.current_profile}'")
        else:
            print_warning("Инструмент уже в избранном")
    
    def run_with_example(self, tool: dict):
        """Запустить инструмент с примером"""
        print(f"\n{Colors.INFO}Выберите пример:{Colors.RESET}")
        for i, example in enumerate(tool['examples'], 1):
            print(f"  {i}. {example}")
        
        try:
            choice = int(input(f"\n{Colors.INFO}Номер примера [1-{len(tool['examples'])}]: {Colors.RESET}"))
            if 1 <= choice <= len(tool['examples']):
                example = tool['examples'][choice - 1]
                cmd = f"python3 {tool['script']} {example}"
                print(f"\n{Colors.INFO}Запуск: {cmd}{Colors.RESET}\n")
                print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}\n")
                
                # Добавляем в историю
                self.add_to_history(cmd)
                
                subprocess.run(cmd, shell=True)
            else:
                print_error("Неверный номер примера")
        except ValueError:
            print_error("Введите корректный номер")
        except KeyboardInterrupt:
            print_warning("\nПрервано пользователем")
        except Exception as e:
            print_error(f"Ошибка: {e}")
    
    def run_quick_command(self, cmd_key: str):
        """Запустить быструю команду"""
        if cmd_key not in self.kali_quick_commands:
            print_error("Неверный выбор!")
            return
        
        cmd_info = self.kali_quick_commands[cmd_key]
        
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}{cmd_info['name']}{Colors.RESET}\n")
        print(f"{Colors.INFO}Описание: {cmd_info['desc']}{Colors.RESET}")
        print(f"{Colors.WARNING}Команда: {cmd_info['command']}{Colors.RESET}\n")
        
        # Заменяем TARGET на введенный пользователем
        if 'TARGET' in cmd_info['command']:
            target = input(f"{Colors.INFO}Введите цель (TARGET): {Colors.RESET}").strip()
            if not target:
                print_error("Цель не указана!")
                return
            cmd = cmd_info['command'].replace('TARGET', target)
        else:
            cmd = cmd_info['command']
        
        print(f"\n{Colors.INFO}Выполнение: {cmd}{Colors.RESET}\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}\n")
        
        try:
            subprocess.run(cmd, shell=True)
        except KeyboardInterrupt:
            print_warning("\nПрервано пользователем")
        except Exception as e:
            print_error(f"Ошибка: {e}")
        
        input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
    
    def run(self):
        """Главный цикл"""
        while True:
            clear_screen()
            self.show_banner()
            self.show_main_menu()
            
            choice = input(f"\n{Colors.INFO}Выберите опцию: {Colors.RESET}").strip().upper()
            
            if choice == '0':
                self.save_config()
                print_success("До встречи на CTF! 🐉")
                sys.exit(0)
            
            elif choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
                self.run_tool(choice)
            
            elif choice == 'C':
                self.handle_categories_menu()
            
            elif choice == 'F':
                self.handle_favorites_menu()
            
            elif choice == 'H':
                while True:
                    clear_screen()
                    self.show_history_menu()
                    input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
                    break
            
            elif choice == 'P':
                self.handle_profiles_menu()
            
            elif choice == 'Q':
                while True:
                    clear_screen()
                    self.show_quick_commands()
                    cmd_choice = input(f"\n{Colors.INFO}Выберите команду [0-8]: {Colors.RESET}").strip()
                    
                    if cmd_choice == '0':
                        break
                    elif cmd_choice in self.kali_quick_commands:
                        self.run_quick_command(cmd_choice)
                    else:
                        print_error("Неверный выбор!")
                        time.sleep(1)
            
            elif choice == 'K':
                while True:
                    clear_screen()
                    self.show_kali_tools()
                    input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
                    break
            
            elif choice == 'S':
                while True:
                    clear_screen()
                    self.show_system_info()
                    input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
                    break
            
            elif choice == 'T':
                while True:
                    clear_screen()
                    self.show_tools_check()
                    input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
                    break
            
            else:
                print_error("Неверный выбор!")
                time.sleep(1)
    
    def handle_categories_menu(self):
        """Обработка меню категорий"""
        while True:
            clear_screen()
            category_keys = self.show_categories_menu()
            choice = input(f"\n{Colors.INFO}Выберите категорию [0-{len(category_keys)}]: {Colors.RESET}").strip()
            
            if choice == '0':
                break
            elif choice in category_keys:
                category = category_keys[choice]
                self.show_category_tools(category)
            else:
                print_error("Неверный выбор!")
                time.sleep(1)
    
    def show_category_tools(self, category: str):
        """Показать инструменты категории"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}КАТЕГОРИЯ: {category.upper()}{Colors.RESET}\n")
        
        tools_in_category = []
        for key, tool in self.ctf_tools.items():
            if tool.get('category', 'Other') == category:
                tools_in_category.append((key, tool))
        
        for key, tool in sorted(tools_in_category):
            exists = "✅" if self.check_tool_exists(tool['script']) else "❌"
            print(f"{Colors.SUCCESS}[{key}]{Colors.RESET} {exists} {tool['name']}")
            print(f"    {Colors.INFO}{tool['desc']}{Colors.RESET}")
        
        print(f"\n{Colors.WARNING}[0]{Colors.RESET} Назад к категориям\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        
        choice = input(f"\n{Colors.INFO}Выберите инструмент: {Colors.RESET}").strip()
        if choice != '0' and choice in [key for key, _ in tools_in_category]:
            self.run_tool(choice)
    
    def handle_favorites_menu(self):
        """Обработка меню избранных"""
        while True:
            clear_screen()
            self.show_favorites_menu()
            
            if self.current_profile not in self.user_profiles:
                self.user_profiles[self.current_profile] = {'name': self.current_profile, 'favorites': []}
            
            favorites = self.user_profiles[self.current_profile].get('favorites', [])
            
            if not favorites:
                input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
                break
            
            choice = input(f"\n{Colors.INFO}Выберите инструмент [0-{len(favorites)}]: {Colors.RESET}").strip()
            
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(favorites):
                tool_key = favorites[int(choice) - 1]
                if tool_key in self.ctf_tools:
                    self.run_tool(tool_key)
                else:
                    print_error("Инструмент не найден!")
                    time.sleep(1)
            else:
                print_error("Неверный выбор!")
                time.sleep(1)
    
    def handle_profiles_menu(self):
        """Обработка меню профилей"""
        while True:
            clear_screen()
            self.show_profiles_menu()
            choice = input(f"\n{Colors.INFO}Выберите действие [0-4]: {Colors.RESET}").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.create_profile()
            elif choice == '2':
                self.switch_profile()
            elif choice == '3':
                self.delete_profile()
            elif choice == '4':
                self.show_all_profiles()
            else:
                print_error("Неверный выбор!")
                time.sleep(1)
    
    def create_profile(self):
        """Создать новый профиль"""
        name = input(f"\n{Colors.INFO}Введите имя профиля: {Colors.RESET}").strip()
        if name and name not in self.user_profiles:
            self.user_profiles[name] = {'name': name, 'favorites': []}
            self.save_profiles()
            print_success(f"Профиль '{name}' создан")
        elif name in self.user_profiles:
            print_error("Профиль уже существует")
        else:
            print_error("Неверное имя профиля")
        input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
    
    def switch_profile(self):
        """Переключить профиль"""
        if len(self.user_profiles) <= 1:
            print_warning("Создайте дополнительные профили для переключения")
            input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
            return
        
        print(f"\n{Colors.INFO}Доступные профили:{Colors.RESET}")
        profiles = list(self.user_profiles.keys())
        for i, profile in enumerate(profiles, 1):
            marker = " (текущий)" if profile == self.current_profile else ""
            print(f"  {i}. {profile}{marker}")
        
        try:
            choice = int(input(f"\n{Colors.INFO}Выберите профиль [1-{len(profiles)}]: {Colors.RESET}"))
            if 1 <= choice <= len(profiles):
                new_profile = profiles[choice - 1]
                if new_profile != self.current_profile:
                    self.current_profile = new_profile
                    self.save_config()
                    print_success(f"Переключен на профиль '{new_profile}'")
                else:
                    print_warning("Этот профиль уже активен")
            else:
                print_error("Неверный выбор")
        except ValueError:
            print_error("Введите корректный номер")
        
        input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
    
    def delete_profile(self):
        """Удалить профиль"""
        if len(self.user_profiles) <= 1:
            print_warning("Нельзя удалить единственный профиль")
            input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
            return
        
        print(f"\n{Colors.INFO}Доступные профили:{Colors.RESET}")
        profiles = list(self.user_profiles.keys())
        for i, profile in enumerate(profiles, 1):
            marker = " (текущий)" if profile == self.current_profile else ""
            print(f"  {i}. {profile}{marker}")
        
        try:
            choice = int(input(f"\n{Colors.INFO}Выберите профиль для удаления [1-{len(profiles)}]: {Colors.RESET}"))
            if 1 <= choice <= len(profiles):
                profile_to_delete = profiles[choice - 1]
                if profile_to_delete == self.current_profile:
                    print_error("Нельзя удалить активный профиль")
                else:
                    if get_user_confirmation(f"Удалить профиль '{profile_to_delete}'?"):
                        del self.user_profiles[profile_to_delete]
                        self.save_profiles()
                        print_success(f"Профиль '{profile_to_delete}' удален")
            else:
                print_error("Неверный выбор")
        except ValueError:
            print_error("Введите корректный номер")
        
        input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
    
    def show_all_profiles(self):
        """Показать все профили"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}ВСЕ ПРОФИЛИ:{Colors.RESET}\n")
        
        for profile_name, profile_data in self.user_profiles.items():
            marker = " (текущий)" if profile_name == self.current_profile else ""
            print(f"{Colors.SUCCESS}📁 {profile_name}{marker}{Colors.RESET}")
            favorites = profile_data.get('favorites', [])
            print(f"    Избранных инструментов: {len(favorites)}")
            if favorites:
                for fav in favorites:
                    if fav in self.ctf_tools:
                        tool_name = self.ctf_tools[fav]['name']
                        print(f"      - {tool_name}")
            print()
        
        print(f"{Colors.WARNING}[0]{Colors.RESET} Назад к управлению профилями\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        
        input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")

def main():
    try:
        launcher = EnhancedKaliCTFLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Выход...{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

