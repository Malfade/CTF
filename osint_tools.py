#!/usr/bin/env python3
"""
OSINT Tools - Инструменты для разведки и сбора информации
"""

import requests
import argparse
import sys
import json
import socket
from urllib.parse import urlparse
from typing import List, Dict, Optional
from utils import *

# Опциональные импорты
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    print_warning("dnspython не установлен - DNS функции недоступны")

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False
    print_warning("python-whois не установлен - WHOIS функции недоступны")

class DomainAnalyzer:
    """Анализ доменов и DNS"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def whois_lookup(self, domain: str) -> Dict:
        """WHOIS запрос для домена"""
        if not WHOIS_AVAILABLE:
            print_error("WHOIS функции недоступны - установите python-whois")
            return {}
        
        print_info(f"WHOIS запрос для {domain}...")
        
        try:
            domain_info = whois.whois(domain)
            
            result = {
                'domain': domain,
                'registrar': getattr(domain_info, 'registrar', 'Unknown'),
                'creation_date': str(getattr(domain_info, 'creation_date', 'Unknown')),
                'expiration_date': str(getattr(domain_info, 'expiration_date', 'Unknown')),
                'name_servers': getattr(domain_info, 'name_servers', []),
                'emails': getattr(domain_info, 'emails', []),
                'org': getattr(domain_info, 'org', 'Unknown')
            }
            
            print_success(f"Регистратор: {result['registrar']}")
            print_success(f"Создан: {result['creation_date']}")
            print_success(f"Истекает: {result['expiration_date']}")
            print_success(f"Организация: {result['org']}")
            
            return result
            
        except Exception as e:
            print_error(f"Ошибка WHOIS: {e}")
            return {}
    
    def dns_lookup(self, domain: str) -> Dict:
        """DNS запросы для домена"""
        if not DNS_AVAILABLE:
            print_error("DNS функции недоступны - установите dnspython")
            return {}
        
        print_info(f"DNS запросы для {domain}...")
        
        result = {
            'domain': domain,
            'a_records': [],
            'aaaa_records': [],
            'mx_records': [],
            'ns_records': [],
            'txt_records': [],
            'cname_records': []
        }
        
        record_types = {
            'A': 'a_records',
            'AAAA': 'aaaa_records', 
            'MX': 'mx_records',
            'NS': 'ns_records',
            'TXT': 'txt_records',
            'CNAME': 'cname_records'
        }
        
        for record_type, key in record_types.items():
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records = [str(answer) for answer in answers]
                result[key] = records
                
                if records:
                    print_success(f"{record_type}: {', '.join(records)}")
                    
            except Exception as e:
                print_warning(f"Нет {record_type} записей: {e}")
        
        return result
    
    def subdomain_enumeration(self, domain: str) -> List[str]:
        """Перечисление поддоменов"""
        print_info(f"Поиск поддоменов для {domain}...")
        
        # Список популярных поддоменов
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging',
            'api', 'app', 'blog', 'shop', 'store', 'support', 'help',
            'docs', 'wiki', 'forum', 'chat', 'login', 'portal',
            'secure', 'ssl', 'vpn', 'remote', 'backup', 'db',
            'mysql', 'postgres', 'redis', 'mongodb', 'elasticsearch',
            'jenkins', 'git', 'svn', 'ci', 'cd', 'monitor',
            'stats', 'analytics', 'metrics', 'logs', 'status'
        ]
        
        found_subdomains = []
        
        for subdomain in common_subdomains:
            full_domain = f"{subdomain}.{domain}"
            try:
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
                print_success(f"Найден поддомен: {full_domain}")
            except:
                pass
        
        return found_subdomains
    
    def reverse_dns_lookup(self, ip: str) -> List[str]:
        """Обратный DNS запрос"""
        print_info(f"Обратный DNS для {ip}...")
        
        try:
            hostnames = socket.gethostbyaddr(ip)
            print_success(f"Имя хоста: {hostnames[0]}")
            return hostnames
        except Exception as e:
            print_warning(f"Обратный DNS не найден: {e}")
            return []

class ShodanIntegration:
    """Интеграция с Shodan"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.available = self.check_shodan()
    
    def check_shodan(self) -> bool:
        """Проверка доступности Shodan API"""
        if not self.api_key:
            print_warning("Shodan API ключ не указан - используйте переменную SHODAN_API_KEY")
            return False
        
        try:
            import shodan
            api = shodan.Shodan(self.api_key)
            api.info()
            print_success("Shodan API доступен")
            return True
        except Exception as e:
            print_warning(f"Shodan API недоступен: {e}")
            return False
    
    def search_host(self, ip: str) -> Dict:
        """Поиск информации о хосте в Shodan"""
        if not self.available:
            return {}
        
        print_info(f"Поиск {ip} в Shodan...")
        
        try:
            import shodan
            api = shodan.Shodan(self.api_key)
            host = api.host(ip)
            
            result = {
                'ip': ip,
                'org': host.get('org', 'Unknown'),
                'os': host.get('os', 'Unknown'),
                'ports': [service['port'] for service in host.get('data', [])],
                'services': []
            }
            
            for service in host.get('data', []):
                service_info = {
                    'port': service.get('port'),
                    'product': service.get('product', ''),
                    'version': service.get('version', ''),
                    'banner': service.get('data', '')[:200]
                }
                result['services'].append(service_info)
                print_success(f"Порт {service_info['port']}: {service_info['product']} {service_info['version']}")
            
            return result
            
        except Exception as e:
            print_error(f"Ошибка Shodan: {e}")
            return {}
    
    def search_domain(self, domain: str) -> Dict:
        """Поиск информации о домене в Shodan"""
        if not self.available:
            return {}
        
        print_info(f"Поиск {domain} в Shodan...")
        
        try:
            import shodan
            api = shodan.Shodan(self.api_key)
            results = api.search(f"hostname:{domain}")
            
            result = {
                'domain': domain,
                'total_results': results['total'],
                'hosts': []
            }
            
            for match in results['matches'][:10]:  # Первые 10 результатов
                host_info = {
                    'ip': match['ip_str'],
                    'port': match['port'],
                    'product': match.get('product', ''),
                    'version': match.get('version', '')
                }
                result['hosts'].append(host_info)
                print_success(f"{host_info['ip']}:{host_info['port']} - {host_info['product']}")
            
            return result
            
        except Exception as e:
            print_error(f"Ошибка Shodan: {e}")
            return {}

class SocialMediaOSINT:
    """OSINT в социальных сетях"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_username(self, username: str) -> Dict:
        """Поиск пользователя по имени"""
        print_info(f"Поиск пользователя {username}...")
        
        # Список популярных платформ
        platforms = {
            'GitHub': f"https://github.com/{username}",
            'Twitter': f"https://twitter.com/{username}",
            'Instagram': f"https://instagram.com/{username}",
            'LinkedIn': f"https://linkedin.com/in/{username}",
            'Facebook': f"https://facebook.com/{username}",
            'Reddit': f"https://reddit.com/user/{username}",
            'YouTube': f"https://youtube.com/@{username}",
            'TikTok': f"https://tiktok.com/@{username}"
        }
        
        found_profiles = []
        
        for platform, url in platforms.items():
            try:
                response = self.session.get(url, timeout=5, allow_redirects=False)
                if response.status_code == 200:
                    found_profiles.append({
                        'platform': platform,
                        'url': url,
                        'status': 'Found'
                    })
                    print_success(f"{platform}: {url}")
                elif response.status_code == 404:
                    print_info(f"{platform}: Не найден")
                else:
                    print_warning(f"{platform}: Статус {response.status_code}")
            except Exception as e:
                print_warning(f"{platform}: Ошибка - {e}")
        
        return {
            'username': username,
            'profiles': found_profiles
        }
    
    def search_email(self, email: str) -> Dict:
        """Поиск информации по email"""
        print_info(f"Поиск информации по email {email}...")
        
        # Проверка на утечки данных (упрощенная версия)
        breach_indicators = [
            'haveibeenpwned.com',
            'dehashed.com',
            'leakix.net'
        ]
        
        result = {
            'email': email,
            'breach_check': 'Manual check recommended',
            'suggestions': [
                f"Проверьте {email} на haveibeenpwned.com",
                f"Поищите в Google: \"{email}\"",
                f"Проверьте социальные сети с этим email"
            ]
        }
        
        print_info("Рекомендации:")
        for suggestion in result['suggestions']:
            print(f"  - {suggestion}")
        
        return result

class MetadataExtractor:
    """Извлечение метаданных из файлов"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx', '.xls', '.xlsx']
    
    def extract_file_metadata(self, filepath: str) -> Dict:
        """Извлечение метаданных из файла"""
        print_info(f"Извлечение метаданных из {filepath}...")
        
        result = {
            'file': filepath,
            'exif_data': {},
            'pdf_info': {},
            'office_info': {}
        }
        
        file_ext = filepath.lower().split('.')[-1]
        
        if file_ext in ['jpg', 'jpeg', 'png']:
            result['exif_data'] = self.extract_image_metadata(filepath)
        elif file_ext == 'pdf':
            result['pdf_info'] = self.extract_pdf_metadata(filepath)
        elif file_ext in ['doc', 'docx', 'xls', 'xlsx']:
            result['office_info'] = self.extract_office_metadata(filepath)
        
        return result
    
    def extract_image_metadata(self, filepath: str) -> Dict:
        """Извлечение EXIF данных из изображений"""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            image = Image.open(filepath)
            exif_data = {}
            
            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_data[tag] = value
                        
                        if tag in ['Make', 'Model', 'DateTime', 'GPSInfo']:
                            print_success(f"{tag}: {value}")
            
            return exif_data
            
        except Exception as e:
            print_error(f"Ошибка извлечения EXIF: {e}")
            return {}
    
    def extract_pdf_metadata(self, filepath: str) -> Dict:
        """Извлечение метаданных из PDF"""
        try:
            import PyPDF2
            
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                if metadata:
                    result = {
                        'title': metadata.get('/Title', ''),
                        'author': metadata.get('/Author', ''),
                        'subject': metadata.get('/Subject', ''),
                        'creator': metadata.get('/Creator', ''),
                        'producer': metadata.get('/Producer', ''),
                        'creation_date': metadata.get('/CreationDate', ''),
                        'modification_date': metadata.get('/ModDate', '')
                    }
                    
                    for key, value in result.items():
                        if value:
                            print_success(f"{key}: {value}")
                    
                    return result
            
            return {}
            
        except Exception as e:
            print_error(f"Ошибка извлечения PDF метаданных: {e}")
            return {}

def main():
    parser = argparse.ArgumentParser(
        description="OSINT Tools - Инструменты разведки",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --whois example.com
  %(prog)s --dns example.com
  %(prog)s --subdomains example.com
  %(prog)s --reverse-dns 8.8.8.8
  %(prog)s --shodan-host 8.8.8.8
  %(prog)s --username john_doe
  %(prog)s --email user@example.com
  %(prog)s --metadata file.jpg
        """
    )
    
    # Domain analysis
    parser.add_argument('--whois', metavar='DOMAIN', help='WHOIS запрос')
    parser.add_argument('--dns', metavar='DOMAIN', help='DNS запросы')
    parser.add_argument('--subdomains', metavar='DOMAIN', help='Поиск поддоменов')
    parser.add_argument('--reverse-dns', metavar='IP', help='Обратный DNS')
    
    # Shodan integration
    parser.add_argument('--shodan-host', metavar='IP', help='Поиск хоста в Shodan')
    parser.add_argument('--shodan-domain', metavar='DOMAIN', help='Поиск домена в Shodan')
    parser.add_argument('--shodan-key', help='Shodan API ключ')
    
    # Social media
    parser.add_argument('--username', metavar='USERNAME', help='Поиск пользователя')
    parser.add_argument('--email', metavar='EMAIL', help='Поиск по email')
    
    # Metadata
    parser.add_argument('--metadata', metavar='FILE', help='Извлечение метаданных')
    
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    print_banner("OSINT TOOLS")
    
    results = {}
    
    if args.whois:
        analyzer = DomainAnalyzer()
        results['whois'] = analyzer.whois_lookup(args.whois)
    
    elif args.dns:
        analyzer = DomainAnalyzer()
        results['dns'] = analyzer.dns_lookup(args.dns)
    
    elif args.subdomains:
        analyzer = DomainAnalyzer()
        results['subdomains'] = analyzer.subdomain_enumeration(args.subdomains)
    
    elif args.reverse_dns:
        analyzer = DomainAnalyzer()
        results['reverse_dns'] = analyzer.reverse_dns_lookup(args.reverse_dns)
    
    elif args.shodan_host:
        shodan = ShodanIntegration(args.shodan_key)
        results['shodan_host'] = shodan.search_host(args.shodan_host)
    
    elif args.shodan_domain:
        shodan = ShodanIntegration(args.shodan_key)
        results['shodan_domain'] = shodan.search_domain(args.shodan_domain)
    
    elif args.username:
        social = SocialMediaOSINT()
        results['username_search'] = social.search_username(args.username)
    
    elif args.email:
        social = SocialMediaOSINT()
        results['email_search'] = social.search_email(args.email)
    
    elif args.metadata:
        extractor = MetadataExtractor()
        results['metadata'] = extractor.extract_file_metadata(args.metadata)
    
    else:
        parser.print_help()
        sys.exit(0)
    
    if args.save and results:
        save_results(results, "osint", "json")

if __name__ == "__main__":
    main()
