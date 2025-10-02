#!/usr/bin/env python3
"""
Defense Monitor - Инструменты для защиты и мониторинга
"""

import psutil
import argparse
import time
import sys
from datetime import datetime
from collections import defaultdict
from typing import List, Dict
from utils import *

class SystemMonitor:
    """Мониторинг системы"""
    
    def __init__(self):
        self.baseline = {}
        self.alerts = []
    
    def get_network_connections(self) -> List[Dict]:
        """Получение сетевых соединений"""
        connections = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED':
                connections.append({
                    'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                    'status': conn.status,
                    'pid': conn.pid
                })
        return connections
    
    def monitor_network(self, interval: int = 5, duration: int = 60):
        """Мониторинг сетевых соединений"""
        print_info(f"Мониторинг сети ({duration} секунд, интервал {interval}с)...")
        
        connection_count = defaultdict(int)
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                connections = self.get_network_connections()
                
                for conn in connections:
                    remote = conn['remote_addr']
                    if remote != "N/A":
                        connection_count[remote] += 1
                
                print(f"\r[*] Активных соединений: {len(connections)}", end='', flush=True)
                time.sleep(interval)
            
            print()
            
            # Анализ подозрительных соединений
            print_info("Топ соединений:")
            sorted_conns = sorted(connection_count.items(), key=lambda x: x[1], reverse=True)
            for remote, count in sorted_conns[:10]:
                if count > 10:
                    print_warning(f"{remote}: {count} соединений (подозрительно!)")
                else:
                    print_info(f"{remote}: {count} соединений")
            
            return connection_count
            
        except KeyboardInterrupt:
            print_info("\nМониторинг остановлен")
            return connection_count
    
    def check_suspicious_processes(self) -> List[Dict]:
        """Проверка подозрительных процессов"""
        print_info("Проверка процессов...")
        suspicious = []
        
        # Подозрительные имена процессов
        suspicious_names = [
            'nc', 'netcat', 'nmap', 'tcpdump', 'wireshark',
            'metasploit', 'msfconsole', 'sqlmap', 'hydra',
            'john', 'hashcat', 'aircrack', 'ettercap'
        ]
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
            try:
                name = proc.info['name'].lower()
                for sus_name in suspicious_names:
                    if sus_name in name:
                        suspicious.append(proc.info)
                        print_warning(f"Подозрительный процесс: {proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if not suspicious:
            print_success("Подозрительных процессов не обнаружено")
        
        return suspicious
    
    def monitor_file_changes(self, directory: str, duration: int = 60):
        """Мониторинг изменений файлов"""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class ChangeHandler(FileSystemEventHandler):
            def __init__(self):
                self.changes = []
            
            def on_modified(self, event):
                if not event.is_directory:
                    print_warning(f"Изменен: {event.src_path}")
                    self.changes.append(('modified', event.src_path))
            
            def on_created(self, event):
                if not event.is_directory:
                    print_warning(f"Создан: {event.src_path}")
                    self.changes.append(('created', event.src_path))
            
            def on_deleted(self, event):
                if not event.is_directory:
                    print_error(f"Удален: {event.src_path}")
                    self.changes.append(('deleted', event.src_path))
        
        print_info(f"Мониторинг изменений в {directory} ({duration}с)...")
        
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, directory, recursive=True)
        observer.start()
        
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            pass
        
        observer.stop()
        observer.join()
        
        print_success(f"Зафиксировано изменений: {len(event_handler.changes)}")
        return event_handler.changes
    
    def get_system_info(self) -> Dict:
        """Получение информации о системе"""
        print_info("Сбор информации о системе...")
        
        info = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections()),
            'processes': len(psutil.pids()),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print_success(f"CPU: {info['cpu_percent']}%")
        print_success(f"Память: {info['memory_percent']}%")
        print_success(f"Диск: {info['disk_percent']}%")
        print_success(f"Сетевые соединения: {info['network_connections']}")
        print_success(f"Процессов: {info['processes']}")
        print_success(f"Время загрузки: {info['boot_time']}")
        
        return info

class PortMonitor:
    """Мониторинг открытых портов"""
    
    def __init__(self):
        self.baseline_ports = set()
    
    def get_listening_ports(self) -> List[Dict]:
        """Получение слушающих портов"""
        ports = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'LISTEN':
                ports.append({
                    'port': conn.laddr.port,
                    'address': conn.laddr.ip,
                    'pid': conn.pid
                })
        return ports
    
    def create_baseline(self):
        """Создание baseline открытых портов"""
        print_info("Создание baseline портов...")
        ports = self.get_listening_ports()
        self.baseline_ports = {p['port'] for p in ports}
        print_success(f"Baseline создан: {len(self.baseline_ports)} портов")
        return ports
    
    def check_new_ports(self) -> List[Dict]:
        """Проверка новых открытых портов"""
        if not self.baseline_ports:
            print_warning("Baseline не создан, создаю...")
            self.create_baseline()
            return []
        
        current_ports = self.get_listening_ports()
        current_port_numbers = {p['port'] for p in current_ports}
        
        new_ports = current_port_numbers - self.baseline_ports
        
        if new_ports:
            print_warning(f"Обнаружены новые открытые порты: {new_ports}")
            new_port_info = [p for p in current_ports if p['port'] in new_ports]
            for port_info in new_port_info:
                print_warning(f"  Порт {port_info['port']}: {port_info['address']} (PID: {port_info['pid']})")
            return new_port_info
        else:
            print_success("Новых портов не обнаружено")
            return []
    
    def monitor_ports(self, interval: int = 5, duration: int = 60):
        """Непрерывный мониторинг портов"""
        print_info("Создание baseline...")
        self.create_baseline()
        
        print_info(f"Мониторинг портов ({duration}с, интервал {interval}с)...")
        start_time = time.time()
        alerts = []
        
        try:
            while time.time() - start_time < duration:
                time.sleep(interval)
                new_ports = self.check_new_ports()
                if new_ports:
                    alerts.extend(new_ports)
                    # Обновляем baseline
                    current_ports = self.get_listening_ports()
                    self.baseline_ports = {p['port'] for p in current_ports}
        except KeyboardInterrupt:
            print_info("\nМониторинг остановлен")
        
        if alerts:
            print_warning(f"Всего предупреждений: {len(alerts)}")
        else:
            print_success("Предупреждений нет")
        
        return alerts

class LogAnalyzer:
    """Анализатор логов для обнаружения атак"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
    
    def detect_bruteforce(self, threshold: int = 5) -> List[Dict]:
        """Обнаружение brute force атак"""
        print_info(f"Анализ {self.log_file} на brute force...")
        
        failed_attempts = defaultdict(int)
        
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    # Поиск неудачных попыток входа
                    if 'failed' in line.lower() or 'authentication failure' in line.lower():
                        # Извлечение IP адреса (простой паттерн)
                        import re
                        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
                        ips = re.findall(ip_pattern, line)
                        if ips:
                            failed_attempts[ips[0]] += 1
            
            # Поиск IP с превышением порога
            attacks = []
            for ip, count in failed_attempts.items():
                if count >= threshold:
                    attacks.append({'ip': ip, 'attempts': count})
                    print_warning(f"Возможная brute force атака с {ip}: {count} попыток")
            
            if not attacks:
                print_success("Brute force атак не обнаружено")
            
            return attacks
            
        except Exception as e:
            print_error(f"Ошибка анализа лога: {e}")
            return []

def main():
    parser = argparse.ArgumentParser(
        description="Defense Monitor - Инструменты защиты и мониторинга",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --monitor-network --duration 120
  %(prog)s --check-processes
  %(prog)s --monitor-ports --duration 300
  %(prog)s --system-info
  %(prog)s --analyze-log /var/log/auth.log
        """
    )
    
    parser.add_argument('--monitor-network', action='store_true', help='Мониторинг сети')
    parser.add_argument('--check-processes', action='store_true', help='Проверка процессов')
    parser.add_argument('--monitor-ports', action='store_true', help='Мониторинг портов')
    parser.add_argument('--monitor-files', metavar='DIR', help='Мониторинг изменений файлов')
    parser.add_argument('--system-info', action='store_true', help='Информация о системе')
    parser.add_argument('--analyze-log', metavar='FILE', help='Анализ лог-файла')
    parser.add_argument('--duration', type=int, default=60, help='Длительность мониторинга (секунды)')
    parser.add_argument('--interval', type=int, default=5, help='Интервал проверки (секунды)')
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    print_banner("DEFENSE MONITOR")
    
    monitor = SystemMonitor()
    results = {}
    
    if args.monitor_network:
        results['network'] = monitor.monitor_network(args.interval, args.duration)
    
    elif args.check_processes:
        results['processes'] = monitor.check_suspicious_processes()
    
    elif args.monitor_ports:
        port_monitor = PortMonitor()
        results['ports'] = port_monitor.monitor_ports(args.interval, args.duration)
    
    elif args.monitor_files:
        results['files'] = monitor.monitor_file_changes(args.monitor_files, args.duration)
    
    elif args.system_info:
        results['system'] = monitor.get_system_info()
    
    elif args.analyze_log:
        analyzer = LogAnalyzer(args.analyze_log)
        results['bruteforce'] = analyzer.detect_bruteforce()
    
    else:
        parser.print_help()
        sys.exit(0)
    
    if args.save and results:
        save_results(results, "defense_monitor", "json")

if __name__ == "__main__":
    main()




