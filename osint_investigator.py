#!/usr/bin/env python3
"""
OSINT Investigator - Поиск информации о человеке через Tor (только для CTF)
"""

import argparse
import sys
import json
import time
import random
import requests
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from utils import *

try:
    from stem import Signal
    from stem.control import Controller
    TOR_AVAILABLE = True
except ImportError:
    TOR_AVAILABLE = False
    print_warning("stem не установлен - Tor функции недоступны")

class TorOSINTInvestigator:
    """OSINT исследователь через Tor"""
    
    def __init__(self):
        self.session = requests.Session()
        self.tor_proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        self.results = {
            'target': '',
            'timestamp': '',
            'social_media': [],
            'email_info': [],
            'phone_info': [],
            'username_matches': [],
            'domain_info': [],
            'leaked_data': [],
            'public_records': []
        }
    
    def renew_tor_identity(self):
        """Обновление Tor идентичности"""
        if not TOR_AVAILABLE:
            print_warning("Tor недоступен - используем обычное соединение")
            return False
        
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                print_success("Tor идентичность обновлена")
                time.sleep(5)  # Ждем обновления
                return True
        except Exception as e:
            print_warning(f"Не удалось обновить Tor идентичность: {e}")
            return False
    
    def search_social_media(self, username: str, email: str = None) -> List[Dict]:
        """Поиск в социальных сетях"""
        print_info(f"Поиск в социальных сетях для: {username}")
        
        social_platforms = [
            {
                'name': 'Facebook',
                'url': f'https://www.facebook.com/{username}',
                'search_url': f'https://www.facebook.com/search/people/?q={username}'
            },
            {
                'name': 'Twitter',
                'url': f'https://twitter.com/{username}',
                'search_url': f'https://twitter.com/search?q={username}'
            },
            {
                'name': 'Instagram',
                'url': f'https://www.instagram.com/{username}',
                'search_url': f'https://www.instagram.com/explore/tags/{username}/'
            },
            {
                'name': 'LinkedIn',
                'url': f'https://www.linkedin.com/in/{username}',
                'search_url': f'https://www.linkedin.com/search/results/people/?keywords={username}'
            },
            {
                'name': 'GitHub',
                'url': f'https://github.com/{username}',
                'search_url': f'https://github.com/search?q={username}'
            },
            {
                'name': 'Reddit',
                'url': f'https://www.reddit.com/user/{username}',
                'search_url': f'https://www.reddit.com/search/?q={username}'
            }
        ]
        
        found_profiles = []
        
        for platform in social_platforms:
            try:
                # Проверяем прямой профиль
                response = self.session.get(
                    platform['url'], 
                    proxies=self.tor_proxies,
                    timeout=10,
                    headers={'User-Agent': self._get_random_user_agent()}
                )
                
                if response.status_code == 200:
                    profile_info = {
                        'platform': platform['name'],
                        'url': platform['url'],
                        'status': 'found',
                        'title': self._extract_title(response.text),
                        'description': self._extract_description(response.text)
                    }
                    found_profiles.append(profile_info)
                    print_success(f"Найден профиль на {platform['name']}: {platform['url']}")
                
                # Небольшая задержка между запросами
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print_warning(f"Ошибка поиска на {platform['name']}: {e}")
        
        return found_profiles
    
    def search_email_breaches(self, email: str) -> List[Dict]:
        """Поиск утечек данных по email"""
        print_info(f"Поиск утечек данных для email: {email}")
        
        # Симуляция поиска в базах утечек (для CTF)
        breach_sources = [
            'Have I Been Pwned',
            'DeHashed',
            'LeakCheck',
            'BreachAlarm',
            'Intel471'
        ]
        
        # Генерируем реалистичные результаты для CTF
        breaches = []
        if random.random() > 0.3:  # 70% шанс найти утечки
            num_breaches = random.randint(1, 5)
            for i in range(num_breaches):
                breach = {
                    'source': random.choice(breach_sources),
                    'date': f"202{random.randint(0, 4)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    'data_types': random.sample(['email', 'password', 'phone', 'address', 'name'], random.randint(1, 3)),
                    'severity': random.choice(['low', 'medium', 'high']),
                    'description': f"Data breach involving {random.randint(1000, 10000000)} records"
                }
                breaches.append(breach)
                print_warning(f"Найдена утечка: {breach['source']} ({breach['date']})")
        
        return breaches
    
    def search_phone_info(self, phone: str) -> List[Dict]:
        """Поиск информации по номеру телефона"""
        print_info(f"Поиск информации по номеру: {phone}")
        
        # Симуляция поиска по номеру телефона
        phone_info = []
        
        # Проверяем различные источники
        sources = [
            'TrueCaller',
            'SpyDialer',
            'WhitePages',
            'Pipl',
            'Social Media'
        ]
        
        for source in sources:
            if random.random() > 0.4:  # 60% шанс найти информацию
                info = {
                    'source': source,
                    'carrier': random.choice(['Verizon', 'AT&T', 'T-Mobile', 'Sprint', 'Unknown']),
                    'location': f"{random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])}",
                    'type': random.choice(['mobile', 'landline', 'voip']),
                    'confidence': random.randint(60, 95)
                }
                phone_info.append(info)
                print_success(f"Найдена информация в {source}: {info['carrier']}")
        
        return phone_info
    
    def search_username_across_platforms(self, username: str) -> List[Dict]:
        """Поиск username на различных платформах"""
        print_info(f"Поиск username '{username}' на различных платформах")
        
        platforms = [
            'Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'GitHub',
            'Reddit', 'YouTube', 'TikTok', 'Snapchat', 'Discord',
            'Steam', 'Twitch', 'Pinterest', 'Tumblr', 'Flickr'
        ]
        
        matches = []
        
        for platform in platforms:
            if random.random() > 0.6:  # 40% шанс найти совпадение
                match = {
                    'platform': platform,
                    'username': username,
                    'url': f"https://{platform.lower()}.com/{username}",
                    'status': 'active' if random.random() > 0.2 else 'inactive',
                    'last_seen': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    'followers': random.randint(0, 10000) if random.random() > 0.5 else 0
                }
                matches.append(match)
                print_success(f"Найден {username} на {platform}")
        
        return matches
    
    def search_domain_info(self, domain: str) -> List[Dict]:
        """Поиск информации о домене"""
        print_info(f"Поиск информации о домене: {domain}")
        
        domain_info = []
        
        # WHOIS информация
        whois_data = {
            'registrar': random.choice(['GoDaddy', 'Namecheap', 'Google Domains', 'Cloudflare']),
            'creation_date': f"202{random.randint(0, 4)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'expiration_date': f"202{random.randint(5, 9)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'nameservers': [f"ns1.{domain}", f"ns2.{domain}"],
            'status': 'active'
        }
        domain_info.append({'type': 'whois', 'data': whois_data})
        
        # DNS записи
        dns_records = {
            'A': [f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"],
            'MX': [f"mail.{domain}"],
            'NS': [f"ns1.{domain}", f"ns2.{domain}"]
        }
        domain_info.append({'type': 'dns', 'data': dns_records})
        
        print_success(f"Найдена информация о домене {domain}")
        return domain_info
    
    def search_public_records(self, name: str, location: str = None) -> List[Dict]:
        """Поиск в публичных записях"""
        print_info(f"Поиск публичных записей для: {name}")
        
        records = []
        
        # Симуляция поиска в публичных базах
        record_types = [
            'Property Records',
            'Court Records',
            'Business Records',
            'Professional Licenses',
            'Voter Registration'
        ]
        
        for record_type in record_types:
            if random.random() > 0.5:  # 50% шанс найти запись
                record = {
                    'type': record_type,
                    'name': name,
                    'location': location or random.choice(['New York', 'California', 'Texas', 'Florida']),
                    'date': f"202{random.randint(0, 4)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    'details': f"Public record found in {record_type.lower()}"
                }
                records.append(record)
                print_success(f"Найдена запись: {record_type}")
        
        return records
    
    def comprehensive_investigation(self, target_data: Dict) -> Dict:
        """Комплексное расследование"""
        print_warning("🔍 НАЧИНАЕМ OSINT РАССЛЕДОВАНИЕ ЧЕРЕЗ TOR")
        print_warning("⚠️  ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
        
        self.results['target'] = target_data
        self.results['timestamp'] = datetime.now().isoformat()
        
        # Обновляем Tor идентичность
        self.renew_tor_identity()
        
        # Поиск в социальных сетях
        if 'username' in target_data:
            self.results['social_media'] = self.search_social_media(
                target_data['username'], 
                target_data.get('email')
            )
        
        # Поиск утечек по email
        if 'email' in target_data:
            self.results['leaked_data'] = self.search_email_breaches(target_data['email'])
        
        # Поиск информации по телефону
        if 'phone' in target_data:
            self.results['phone_info'] = self.search_phone_info(target_data['phone'])
        
        # Поиск username на платформах
        if 'username' in target_data:
            self.results['username_matches'] = self.search_username_across_platforms(target_data['username'])
        
        # Поиск информации о домене
        if 'domain' in target_data:
            self.results['domain_info'] = self.search_domain_info(target_data['domain'])
        
        # Поиск публичных записей
        if 'name' in target_data:
            self.results['public_records'] = self.search_public_records(
                target_data['name'], 
                target_data.get('location')
            )
        
        print_success("🎯 OSINT расследование завершено")
        return self.results
    
    def _get_random_user_agent(self) -> str:
        """Получение случайного User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        return random.choice(user_agents)
    
    def _extract_title(self, html: str) -> str:
        """Извлечение заголовка страницы"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()
        return "No title found"
    
    def _extract_description(self, html: str) -> str:
        """Извлечение описания страницы"""
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        if desc_match:
            return desc_match.group(1).strip()
        return "No description found"

class OSINTReportGenerator:
    """Генератор отчетов OSINT"""
    
    def __init__(self):
        pass
    
    def generate_html_report(self, results: Dict, output_file: str = None) -> str:
        """Генерация HTML отчета"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"osint_report_{timestamp}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OSINT Investigation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .section {{ margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .section h3 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
        .item {{ margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 3px; }}
        .found {{ color: #27ae60; font-weight: bold; }}
        .warning {{ color: #e74c3c; font-weight: bold; }}
        .info {{ color: #3498db; }}
        .timestamp {{ color: #7f8c8d; font-size: 12px; }}
        .ctf-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 4px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 OSINT Investigation Report</h1>
            <p class="timestamp">Generated: {results.get('timestamp', 'Unknown')}</p>
        </div>
        
        <div class="ctf-notice">
            <strong>⚠️ CTF DEMO REPORT</strong><br>
            This report is generated for educational purposes only. All data is simulated for CTF scenarios.
        </div>
        
        <div class="section">
            <h3>🎯 Target Information</h3>
            <div class="item">
                <strong>Target:</strong> {results.get('target', {})}<br>
                <strong>Investigation Date:</strong> {results.get('timestamp', 'Unknown')}
            </div>
        </div>
        
        <div class="section">
            <h3>📱 Social Media Profiles</h3>
            {self._format_social_media(results.get('social_media', []))}
        </div>
        
        <div class="section">
            <h3>📧 Email Information</h3>
            {self._format_email_info(results.get('email_info', []))}
        </div>
        
        <div class="section">
            <h3>📞 Phone Information</h3>
            {self._format_phone_info(results.get('phone_info', []))}
        </div>
        
        <div class="section">
            <h3>👤 Username Matches</h3>
            {self._format_username_matches(results.get('username_matches', []))}
        </div>
        
        <div class="section">
            <h3>🌐 Domain Information</h3>
            {self._format_domain_info(results.get('domain_info', []))}
        </div>
        
        <div class="section">
            <h3>🔓 Data Breaches</h3>
            {self._format_breaches(results.get('leaked_data', []))}
        </div>
        
        <div class="section">
            <h3>📋 Public Records</h3>
            {self._format_public_records(results.get('public_records', []))}
        </div>
        
        <div class="ctf-notice">
            <strong>⚠️ IMPORTANT:</strong> This is a CTF demonstration tool. Use only for educational purposes and legal investigations.
        </div>
    </div>
</body>
</html>
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print_success(f"HTML отчет сохранен: {output_file}")
            return output_file
        except Exception as e:
            print_error(f"Ошибка сохранения отчета: {e}")
            return None
    
    def _format_social_media(self, profiles: List[Dict]) -> str:
        """Форматирование социальных сетей"""
        if not profiles:
            return "<div class='item info'>Профили в социальных сетях не найдены</div>"
        
        html = ""
        for profile in profiles:
            html += f"""
            <div class="item found">
                <strong>{profile['platform']}:</strong> 
                <a href="{profile['url']}" target="_blank">{profile['url']}</a><br>
                <strong>Title:</strong> {profile.get('title', 'N/A')}<br>
                <strong>Description:</strong> {profile.get('description', 'N/A')}
            </div>
            """
        return html
    
    def _format_email_info(self, email_info: List[Dict]) -> str:
        """Форматирование информации об email"""
        if not email_info:
            return "<div class='item info'>Информация об email не найдена</div>"
        
        html = ""
        for info in email_info:
            html += f"<div class='item'><strong>{info.get('type', 'Unknown')}:</strong> {info.get('data', 'N/A')}</div>"
        return html
    
    def _format_phone_info(self, phone_info: List[Dict]) -> str:
        """Форматирование информации о телефоне"""
        if not phone_info:
            return "<div class='item info'>Информация о телефоне не найдена</div>"
        
        html = ""
        for info in phone_info:
            html += f"""
            <div class="item">
                <strong>Source:</strong> {info['source']}<br>
                <strong>Carrier:</strong> {info['carrier']}<br>
                <strong>Location:</strong> {info['location']}<br>
                <strong>Type:</strong> {info['type']}<br>
                <strong>Confidence:</strong> {info['confidence']}%
            </div>
            """
        return html
    
    def _format_username_matches(self, matches: List[Dict]) -> str:
        """Форматирование совпадений username"""
        if not matches:
            return "<div class='item info'>Совпадения username не найдены</div>"
        
        html = ""
        for match in matches:
            status_class = "found" if match['status'] == 'active' else "warning"
            html += f"""
            <div class="item {status_class}">
                <strong>{match['platform']}:</strong> 
                <a href="{match['url']}" target="_blank">{match['username']}</a><br>
                <strong>Status:</strong> {match['status']}<br>
                <strong>Last Seen:</strong> {match['last_seen']}<br>
                <strong>Followers:</strong> {match['followers']}
            </div>
            """
        return html
    
    def _format_domain_info(self, domain_info: List[Dict]) -> str:
        """Форматирование информации о домене"""
        if not domain_info:
            return "<div class='item info'>Информация о домене не найдена</div>"
        
        html = ""
        for info in domain_info:
            html += f"<div class='item'><strong>{info['type'].upper()}:</strong> {info['data']}</div>"
        return html
    
    def _format_breaches(self, breaches: List[Dict]) -> str:
        """Форматирование утечек данных"""
        if not breaches:
            return "<div class='item info'>Утечки данных не найдены</div>"
        
        html = ""
        for breach in breaches:
            severity_class = "warning" if breach['severity'] == 'high' else "info"
            html += f"""
            <div class="item {severity_class}">
                <strong>Source:</strong> {breach['source']}<br>
                <strong>Date:</strong> {breach['date']}<br>
                <strong>Severity:</strong> {breach['severity']}<br>
                <strong>Data Types:</strong> {', '.join(breach['data_types'])}<br>
                <strong>Description:</strong> {breach['description']}
            </div>
            """
        return html
    
    def _format_public_records(self, records: List[Dict]) -> str:
        """Форматирование публичных записей"""
        if not records:
            return "<div class='item info'>Публичные записи не найдены</div>"
        
        html = ""
        for record in records:
            html += f"""
            <div class="item">
                <strong>Type:</strong> {record['type']}<br>
                <strong>Name:</strong> {record['name']}<br>
                <strong>Location:</strong> {record['location']}<br>
                <strong>Date:</strong> {record['date']}<br>
                <strong>Details:</strong> {record['details']}
            </div>
            """
        return html

def main():
    parser = argparse.ArgumentParser(description='OSINT Investigator - ТОЛЬКО ДЛЯ CTF!')
    parser.add_argument('--username', help='Username для поиска')
    parser.add_argument('--email', help='Email для поиска')
    parser.add_argument('--phone', help='Номер телефона для поиска')
    parser.add_argument('--name', help='Полное имя для поиска')
    parser.add_argument('--domain', help='Домен для анализа')
    parser.add_argument('--location', help='Местоположение')
    parser.add_argument('--output', help='Файл для сохранения отчета')
    parser.add_argument('--html-report', action='store_true', help='Создать HTML отчет')
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    # Предупреждение
    print_warning("⚠️  OSINT ИССЛЕДОВАНИЕ - ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
    print_warning("⚠️  НЕ ИСПОЛЬЗУЙТЕ ДЛЯ НЕЗАКОННЫХ ЦЕЛЕЙ!")
    print()
    
    # Проверяем наличие данных для поиска
    target_data = {}
    if args.username:
        target_data['username'] = args.username
    if args.email:
        target_data['email'] = args.email
    if args.phone:
        target_data['phone'] = args.phone
    if args.name:
        target_data['name'] = args.name
    if args.domain:
        target_data['domain'] = args.domain
    if args.location:
        target_data['location'] = args.location
    
    if not target_data:
        print_error("Необходимо указать хотя бы один параметр для поиска")
        print_info("Примеры:")
        print_info("  --username john_doe")
        print_info("  --email john@example.com")
        print_info("  --phone +1234567890")
        print_info("  --name 'John Doe'")
        return
    
    # Запускаем расследование
    investigator = TorOSINTInvestigator()
    results = investigator.comprehensive_investigation(target_data)
    
    # Выводим результаты
    print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    print_success("🎯 OSINT РАССЛЕДОВАНИЕ ЗАВЕРШЕНО")
    
    # Статистика
    total_findings = (
        len(results.get('social_media', [])) +
        len(results.get('leaked_data', [])) +
        len(results.get('phone_info', [])) +
        len(results.get('username_matches', [])) +
        len(results.get('domain_info', [])) +
        len(results.get('public_records', []))
    )
    
    print_info(f"Всего найдено: {total_findings} записей")
    print_info(f"Социальные сети: {len(results.get('social_media', []))}")
    print_info(f"Утечки данных: {len(results.get('leaked_data', []))}")
    print_info(f"Информация о телефоне: {len(results.get('phone_info', []))}")
    print_info(f"Совпадения username: {len(results.get('username_matches', []))}")
    print_info(f"Информация о домене: {len(results.get('domain_info', []))}")
    print_info(f"Публичные записи: {len(results.get('public_records', []))}")
    
    # Создаем HTML отчет
    if args.html_report:
        report_generator = OSINTReportGenerator()
        html_file = report_generator.generate_html_report(results, args.output)
        if html_file:
            print_success(f"HTML отчет создан: {html_file}")
    
    # Сохраняем результаты
    if args.save:
        save_results(results, "osint_investigation", "json")
    
    print_warning("\n⚠️  ПОМНИТЕ: Используйте только для легальных CTF и образования!")

if __name__ == "__main__":
    main()

