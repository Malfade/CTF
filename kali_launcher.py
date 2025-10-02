#!/usr/bin/env python3
"""
Kali Linux CTF Launcher - Специальный launcher для Kali Linux
"""

import sys
import subprocess
import os
from utils import *

class KaliCTFLauncher:
    """Специальный launcher для Kali Linux"""
    
    def __init__(self):
        self.tools = {
            '1': {
                'name': 'Network Tools (Enhanced)',
                'desc': 'Сканирование портов с nmap интеграцией',
                'script': 'network_tools.py',
                'examples': [
                    '--nmap-scan 192.168.1.1 --nmap-type aggressive',
                    '--os-detect 192.168.1.1',
                    '--vuln-scan 192.168.1.1'
                ]
            },
            '2': {
                'name': 'Web Exploitation',
                'desc': 'SQL injection, XSS, Directory brute-force',
                'script': 'web_exploit.py',
                'examples': [
                    '--url http://target.com --test-all',
                    '--url http://target.com/page.php?id=1 --test-sqli'
                ]
            },
            '3': {
                'name': 'Crypto Tools',
                'desc': 'Взлом хешей, шифрование/дешифрование',
                'script': 'crypto_tools.py',
                'examples': [
                    '--crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5',
                    '--caesar-bruteforce "KHOOR"'
                ]
            },
            '4': {
                'name': 'Kali Integration',
                'desc': 'Интеграция с инструментами Kali Linux',
                'script': 'kali_integration.py',
                'examples': [
                    '--list-tools',
                    '--nmap 192.168.1.1 --scan-type aggressive',
                    '--nikto http://target.com',
                    '--john hashes.txt --wordlist /usr/share/wordlists/rockyou.txt'
                ]
            },
            '5': {
                'name': 'OSINT Tools',
                'desc': 'Разведка и сбор информации',
                'script': 'osint_tools.py',
                'examples': [
                    '--whois example.com',
                    '--subdomains example.com',
                    '--username john_doe'
                ]
            },
            '6': {
                'name': 'Tor Integration',
                'desc': 'Анонимность через Tor',
                'script': 'tor_integration.py',
                'examples': [
                    '--check-tor',
                    '--scan-url https://target.com',
                    '--scan-onion facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion'
                ]
            },
            '7': {
                'name': 'Payload Generator',
                'desc': 'Генерация пейлоадов для эксплуатации',
                'script': 'payload_generator.py',
                'examples': [
                    '--xss --context html',
                    '--reverse-shell 10.10.10.1 4444 --shell-type bash'
                ]
            },
            '8': {
                'name': 'Steganography',
                'desc': 'Скрытие и извлечение данных из файлов',
                'script': 'steganography.py',
                'examples': [
                    '--extract-text image.png',
                    '--analyze image.png'
                ]
            },
            '9': {
                'name': 'Forensics',
                'desc': 'Цифровая форензика',
                'script': 'forensics.py',
                'examples': [
                    '--file suspicious.bin --analyze',
                    '--file file.bin --strings --min-length 6'
                ]
            },
            '10': {
                'name': 'Defense Monitor',
                'desc': 'Мониторинг системы и обнаружение атак',
                'script': 'defense_monitor.py',
                'examples': [
                    '--monitor-network --duration 120',
                    '--check-processes'
                ]
            },
            '11': {
                'name': 'Wordlist Generator',
                'desc': 'Генерация словарей для брутфорса',
                'script': 'wordlist_generator.py',
                'examples': [
                    '--numeric --min 4 --max 6 -o pins.txt',
                    '--common --apply-rules -o passwords.txt'
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
    
    def show_banner(self):
        """Показать баннер Kali Linux"""
        banner = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              🐉 KALI LINUX CTF TOOLS LAUNCHER 🐉             ║
║                    Version 2.0 - Kali Edition                 ║
║                                                               ║
║  Специальная версия для Kali Linux с интеграцией             ║
║  популярных инструментов безопасности                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)
    
    def show_main_menu(self):
        """Показать главное меню"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}ГЛАВНОЕ МЕНЮ:{Colors.RESET}\n")
        
        print(f"{Colors.SUCCESS}[1-11]{Colors.RESET} CTF Инструменты")
        print(f"{Colors.SUCCESS}[Q]{Colors.RESET} Быстрые команды Kali")
        print(f"{Colors.SUCCESS}[K]{Colors.RESET} Kali инструменты")
        print(f"{Colors.SUCCESS}[S]{Colors.RESET} Системная информация")
        print(f"{Colors.WARNING}[0]{Colors.RESET} Выход\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_tools_menu(self):
        """Показать меню инструментов"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}CTF ИНСТРУМЕНТЫ:{Colors.RESET}\n")
        
        for key, tool in sorted(self.tools.items()):
            print(f"{Colors.SUCCESS}[{key}]{Colors.RESET} {tool['name']}")
            print(f"    {Colors.INFO}{tool['desc']}{Colors.RESET}\n")
        
        print(f"{Colors.WARNING}[0]{Colors.RESET} Назад в главное меню\n")
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
        if tool_key not in self.tools:
            print_error("Неверный выбор!")
            return
        
        tool = self.tools[tool_key]
        
        clear_screen()
        print_banner(tool['name'])
        
        print(f"\n{Colors.INFO}Описание:{Colors.RESET}")
        print(f"  {tool['desc']}\n")
        
        print(f"{Colors.INFO}Примеры использования:{Colors.RESET}")
        for i, example in enumerate(tool['examples'], 1):
            print(f"  {i}. python3 {tool['script']} {example}")
        
        print(f"\n{Colors.INFO}Для справки используйте:{Colors.RESET}")
        print(f"  python3 {tool['script']} --help\n")
        
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.WARNING}Выберите действие:{Colors.RESET}\n")
        print(f"{Colors.SUCCESS}[1]{Colors.RESET} Запустить с параметрами")
        print(f"{Colors.SUCCESS}[2]{Colors.RESET} Показать справку (--help)")
        print(f"{Colors.SUCCESS}[0]{Colors.RESET} Вернуться в главное меню\n")
        
        choice = input(f"{Colors.INFO}Ваш выбор: {Colors.RESET}").strip()
        
        if choice == '1':
            params = input(f"\n{Colors.INFO}Введите параметры: {Colors.RESET}").strip()
            cmd = f"python3 {tool['script']} {params}"
            print(f"\n{Colors.INFO}Запуск: {cmd}{Colors.RESET}\n")
            print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}\n")
            
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
        
        input(f"\n{Colors.WARNING}Нажмите Enter для продолжения...{Colors.RESET}")
    
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
                print_success("До встречи на CTF! 🐉")
                sys.exit(0)
            
            elif choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
                self.run_tool(choice)
            
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
            
            else:
                print_error("Неверный выбор!")
                time.sleep(1)

def main():
    try:
        launcher = KaliCTFLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Выход...{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

