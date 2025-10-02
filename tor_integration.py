#!/usr/bin/env python3
"""
Tor Integration - Интеграция с Tor для анонимности
"""

import requests
import argparse
import sys
import subprocess
import time
from typing import Dict, Optional
from utils import *

class TorManager:
    """Управление Tor соединениями"""
    
    def __init__(self, tor_port: int = 9050, control_port: int = 9051):
        self.tor_port = tor_port
        self.control_port = control_port
        self.session = None
        self.tor_running = False
    
    def check_tor_running(self) -> bool:
        """Проверка запущен ли Tor"""
        try:
            # Проверяем доступность SOCKS порта
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            
            if result == 0:
                print_success("Tor запущен и доступен")
                self.tor_running = True
                return True
            else:
                print_warning("Tor не запущен")
                self.tor_running = False
                return False
                
        except Exception as e:
            print_error(f"Ошибка проверки Tor: {e}")
            return False
    
    def start_tor(self) -> bool:
        """Запуск Tor (если доступен)"""
        print_info("Попытка запуска Tor...")
        
        try:
            # Проверяем наличие tor в системе
            result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
            if result.returncode != 0:
                print_error("Tor не установлен в системе")
                print_info("Установите Tor: sudo apt install tor")
                return False
            
            # Запускаем Tor в фоне
            subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Ждем запуска
            for i in range(10):
                time.sleep(1)
                if self.check_tor_running():
                    return True
                print_info(f"Ожидание запуска Tor... {i+1}/10")
            
            print_error("Не удалось запустить Tor")
            return False
            
        except Exception as e:
            print_error(f"Ошибка запуска Tor: {e}")
            return False
    
    def create_tor_session(self) -> requests.Session:
        """Создание сессии с Tor прокси"""
        if not self.tor_running:
            if not self.start_tor():
                print_error("Не удалось запустить Tor")
                return None
        
        session = requests.Session()
        session.proxies = {
            'http': f'socks5://127.0.0.1:{self.tor_port}',
            'https': f'socks5://127.0.0.1:{self.tor_port}'
        }
        
        # Устанавливаем таймауты
        session.timeout = 30
        
        print_success("Tor сессия создана")
        return session
    
    def get_tor_ip(self) -> Optional[str]:
        """Получение текущего IP через Tor"""
        session = self.create_tor_session()
        if not session:
            return None
        
        try:
            print_info("Получение IP через Tor...")
            response = session.get('https://httpbin.org/ip', timeout=30)
            if response.status_code == 200:
                ip_data = response.json()
                tor_ip = ip_data.get('origin', 'Unknown')
                print_success(f"Tor IP: {tor_ip}")
                return tor_ip
            else:
                print_error(f"Ошибка получения IP: {response.status_code}")
                return None
                
        except Exception as e:
            print_error(f"Ошибка получения Tor IP: {e}")
            return None
    
    def renew_tor_identity(self) -> bool:
        """Обновление Tor identity (новый IP)"""
        print_info("Обновление Tor identity...")
        
        try:
            import socket
            
            # Подключаемся к Tor control порту
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', self.control_port))
            
            # Отправляем команду на обновление identity
            sock.send(b'AUTHENTICATE ""\r\n')
            response = sock.recv(1024)
            
            if b'250' in response:
                sock.send(b'SIGNAL NEWNYM\r\n')
                response = sock.recv(1024)
                
                if b'250' in response:
                    print_success("Tor identity обновлен")
                    sock.close()
                    time.sleep(5)  # Ждем обновления
                    return True
            
            sock.close()
            print_error("Не удалось обновить Tor identity")
            return False
            
        except Exception as e:
            print_error(f"Ошибка обновления Tor identity: {e}")
            return False

class TorWebScanner:
    """Веб-сканер через Tor"""
    
    def __init__(self):
        self.tor_manager = TorManager()
        self.session = None
    
    def setup_tor_session(self):
        """Настройка Tor сессии"""
        self.session = self.tor_manager.create_tor_session()
        if self.session:
            print_success("Tor веб-сканер готов")
        else:
            print_error("Не удалось настроить Tor сессию")
    
    def scan_url_through_tor(self, url: str) -> Dict:
        """Сканирование URL через Tor"""
        if not self.session:
            self.setup_tor_session()
        
        if not self.session:
            return {}
        
        print_info(f"Сканирование {url} через Tor...")
        
        try:
            response = self.session.get(url, timeout=30)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_length': len(response.content),
                'tor_ip': self.tor_manager.get_tor_ip()
            }
            
            print_success(f"Статус: {response.status_code}")
            print_success(f"Размер: {len(response.content)} bytes")
            print_success(f"Tor IP: {result['tor_ip']}")
            
            return result
            
        except Exception as e:
            print_error(f"Ошибка сканирования через Tor: {e}")
            return {}
    
    def test_tor_connectivity(self) -> bool:
        """Тестирование Tor соединения"""
        print_info("Тестирование Tor соединения...")
        
        if not self.session:
            self.setup_tor_session()
        
        if not self.session:
            return False
        
        try:
            # Тестируем доступность Tor
            response = self.session.get('https://check.torproject.org/', timeout=30)
            
            if response.status_code == 200:
                if 'Congratulations' in response.text:
                    print_success("Tor работает корректно!")
                    return True
                else:
                    print_warning("Tor может работать некорректно")
                    return False
            else:
                print_error(f"Ошибка тестирования Tor: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Ошибка тестирования Tor: {e}")
            return False

class OnionScanner:
    """Сканер .onion сайтов"""
    
    def __init__(self):
        self.tor_manager = TorManager()
        self.session = None
    
    def setup_tor_session(self):
        """Настройка Tor сессии для .onion"""
        self.session = self.tor_manager.create_tor_session()
        if self.session:
            print_success("Onion сканер готов")
        else:
            print_error("Не удалось настроить Tor сессию")
    
    def scan_onion_site(self, onion_url: str) -> Dict:
        """Сканирование .onion сайта"""
        if not self.session:
            self.setup_tor_session()
        
        if not self.session:
            return {}
        
        # Убеждаемся что URL содержит .onion
        if '.onion' not in onion_url:
            print_error("URL должен содержать .onion")
            return {}
        
        print_info(f"Сканирование .onion сайта: {onion_url}")
        
        try:
            response = self.session.get(onion_url, timeout=60)
            
            result = {
                'onion_url': onion_url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_length': len(response.content),
                'title': '',
                'links': []
            }
            
            # Извлекаем заголовок
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                result['title'] = title_tag.text.strip()
            
            # Извлекаем ссылки
            links = soup.find_all('a', href=True)
            result['links'] = [link['href'] for link in links[:10]]  # Первые 10 ссылок
            
            print_success(f"Статус: {response.status_code}")
            print_success(f"Заголовок: {result['title']}")
            print_success(f"Ссылок найдено: {len(result['links'])}")
            
            return result
            
        except Exception as e:
            print_error(f"Ошибка сканирования .onion: {e}")
            return {}
    
    def discover_onion_services(self, search_term: str = "") -> List[str]:
        """Поиск .onion сервисов (упрощенная версия)"""
        print_info("Поиск .onion сервисов...")
        
        # Список известных .onion сервисов (для демонстрации)
        known_onions = [
            "facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion",
            "duckduckgogg42tsccq3g4yqgce7imqwa46x5c7npaqltj2xcl5cduad.onion",
            "3g2upl4pq6kufc4m.onion",  # DuckDuckGo
            "protonirockerxow.onion",  # ProtonMail
        ]
        
        if search_term:
            # Фильтруем по поисковому термину
            filtered_onions = [onion for onion in known_onions if search_term.lower() in onion.lower()]
            return filtered_onions
        
        return known_onions

def main():
    parser = argparse.ArgumentParser(
        description="Tor Integration - Интеграция с Tor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --check-tor
  %(prog)s --start-tor
  %(prog)s --get-ip
  %(prog)s --renew-identity
  %(prog)s --test-connectivity
  %(prog)s --scan-url https://example.com
  %(prog)s --scan-onion facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion
  %(prog)s --discover-onions
        """
    )
    
    # Tor management
    parser.add_argument('--check-tor', action='store_true', help='Проверить статус Tor')
    parser.add_argument('--start-tor', action='store_true', help='Запустить Tor')
    parser.add_argument('--get-ip', action='store_true', help='Получить Tor IP')
    parser.add_argument('--renew-identity', action='store_true', help='Обновить Tor identity')
    parser.add_argument('--test-connectivity', action='store_true', help='Тестировать Tor соединение')
    
    # Web scanning through Tor
    parser.add_argument('--scan-url', metavar='URL', help='Сканировать URL через Tor')
    
    # Onion services
    parser.add_argument('--scan-onion', metavar='ONION_URL', help='Сканировать .onion сайт')
    parser.add_argument('--discover-onions', action='store_true', help='Найти .onion сервисы')
    
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    print_banner("TOR INTEGRATION")
    
    results = {}
    
    if args.check_tor:
        tor_manager = TorManager()
        results['tor_status'] = tor_manager.check_tor_running()
    
    elif args.start_tor:
        tor_manager = TorManager()
        results['tor_started'] = tor_manager.start_tor()
    
    elif args.get_ip:
        tor_manager = TorManager()
        results['tor_ip'] = tor_manager.get_tor_ip()
    
    elif args.renew_identity:
        tor_manager = TorManager()
        results['identity_renewed'] = tor_manager.renew_tor_identity()
    
    elif args.test_connectivity:
        scanner = TorWebScanner()
        results['connectivity_test'] = scanner.test_tor_connectivity()
    
    elif args.scan_url:
        scanner = TorWebScanner()
        results['url_scan'] = scanner.scan_url_through_tor(args.scan_url)
    
    elif args.scan_onion:
        onion_scanner = OnionScanner()
        results['onion_scan'] = onion_scanner.scan_onion_site(args.scan_onion)
    
    elif args.discover_onions:
        onion_scanner = OnionScanner()
        results['onion_services'] = onion_scanner.discover_onion_services()
    
    else:
        parser.print_help()
        sys.exit(0)
    
    if args.save and results:
        save_results(results, "tor_integration", "json")

if __name__ == "__main__":
    main()





