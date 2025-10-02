#!/usr/bin/env python3
"""
CTF Tools Launcher - Главное меню для запуска всех CTF инструментов
"""

import sys
import subprocess
from utils import *

class CTFLauncher:
    """Главное меню запуска CTF инструментов"""
    
    def __init__(self):
        self.tools = {
            '1': {
                'name': 'Network Tools',
                'desc': 'Сканирование портов, перехват трафика',
                'script': 'network_tools.py',
                'examples': [
                    '--scan-common 192.168.1.1',
                    '--ping-sweep 192.168.1.0/24',
                    '--banner-grab 192.168.1.1 --ports 80,443'
                ]
            },
            '2': {
                'name': 'Web Exploitation',
                'desc': 'SQL injection, XSS, Directory brute-force',
                'script': 'web_exploit.py',
                'examples': [
                    '--url http://target.com --test-all',
                    '--url http://target.com/page.php?id=1 --test-sqli',
                    '--url http://target.com --bruteforce'
                ]
            },
            '3': {
                'name': 'Crypto Tools',
                'desc': 'Взлом хешей, шифрование/дешифрование',
                'script': 'crypto_tools.py',
                'examples': [
                    '--crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5',
                    '--caesar "KHOOR" --shift 3 --decrypt',
                    '--encode "Hello" --encoding base64'
                ]
            },
            '4': {
                'name': 'Payload Generator',
                'desc': 'Генерация пейлоадов для эксплуатации',
                'script': 'payload_generator.py',
                'examples': [
                    '--xss --context html',
                    '--sqli --dbms mysql',
                    '--reverse-shell 10.10.10.1 4444 --shell-type bash'
                ]
            },
            '5': {
                'name': 'Defense Monitor',
                'desc': 'Мониторинг системы и обнаружение атак',
                'script': 'defense_monitor.py',
                'examples': [
                    '--monitor-network --duration 120',
                    '--check-processes',
                    '--monitor-ports --duration 300'
                ]
            },
            '6': {
                'name': 'Steganography',
                'desc': 'Скрытие и извлечение данных из файлов',
                'script': 'steganography.py',
                'examples': [
                    '--hide-text image.png "Secret" output.png',
                    '--extract-text stego.png',
                    '--analyze image.png'
                ]
            },
            '7': {
                'name': 'OSINT Tools',
                'desc': 'Разведка и сбор информации',
                'script': 'osint_tools.py',
                'examples': [
                    '--whois example.com',
                    '--dns example.com',
                    '--subdomains example.com',
                    '--username john_doe'
                ]
            },
            '8': {
                'name': 'Tor Integration',
                'desc': 'Анонимность через Tor',
                'script': 'tor_integration.py',
                'examples': [
                    '--check-tor',
                    '--get-ip',
                    '--scan-url https://example.com',
                    '--scan-onion facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion'
                ]
            },
            '9': {
                'name': 'Social Engineering',
                'desc': 'Инструменты социальной инженерии (только CTF)',
                'script': 'social_engineering.py',
                'examples': [
                    '--target https://example.com --clone-only',
                    '--target https://bank.com --clone-phishing',
                    '--target https://login.site.com --phishing-only --template bank'
                ]
            },
            '10': {
                'name': 'Advanced Crypto',
                'desc': 'Продвинутые криптографические инструменты',
                'script': 'advanced_crypto.py',
                'examples': [
                    '--encrypt "Hello" --method aes --key "secretkey"',
                    '--generate-rsa 2048',
                    '--crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 --hash-type md5'
                ]
            },
            '11': {
                'name': 'Malware Analysis',
                'desc': 'Анализ вредоносного ПО (только CTF)',
                'script': 'malware_analysis.py',
                'examples': [
                    '--file suspicious.exe',
                    '--file malware.bin --pe-only',
                    '--file sample.exe --yara-only'
                ]
            },
            '12': {
                'name': 'OSINT Investigator',
                'desc': 'Поиск информации о человеке через Tor (только CTF)',
                'script': 'osint_investigator.py',
                'examples': [
                    '--username john_doe --email john@example.com',
                    '--phone +1234567890 --name "John Doe"',
                    '--username target_user --html-report'
                ]
            },
            '13': {
                'name': 'Phishing Server',
                'desc': 'HTTP сервер для сбора данных с фишинговых страниц (только CTF)',
                'script': 'phishing_server.py',
                'examples': [
                    '--port 8080',
                    '--port 3000'
                ]
            },
        }
    
    def show_banner(self):
        """Показать главный баннер"""
        banner = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║               CTF TOOLS COLLECTION LAUNCHER                   ║
║                    Version 1.0                                ║
║                                                               ║
║  Комплексный набор инструментов для CTF соревнований         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)
    
    def show_menu(self):
        """Показать главное меню"""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.HEADER}ДОСТУПНЫЕ ИНСТРУМЕНТЫ:{Colors.RESET}\n")
        
        for key, tool in sorted(self.tools.items()):
            print(f"{Colors.SUCCESS}[{key}]{Colors.RESET} {tool['name']}")
            print(f"    {Colors.INFO}{tool['desc']}{Colors.RESET}\n")
        
        print(f"{Colors.WARNING}[0]{Colors.RESET} Выход\n")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    
    def show_tool_info(self, tool_key: str):
        """Показать информацию об инструменте"""
        if tool_key not in self.tools:
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
    
    def run_tool(self, tool_key: str):
        """Запустить инструмент"""
        if tool_key not in self.tools:
            print_error("Неверный выбор!")
            return
        
        tool = self.tools[tool_key]
        
        self.show_tool_info(tool_key)
        
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
    
    def run(self):
        """Главный цикл"""
        while True:
            clear_screen()
            self.show_banner()
            self.show_menu()
            
            choice = input(f"\n{Colors.INFO}Выберите инструмент [0-13]: {Colors.RESET}").strip()
            
            if choice == '0':
                print_success("До встречи на CTF!")
                sys.exit(0)
            
            elif choice in self.tools:
                self.run_tool(choice)
            
            else:
                print_error("Неверный выбор!")
                time.sleep(1)

def main():
    try:
        launcher = CTFLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Выход...{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


