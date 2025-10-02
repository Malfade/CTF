#!/usr/bin/env python3
"""
Network Tools - Инструменты для сетевого анализа и атак
"""

import socket
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress
import subprocess
import struct
import time
import json
import xml.etree.ElementTree as ET
from typing import List, Tuple, Optional, Dict
from utils import *

class NetworkScanner:
    """Сканер сети и портов"""
    
    def __init__(self, timeout: float = 1.0, threads: int = 50):
        self.timeout = timeout
        self.threads = threads
        self.open_ports = []
    
    def scan_port(self, host: str, port: int) -> Tuple[int, bool, str]:
        """Сканирование одного порта"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                return (port, True, service)
            return (port, False, "")
        except Exception as e:
            return (port, False, "")
    
    def scan_ports(self, host: str, ports: List[int]):
        """Сканирование множества портов"""
        print_info(f"Сканирование {host} ({len(ports)} портов)...")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.scan_port, host, port): port for port in ports}
            
            for i, future in enumerate(as_completed(futures)):
                port, is_open, service = future.result()
                if is_open:
                    self.open_ports.append((port, service))
                    print_success(f"Порт {port} ОТКРЫТ - Сервис: {service}")
                progress_bar(i + 1, len(ports))
        
        print()
        return self.open_ports
    
    def scan_common_ports(self, host: str):
        """Сканирование популярных портов"""
        common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
            993, 995, 1723, 3306, 3389, 5900, 8080, 8443
        ]
        return self.scan_ports(host, common_ports)
    
    def scan_range(self, host: str, start_port: int, end_port: int):
        """Сканирование диапазона портов"""
        ports = list(range(start_port, end_port + 1))
        return self.scan_ports(host, ports)
    
    def ping_sweep(self, network: str):
        """Ping sweep для обнаружения живых хостов"""
        print_info(f"Поиск активных хостов в сети {network}...")
        active_hosts = []
        
        try:
            net = ipaddress.ip_network(network, strict=False)
            hosts = list(net.hosts())
            
            for i, host in enumerate(hosts):
                try:
                    response = subprocess.run(
                        ['ping', '-c', '1', '-W', '1', str(host)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=2
                    )
                    if response.returncode == 0:
                        active_hosts.append(str(host))
                        print_success(f"Хост {host} активен")
                    progress_bar(i + 1, len(hosts))
                except:
                    pass
            
            print()
            return active_hosts
        except Exception as e:
            print_error(f"Ошибка ping sweep: {e}")
            return []

class TCPPacketCrafter:
    """Создание и отправка пользовательских TCP пакетов"""
    
    def send_syn_flood(self, target_ip: str, target_port: int, count: int = 100):
        """SYN flood атака (только для тестирования!)"""
        print_warning("SYN Flood - используйте только в контролируемой среде!")
        
        try:
            for i in range(count):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                try:
                    sock.connect((target_ip, target_port))
                    sock.close()
                except:
                    pass
                progress_bar(i + 1, count)
            print()
            print_success(f"Отправлено {count} SYN пакетов")
        except Exception as e:
            print_error(f"Ошибка: {e}")

class BannerGrabber:
    """Захват баннеров сервисов"""
    
    def grab_banner(self, host: str, port: int, timeout: float = 2.0) -> Optional[str]:
        """Захват баннера сервиса"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Пробуем получить баннер
            try:
                sock.send(b'HEAD / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n')
            except:
                pass
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return banner
        except:
            return None
    
    def scan_banners(self, host: str, ports: List[int]):
        """Сканирование баннеров на множестве портов"""
        print_info(f"Захват баннеров с {host}...")
        results = []
        
        for port in ports:
            banner = self.grab_banner(host, port)
            if banner:
                results.append((port, banner))
                print_success(f"Порт {port}: {banner[:100]}...")
        
        return results

class NmapIntegration:
    """Интеграция с Nmap для продвинутого сканирования"""
    
    def __init__(self):
        self.nmap_available = self.check_nmap()
    
    def check_nmap(self) -> bool:
        """Проверка доступности nmap"""
        try:
            result = subprocess.run(['nmap', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print_success("Nmap найден и готов к использованию")
                return True
        except:
            pass
        print_warning("Nmap не найден - используйте базовое сканирование")
        return False
    
    def nmap_scan(self, target: str, scan_type: str = 'basic') -> Dict:
        """Выполнение nmap сканирования"""
        if not self.nmap_available:
            return {}
        
        print_info(f"Nmap сканирование {target}...")
        
        # Различные типы сканирования
        scan_options = {
            'basic': '-sS -O -sV --top-ports 1000',
            'aggressive': '-A -sS -sV -O --script vuln',
            'stealth': '-sS -T2 -f --top-ports 100',
            'udp': '-sU --top-ports 100',
            'vuln': '-sS -sV --script vuln',
            'full': '-sS -sV -O -A --script vuln,discovery'
        }
        
        options = scan_options.get(scan_type, scan_options['basic'])
        cmd = f"nmap {options} -oX - {target}"
        
        try:
            result = subprocess.run(cmd.split(), capture_output=True, 
                                  text=True, timeout=300)
            
            if result.returncode == 0:
                return self.parse_nmap_xml(result.stdout)
            else:
                print_error(f"Ошибка nmap: {result.stderr}")
                return {}
                
        except subprocess.TimeoutExpired:
            print_error("Nmap сканирование превысило время ожидания")
            return {}
        except Exception as e:
            print_error(f"Ошибка выполнения nmap: {e}")
            return {}
    
    def parse_nmap_xml(self, xml_output: str) -> Dict:
        """Парсинг XML вывода nmap"""
        try:
            root = ET.fromstring(xml_output)
            results = {
                'hosts': [],
                'ports': [],
                'os': [],
                'services': [],
                'vulnerabilities': []
            }
            
            for host in root.findall('host'):
                host_info = {
                    'ip': host.find('address').get('addr') if host.find('address') is not None else 'unknown',
                    'state': 'up',
                    'ports': []
                }
                
                # Порты
                for port in host.findall('.//port'):
                    port_info = {
                        'port': port.get('portid'),
                        'protocol': port.get('protocol'),
                        'state': port.find('state').get('state') if port.find('state') is not None else 'unknown',
                        'service': '',
                        'version': ''
                    }
                    
                    service = port.find('service')
                    if service is not None:
                        port_info['service'] = service.get('name', '')
                        port_info['version'] = service.get('version', '')
                    
                    host_info['ports'].append(port_info)
                    results['ports'].append(port_info)
                    
                    print_success(f"Порт {port_info['port']}: {port_info['service']} {port_info['version']}")
                
                # OS Detection
                os_info = host.find('.//osmatch')
                if os_info is not None:
                    os_name = os_info.get('name', 'Unknown')
                    host_info['os'] = os_name
                    results['os'].append(os_name)
                    print_success(f"ОС: {os_name}")
                
                results['hosts'].append(host_info)
            
            return results
            
        except Exception as e:
            print_error(f"Ошибка парсинга nmap XML: {e}")
            return {}
    
    def nmap_script_scan(self, target: str, script: str) -> Dict:
        """Выполнение nmap скриптов"""
        if not self.nmap_available:
            return {}
        
        print_info(f"Выполнение nmap скрипта {script} на {target}...")
        
        cmd = f"nmap --script {script} -oX - {target}"
        
        try:
            result = subprocess.run(cmd.split(), capture_output=True, 
                                  text=True, timeout=120)
            
            if result.returncode == 0:
                return self.parse_nmap_xml(result.stdout)
            else:
                print_error(f"Ошибка nmap скрипта: {result.stderr}")
                return {}
                
        except Exception as e:
            print_error(f"Ошибка выполнения nmap скрипта: {e}")
            return {}

class OSDetector:
    """Определение операционной системы"""
    
    def __init__(self):
        self.os_signatures = {
            'Linux': [22, 80, 443, 21, 25, 53, 110, 143, 993, 995],
            'Windows': [135, 139, 445, 3389, 5985, 5986],
            'FreeBSD': [22, 80, 443, 25, 53, 110, 143],
            'OpenBSD': [22, 80, 443, 25, 53],
            'macOS': [22, 80, 443, 548, 631]
        }
    
    def detect_os_by_ports(self, open_ports: List[int]) -> str:
        """Определение ОС по открытым портам"""
        print_info("Определение ОС по открытым портам...")
        
        scores = {}
        for os_name, typical_ports in self.os_signatures.items():
            score = len(set(open_ports) & set(typical_ports))
            scores[os_name] = score
        
        if scores:
            best_match = max(scores, key=scores.get)
            confidence = scores[best_match] / len(typical_ports) * 100
            print_success(f"Возможная ОС: {best_match} (уверенность: {confidence:.1f}%)")
            return best_match
        
        return "Unknown"

class VulnerabilityScanner:
    """Сканер уязвимостей"""
    
    def __init__(self):
        self.vuln_db = {
            'ssh': {
                'weak_ciphers': ['des', 'rc4', 'md5'],
                'weak_protocols': ['ssh1']
            },
            'http': {
                'weak_headers': ['Server', 'X-Powered-By'],
                'dangerous_methods': ['PUT', 'DELETE', 'TRACE']
            },
            'ftp': {
                'anonymous': True,
                'weak_auth': True
            }
        }
    
    def scan_service_vulnerabilities(self, host: str, port: int, service: str) -> List[Dict]:
        """Сканирование уязвимостей сервиса"""
        print_info(f"Сканирование уязвимостей {service} на {host}:{port}...")
        
        vulnerabilities = []
        
        if service == 'ssh':
            vulns = self.scan_ssh_vulnerabilities(host, port)
            vulnerabilities.extend(vulns)
        elif service == 'http' or service == 'https':
            vulns = self.scan_http_vulnerabilities(host, port)
            vulnerabilities.extend(vulns)
        elif service == 'ftp':
            vulns = self.scan_ftp_vulnerabilities(host, port)
            vulnerabilities.extend(vulns)
        
        return vulnerabilities
    
    def scan_ssh_vulnerabilities(self, host: str, port: int) -> List[Dict]:
        """Сканирование SSH уязвимостей"""
        vulns = []
        
        try:
            # Проверка на слабые шифры (упрощенная версия)
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Попытка подключения с различными методами
            try:
                client.connect(host, port=port, username='root', password='', timeout=5)
                vulns.append({
                    'type': 'SSH Weak Authentication',
                    'description': 'SSH позволяет подключение с пустым паролем',
                    'severity': 'High'
                })
            except:
                pass
            
            client.close()
            
        except Exception as e:
            print_warning(f"Не удалось проверить SSH уязвимости: {e}")
        
        return vulns
    
    def scan_http_vulnerabilities(self, host: str, port: int) -> List[Dict]:
        """Сканирование HTTP уязвимостей"""
        vulns = []
        
        try:
            import requests
            url = f"http://{host}:{port}"
            
            # Проверка опасных HTTP методов
            response = requests.options(url, timeout=5)
            allowed_methods = response.headers.get('Allow', '')
            
            dangerous_methods = ['PUT', 'DELETE', 'TRACE']
            for method in dangerous_methods:
                if method in allowed_methods:
                    vulns.append({
                        'type': 'HTTP Dangerous Method',
                        'description': f'Разрешен опасный метод: {method}',
                        'severity': 'Medium'
                    })
            
            # Проверка информационных заголовков
            response = requests.get(url, timeout=5)
            if 'Server' in response.headers:
                vulns.append({
                    'type': 'Information Disclosure',
                    'description': f'Раскрывается информация о сервере: {response.headers["Server"]}',
                    'severity': 'Low'
                })
            
        except Exception as e:
            print_warning(f"Не удалось проверить HTTP уязвимости: {e}")
        
        return vulns
    
    def scan_ftp_vulnerabilities(self, host: str, port: int) -> List[Dict]:
        """Сканирование FTP уязвимостей"""
        vulns = []
        
        try:
            import ftplib
            
            # Проверка анонимного доступа
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=5)
            ftp.login('anonymous', '')
            
            vulns.append({
                'type': 'FTP Anonymous Access',
                'description': 'FTP разрешает анонимный доступ',
                'severity': 'Medium'
            })
            
            ftp.quit()
            
        except:
            pass  # Анонимный доступ запрещен - это хорошо
        
        return vulns

def main():
    parser = argparse.ArgumentParser(
        description="Network Tools - CTF сетевые инструменты",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --scan-common 192.168.1.1
  %(prog)s --scan-range 192.168.1.1 1 1000
  %(prog)s --ping-sweep 192.168.1.0/24
  %(prog)s --banner-grab 192.168.1.1 --ports 80,443,22
  %(prog)s --nmap-scan 192.168.1.1 --nmap-type aggressive
  %(prog)s --nmap-script 192.168.1.1 vuln
  %(prog)s --os-detect 192.168.1.1
  %(prog)s --vuln-scan 192.168.1.1
        """
    )
    
    parser.add_argument('--scan-common', metavar='HOST', help='Сканирование популярных портов')
    parser.add_argument('--scan-range', metavar=('HOST', 'START', 'END'), nargs=3, 
                       help='Сканирование диапазона портов')
    parser.add_argument('--ping-sweep', metavar='NETWORK', help='Поиск активных хостов (192.168.1.0/24)')
    parser.add_argument('--banner-grab', metavar='HOST', help='Захват баннеров')
    parser.add_argument('--ports', metavar='PORTS', help='Список портов через запятую (80,443,22)')
    
    # Новые nmap интеграции
    parser.add_argument('--nmap-scan', metavar='TARGET', help='Nmap сканирование')
    parser.add_argument('--nmap-type', choices=['basic', 'aggressive', 'stealth', 'udp', 'vuln', 'full'],
                       default='basic', help='Тип nmap сканирования')
    parser.add_argument('--nmap-script', metavar=('TARGET', 'SCRIPT'), nargs=2,
                       help='Выполнение nmap скрипта')
    
    # OS Detection
    parser.add_argument('--os-detect', metavar='HOST', help='Определение ОС')
    
    # Vulnerability scanning
    parser.add_argument('--vuln-scan', metavar='HOST', help='Сканирование уязвимостей')
    parser.add_argument('--vuln-port', type=int, help='Порт для сканирования уязвимостей')
    parser.add_argument('--vuln-service', help='Сервис для сканирования уязвимостей')
    
    parser.add_argument('--threads', type=int, default=50, help='Количество потоков (по умолчанию: 50)')
    parser.add_argument('--timeout', type=float, default=1.0, help='Timeout в секундах (по умолчанию: 1.0)')
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    print_banner("NETWORK TOOLS")
    
    scanner = NetworkScanner(timeout=args.timeout, threads=args.threads)
    results = []
    
    if args.scan_common:
        results = scanner.scan_common_ports(args.scan_common)
        
    elif args.scan_range:
        host, start, end = args.scan_range
        results = scanner.scan_range(host, int(start), int(end))
        
    elif args.ping_sweep:
        results = scanner.ping_sweep(args.ping_sweep)
        
    elif args.banner_grab:
        if not args.ports:
            print_error("Укажите порты через --ports")
            sys.exit(1)
        
        ports = [int(p) for p in args.ports.split(',')]
        banner_grabber = BannerGrabber()
        results = banner_grabber.scan_banners(args.banner_grab, ports)
    
    # Новые nmap функции
    elif args.nmap_scan:
        nmap = NmapIntegration()
        results = nmap.nmap_scan(args.nmap_scan, args.nmap_type)
        
    elif args.nmap_script:
        target, script = args.nmap_script
        nmap = NmapIntegration()
        results = nmap.nmap_script_scan(target, script)
    
    # OS Detection
    elif args.os_detect:
        # Сначала сканируем порты
        open_ports = [port for port, service in scanner.scan_common_ports(args.os_detect)]
        os_detector = OSDetector()
        detected_os = os_detector.detect_os_by_ports(open_ports)
        results = {'os': detected_os, 'open_ports': open_ports}
    
    # Vulnerability scanning
    elif args.vuln_scan:
        vuln_scanner = VulnerabilityScanner()
        if args.vuln_port and args.vuln_service:
            results = vuln_scanner.scan_service_vulnerabilities(
                args.vuln_scan, args.vuln_port, args.vuln_service)
        else:
            # Сканируем все открытые порты
            open_ports = scanner.scan_common_ports(args.vuln_scan)
            all_vulns = []
            for port, service in open_ports:
                vulns = vuln_scanner.scan_service_vulnerabilities(args.vuln_scan, port, service)
                all_vulns.extend(vulns)
            results = all_vulns
    
    else:
        parser.print_help()
        sys.exit(0)
    
    # Вывод сводки
    print(f"\n{Colors.HEADER}{'=' * 50}{Colors.RESET}")
    print_success(f"Найдено результатов: {len(results)}")
    
    if args.save and results:
        save_results(results, "network_scan", "json")

if __name__ == "__main__":
    main()


