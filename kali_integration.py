#!/usr/bin/env python3
"""
Kali Linux Integration - Интеграция с инструментами Kali Linux
"""

import subprocess
import argparse
import sys
import os
import json
from typing import List, Dict, Optional
from utils import *

class KaliToolsManager:
    """Менеджер инструментов Kali Linux"""
    
    def __init__(self):
        self.kali_tools = {
            'reconnaissance': {
                'nmap': '/usr/bin/nmap',
                'masscan': '/usr/bin/masscan',
                'zmap': '/usr/bin/zmap',
                'dnsrecon': '/usr/bin/dnsrecon',
                'fierce': '/usr/bin/fierce',
                'dmitry': '/usr/bin/dmitry',
                'theharvester': '/usr/bin/theharvester',
                'recon-ng': '/usr/bin/recon-ng',
                'maltego': '/usr/bin/maltego',
                'spiderfoot': '/usr/bin/spiderfoot'
            },
            'vulnerability_assessment': {
                'nessus': '/opt/nessus/bin/nessus',
                'openvas': '/usr/bin/openvas',
                'nikto': '/usr/bin/nikto',
                'skipfish': '/usr/bin/skipfish',
                'w3af': '/usr/bin/w3af',
                'burpsuite': '/usr/bin/burpsuite',
                'zaproxy': '/usr/bin/zaproxy',
                'sqlmap': '/usr/bin/sqlmap',
                'commix': '/usr/bin/commix',
                'wpscan': '/usr/bin/wpscan'
            },
            'exploitation': {
                'metasploit': '/usr/bin/msfconsole',
                'armitage': '/usr/bin/armitage',
                'beef': '/usr/bin/beef',
                'set': '/usr/bin/setoolkit',
                'weevely': '/usr/bin/weevely',
                'webshells': '/usr/share/webshells',
                'payloads': '/usr/share/payloads'
            },
            'forensics': {
                'volatility': '/usr/bin/vol.py',
                'autopsy': '/usr/bin/autopsy',
                'sleuthkit': '/usr/bin/fls',
                'bulk_extractor': '/usr/bin/bulk_extractor',
                'binwalk': '/usr/bin/binwalk',
                'foremost': '/usr/bin/foremost',
                'scalpel': '/usr/bin/scalpel',
                'testdisk': '/usr/bin/testdisk',
                'photorec': '/usr/bin/photorec'
            },
            'password_attacks': {
                'john': '/usr/bin/john',
                'hashcat': '/usr/bin/hashcat',
                'hydra': '/usr/bin/hydra',
                'medusa': '/usr/bin/medusa',
                'patator': '/usr/bin/patator',
                'crunch': '/usr/bin/crunch',
                'cewl': '/usr/bin/cewl',
                'wordlists': '/usr/share/wordlists'
            },
            'wireless': {
                'aircrack-ng': '/usr/bin/aircrack-ng',
                'reaver': '/usr/bin/reaver',
                'bully': '/usr/bin/bully',
                'wifite': '/usr/bin/wifite',
                'kismet': '/usr/bin/kismet',
                'wireshark': '/usr/bin/wireshark',
                'tshark': '/usr/bin/tshark'
            },
            'reverse_engineering': {
                'ghidra': '/usr/bin/ghidra',
                'radare2': '/usr/bin/r2',
                'gdb': '/usr/bin/gdb',
                'objdump': '/usr/bin/objdump',
                'strings': '/usr/bin/strings',
                'file': '/usr/bin/file',
                'hexdump': '/usr/bin/hexdump'
            },
            'steganography': {
                'steghide': '/usr/bin/steghide',
                'outguess': '/usr/bin/outguess',
                'stegsolve': '/usr/bin/stegsolve',
                'zsteg': '/usr/bin/zsteg',
                'exiftool': '/usr/bin/exiftool'
            }
        }
        self.available_tools = self.check_available_tools()
    
    def check_available_tools(self) -> Dict[str, List[str]]:
        """Проверка доступных инструментов Kali"""
        print_info("Проверка доступных инструментов Kali Linux...")
        
        available = {}
        for category, tools in self.kali_tools.items():
            available[category] = []
            for tool_name, tool_path in tools.items():
                if os.path.exists(tool_path) or self.check_command_exists(tool_name):
                    available[category].append(tool_name)
                    print_success(f"✓ {tool_name}")
                else:
                    print_warning(f"✗ {tool_name} (не найден)")
        
        return available
    
    def check_command_exists(self, command: str) -> bool:
        """Проверка существования команды в PATH"""
        try:
            subprocess.run(['which', command], capture_output=True, check=True)
            return True
        except:
            return False
    
    def list_available_tools(self) -> None:
        """Список доступных инструментов"""
        print_banner("KALI LINUX TOOLS")
        
        for category, tools in self.available_tools.items():
            if tools:
                print(f"\n{Colors.HEADER}{category.upper().replace('_', ' ')}{Colors.RESET}")
                for tool in tools:
                    print(f"  {Colors.SUCCESS}•{Colors.RESET} {tool}")
    
    def run_tool(self, tool_name: str, args: List[str] = None) -> Dict:
        """Запуск инструмента Kali"""
        if args is None:
            args = []
        
        # Поиск инструмента
        tool_path = None
        for category, tools in self.kali_tools.items():
            if tool_name in tools:
                tool_path = tools[tool_name]
                break
        
        if not tool_path:
            print_error(f"Инструмент {tool_name} не найден")
            return {}
        
        if not os.path.exists(tool_path) and not self.check_command_exists(tool_name):
            print_error(f"Инструмент {tool_name} не установлен")
            return {}
        
        print_info(f"Запуск {tool_name}...")
        
        try:
            cmd = [tool_name] + args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            return {
                'tool': tool_name,
                'command': ' '.join(cmd),
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            print_error(f"Инструмент {tool_name} превысил время ожидания")
            return {}
        except Exception as e:
            print_error(f"Ошибка запуска {tool_name}: {e}")
            return {}

class KaliReconnaissance:
    """Инструменты разведки Kali"""
    
    def __init__(self):
        self.manager = KaliToolsManager()
    
    def nmap_scan(self, target: str, scan_type: str = 'basic') -> Dict:
        """Nmap сканирование с различными профилями"""
        print_info(f"Nmap сканирование {target}...")
        
        scan_profiles = {
            'basic': ['-sS', '-O', '-sV', '--top-ports', '1000'],
            'aggressive': ['-A', '-sS', '-sV', '-O', '--script', 'vuln'],
            'stealth': ['-sS', '-T2', '-f', '--top-ports', '100'],
            'udp': ['-sU', '--top-ports', '100'],
            'vuln': ['-sS', '-sV', '--script', 'vuln'],
            'full': ['-sS', '-sV', '-O', '-A', '--script', 'vuln,discovery']
        }
        
        args = scan_profiles.get(scan_type, scan_profiles['basic'])
        args.append(target)
        
        return self.manager.run_tool('nmap', args)
    
    def theharvester_scan(self, domain: str, sources: str = 'google,bing,yahoo') -> Dict:
        """TheHarvester для сбора email и поддоменов"""
        print_info(f"TheHarvester сканирование {domain}...")
        
        args = ['-d', domain, '-b', sources, '-l', '500']
        return self.manager.run_tool('theharvester', args)
    
    def dnsrecon_scan(self, domain: str) -> Dict:
        """DNSrecon для DNS разведки"""
        print_info(f"DNSrecon сканирование {domain}...")
        
        args = ['-d', domain, '-t', 'std,axfr,brt,cache,srv,zone']
        return self.manager.run_tool('dnsrecon', args)
    
    def fierce_scan(self, domain: str) -> Dict:
        """Fierce для поиска поддоменов"""
        print_info(f"Fierce сканирование {domain}...")
        
        args = ['-dns', domain]
        return self.manager.run_tool('fierce', args)

class KaliWebTesting:
    """Инструменты тестирования веб-приложений"""
    
    def __init__(self):
        self.manager = KaliToolsManager()
    
    def nikto_scan(self, url: str) -> Dict:
        """Nikto для сканирования веб-серверов"""
        print_info(f"Nikto сканирование {url}...")
        
        args = ['-h', url, '-Format', 'txt']
        return self.manager.run_tool('nikto', args)
    
    def sqlmap_scan(self, url: str, data: str = None) -> Dict:
        """SQLMap для тестирования SQL injection"""
        print_info(f"SQLMap сканирование {url}...")
        
        args = ['-u', url, '--batch', '--dbs']
        if data:
            args.extend(['--data', data])
        
        return self.manager.run_tool('sqlmap', args)
    
    def wpscan_scan(self, url: str) -> Dict:
        """WPScan для тестирования WordPress"""
        print_info(f"WPScan сканирование {url}...")
        
        args = ['--url', url, '--enumerate', 'u,p,t']
        return self.manager.run_tool('wpscan', args)
    
    def dirb_scan(self, url: str, wordlist: str = None) -> Dict:
        """Dirb для брутфорса директорий"""
        print_info(f"Dirb сканирование {url}...")
        
        args = [url]
        if wordlist:
            args.extend(['-w', wordlist])
        
        return self.manager.run_tool('dirb', args)

class KaliPasswordAttacks:
    """Инструменты атак на пароли"""
    
    def __init__(self):
        self.manager = KaliToolsManager()
    
    def john_crack(self, hash_file: str, wordlist: str = None) -> Dict:
        """John the Ripper для взлома хешей"""
        print_info(f"John the Ripper взлом {hash_file}...")
        
        args = [hash_file]
        if wordlist:
            args.extend(['--wordlist', wordlist])
        
        return self.manager.run_tool('john', args)
    
    def hashcat_crack(self, hash_file: str, hash_type: str, wordlist: str = None) -> Dict:
        """Hashcat для взлома хешей"""
        print_info(f"Hashcat взлом {hash_file}...")
        
        args = ['-m', hash_type, hash_file]
        if wordlist:
            args.extend(['-a', '0', wordlist])
        else:
            args.extend(['-a', '3', '?a?a?a?a?a?a'])  # Брутфорс 6 символов
        
        return self.manager.run_tool('hashcat', args)
    
    def hydra_attack(self, target: str, service: str, username: str, wordlist: str) -> Dict:
        """Hydra для брутфорса паролей"""
        print_info(f"Hydra атака на {target}:{service}...")
        
        args = ['-l', username, '-P', wordlist, f'{service}://{target}']
        return self.manager.run_tool('hydra', args)
    
    def crunch_generate(self, min_len: int, max_len: int, charset: str, output: str) -> Dict:
        """Crunch для генерации словарей"""
        print_info(f"Crunch генерация словаря...")
        
        args = [str(min_len), str(max_len), charset, '-o', output]
        return self.manager.run_tool('crunch', args)

class KaliForensics:
    """Инструменты цифровой форензики"""
    
    def __init__(self):
        self.manager = KaliToolsManager()
    
    def volatility_analyze(self, memory_dump: str, plugin: str = 'pslist') -> Dict:
        """Volatility для анализа дампов памяти"""
        print_info(f"Volatility анализ {memory_dump}...")
        
        args = ['-f', memory_dump, plugin]
        return self.manager.run_tool('volatility', args)
    
    def binwalk_extract(self, file_path: str) -> Dict:
        """Binwalk для извлечения данных из файлов"""
        print_info(f"Binwalk извлечение из {file_path}...")
        
        args = ['-e', file_path]
        return self.manager.run_tool('binwalk', args)
    
    def foremost_recover(self, image_path: str, output_dir: str) -> Dict:
        """Foremost для восстановления файлов"""
        print_info(f"Foremost восстановление из {image_path}...")
        
        args = ['-i', image_path, '-o', output_dir]
        return self.manager.run_tool('foremost', args)
    
    def exiftool_analyze(self, file_path: str) -> Dict:
        """ExifTool для анализа метаданных"""
        print_info(f"ExifTool анализ {file_path}...")
        
        args = [file_path]
        return self.manager.run_tool('exiftool', args)

class KaliSteganography:
    """Инструменты стеганографии"""
    
    def __init__(self):
        self.manager = KaliToolsManager()
    
    def steghide_extract(self, image_path: str, passphrase: str = None) -> Dict:
        """Steghide для извлечения скрытых данных"""
        print_info(f"Steghide извлечение из {image_path}...")
        
        args = ['extract', '-sf', image_path]
        if passphrase:
            args.extend(['-p', passphrase])
        
        return self.manager.run_tool('steghide', args)
    
    def zsteg_analyze(self, image_path: str) -> Dict:
        """Zsteg для анализа стеганографии"""
        print_info(f"Zsteg анализ {image_path}...")
        
        args = ['-a', image_path]
        return self.manager.run_tool('zsteg', args)
    
    def outguess_extract(self, image_path: str, output_file: str) -> Dict:
        """Outguess для извлечения данных"""
        print_info(f"Outguess извлечение из {image_path}...")
        
        args = ['-r', image_path, output_file]
        return self.manager.run_tool('outguess', args)

def main():
    parser = argparse.ArgumentParser(
        description="Kali Linux Integration - Интеграция с Kali инструментами",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --list-tools
  %(prog)s --nmap 192.168.1.1 --scan-type aggressive
  %(prog)s --theharvester example.com
  %(prog)s --nikto http://target.com
  %(prog)s --sqlmap http://target.com/page.php?id=1
  %(prog)s --john hashes.txt --wordlist /usr/share/wordlists/rockyou.txt
  %(prog)s --hashcat hashes.txt --hash-type 0 --wordlist rockyou.txt
  %(prog)s --volatility memory.dmp --plugin pslist
  %(prog)s --binwalk suspicious.bin
  %(prog)s --steghide image.jpg
        """
    )
    
    # Общие опции
    parser.add_argument('--list-tools', action='store_true', help='Список доступных инструментов')
    
    # Разведка
    parser.add_argument('--nmap', metavar='TARGET', help='Nmap сканирование')
    parser.add_argument('--scan-type', choices=['basic', 'aggressive', 'stealth', 'udp', 'vuln', 'full'],
                       default='basic', help='Тип nmap сканирования')
    parser.add_argument('--theharvester', metavar='DOMAIN', help='TheHarvester сканирование')
    parser.add_argument('--dnsrecon', metavar='DOMAIN', help='DNSrecon сканирование')
    parser.add_argument('--fierce', metavar='DOMAIN', help='Fierce сканирование')
    
    # Веб-тестирование
    parser.add_argument('--nikto', metavar='URL', help='Nikto сканирование')
    parser.add_argument('--sqlmap', metavar='URL', help='SQLMap тестирование')
    parser.add_argument('--sqlmap-data', help='POST данные для SQLMap')
    parser.add_argument('--wpscan', metavar='URL', help='WPScan сканирование')
    parser.add_argument('--dirb', metavar='URL', help='Dirb сканирование')
    
    # Атаки на пароли
    parser.add_argument('--john', metavar='HASH_FILE', help='John the Ripper')
    parser.add_argument('--john-wordlist', help='Словарь для John')
    parser.add_argument('--hashcat', metavar='HASH_FILE', help='Hashcat')
    parser.add_argument('--hash-type', help='Тип хеша для Hashcat')
    parser.add_argument('--hashcat-wordlist', help='Словарь для Hashcat')
    parser.add_argument('--hydra', metavar='TARGET', help='Hydra атака')
    parser.add_argument('--hydra-service', help='Сервис для Hydra')
    parser.add_argument('--hydra-user', help='Пользователь для Hydra')
    parser.add_argument('--hydra-wordlist', help='Словарь для Hydra')
    parser.add_argument('--crunch', metavar=('MIN', 'MAX', 'CHARSET', 'OUTPUT'), nargs=4,
                       help='Crunch генерация словаря')
    
    # Форензика
    parser.add_argument('--volatility', metavar='MEMORY_DUMP', help='Volatility анализ')
    parser.add_argument('--volatility-plugin', default='pslist', help='Volatility плагин')
    parser.add_argument('--binwalk', metavar='FILE', help='Binwalk извлечение')
    parser.add_argument('--foremost', metavar=('IMAGE', 'OUTPUT'), nargs=2, help='Foremost восстановление')
    parser.add_argument('--exiftool', metavar='FILE', help='ExifTool анализ')
    
    # Стеганография
    parser.add_argument('--steghide', metavar='IMAGE', help='Steghide извлечение')
    parser.add_argument('--steghide-pass', help='Пароль для Steghide')
    parser.add_argument('--zsteg', metavar='IMAGE', help='Zsteg анализ')
    parser.add_argument('--outguess', metavar=('IMAGE', 'OUTPUT'), nargs=2, help='Outguess извлечение')
    
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    print_banner("KALI LINUX INTEGRATION")
    
    results = {}
    
    if args.list_tools:
        manager = KaliToolsManager()
        manager.list_available_tools()
        return
    
    # Разведка
    if args.nmap:
        recon = KaliReconnaissance()
        results['nmap'] = recon.nmap_scan(args.nmap, args.scan_type)
    
    elif args.theharvester:
        recon = KaliReconnaissance()
        results['theharvester'] = recon.theharvester_scan(args.theharvester)
    
    elif args.dnsrecon:
        recon = KaliReconnaissance()
        results['dnsrecon'] = recon.dnsrecon_scan(args.dnsrecon)
    
    elif args.fierce:
        recon = KaliReconnaissance()
        results['fierce'] = recon.fierce_scan(args.fierce)
    
    # Веб-тестирование
    elif args.nikto:
        web = KaliWebTesting()
        results['nikto'] = web.nikto_scan(args.nikto)
    
    elif args.sqlmap:
        web = KaliWebTesting()
        results['sqlmap'] = web.sqlmap_scan(args.sqlmap, args.sqlmap_data)
    
    elif args.wpscan:
        web = KaliWebTesting()
        results['wpscan'] = web.wpscan_scan(args.wpscan)
    
    elif args.dirb:
        web = KaliWebTesting()
        results['dirb'] = web.dirb_scan(args.dirb)
    
    # Атаки на пароли
    elif args.john:
        passwd = KaliPasswordAttacks()
        results['john'] = passwd.john_crack(args.john, args.john_wordlist)
    
    elif args.hashcat:
        passwd = KaliPasswordAttacks()
        results['hashcat'] = passwd.hashcat_crack(args.hashcat, args.hash_type, args.hashcat_wordlist)
    
    elif args.hydra:
        passwd = KaliPasswordAttacks()
        results['hydra'] = passwd.hydra_attack(args.hydra, args.hydra_service, args.hydra_user, args.hydra_wordlist)
    
    elif args.crunch:
        passwd = KaliPasswordAttacks()
        min_len, max_len, charset, output = args.crunch
        results['crunch'] = passwd.crunch_generate(int(min_len), int(max_len), charset, output)
    
    # Форензика
    elif args.volatility:
        forensics = KaliForensics()
        results['volatility'] = forensics.volatility_analyze(args.volatility, args.volatility_plugin)
    
    elif args.binwalk:
        forensics = KaliForensics()
        results['binwalk'] = forensics.binwalk_extract(args.binwalk)
    
    elif args.foremost:
        forensics = KaliForensics()
        image, output = args.foremost
        results['foremost'] = forensics.foremost_recover(image, output)
    
    elif args.exiftool:
        forensics = KaliForensics()
        results['exiftool'] = forensics.exiftool_analyze(args.exiftool)
    
    # Стеганография
    elif args.steghide:
        stego = KaliSteganography()
        results['steghide'] = stego.steghide_extract(args.steghide, args.steghide_pass)
    
    elif args.zsteg:
        stego = KaliSteganography()
        results['zsteg'] = stego.zsteg_analyze(args.zsteg)
    
    elif args.outguess:
        stego = KaliSteganography()
        image, output = args.outguess
        results['outguess'] = stego.outguess_extract(image, output)
    
    else:
        parser.print_help()
        sys.exit(0)
    
    if args.save and results:
        save_results(results, "kali_integration", "json")

if __name__ == "__main__":
    main()

