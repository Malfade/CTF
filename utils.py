#!/usr/bin/env python3
"""
Общие утилиты для CTF инструментов
"""

import os
import sys
import time
import hashlib
import base64
import binascii
from datetime import datetime
from colorama import init, Fore, Style
from typing import List, Dict, Any, Optional

# Инициализация colorama
init(autoreset=True)

class Colors:
    """Цвета для вывода"""
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE
    RESET = Style.RESET_ALL

def print_banner(tool_name: str, version: str = "1.0"):
    """Красивый баннер для инструмента"""
    banner = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════╗
║           CTF TOOLS - {tool_name:<30}║
║           Version: {version:<35}║
╚═══════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def print_success(message: str):
    """Печать сообщения об успехе"""
    print(f"{Colors.SUCCESS}[+] {message}{Colors.RESET}")

def print_error(message: str):
    """Печать сообщения об ошибке"""
    print(f"{Colors.ERROR}[-] {message}{Colors.RESET}")

def print_warning(message: str):
    """Печать предупреждения"""
    print(f"{Colors.WARNING}[!] {message}{Colors.RESET}")

def print_info(message: str):
    """Печать информации"""
    print(f"{Colors.INFO}[*] {message}{Colors.RESET}")

def save_results(data: Any, filename: str, format: str = "txt"):
    """Сохранение результатов в файл"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "ctf_results"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, f"{filename}_{timestamp}.{format}")
        
        if format == "txt":
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(data))
        elif format == "json":
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        
        print_success(f"Результаты сохранены: {filepath}")
        return filepath
    except Exception as e:
        print_error(f"Ошибка сохранения: {e}")
        return None

def calculate_hash(data: bytes, algorithm: str = "md5") -> str:
    """Вычисление хеша"""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Неподдерживаемый алгоритм: {algorithm}")
    
    hasher = algorithms[algorithm]()
    hasher.update(data)
    return hasher.hexdigest()

def encode_base64(data: str) -> str:
    """Кодирование в Base64"""
    return base64.b64encode(data.encode()).decode()

def decode_base64(data: str) -> str:
    """Декодирование из Base64"""
    try:
        return base64.b64decode(data).decode()
    except:
        return "Ошибка декодирования"

def hex_encode(data: str) -> str:
    """Кодирование в HEX"""
    return binascii.hexlify(data.encode()).decode()

def hex_decode(data: str) -> str:
    """Декодирование из HEX"""
    try:
        return binascii.unhexlify(data).decode()
    except:
        return "Ошибка декодирования"

def create_log_file(tool_name: str) -> str:
    """Создание файла логов"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "ctf_logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{tool_name}_{timestamp}.log")
    return log_file

def log_to_file(log_file: str, message: str):
    """Запись в файл логов"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def validate_ip(ip: str) -> bool:
    """Проверка валидности IP адреса"""
    import socket
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def validate_url(url: str) -> bool:
    """Проверка валидности URL"""
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def progress_bar(current: int, total: int, bar_length: int = 40):
    """Простой прогресс бар"""
    percent = float(current) / total
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write(f"\r[{hashes}{spaces}] {int(round(percent * 100))}%")
    sys.stdout.flush()

def get_user_confirmation(prompt: str) -> bool:
    """Получить подтверждение от пользователя"""
    response = input(f"{Colors.WARNING}{prompt} (y/n): {Colors.RESET}").lower()
    return response in ['y', 'yes', 'да']

def clear_screen():
    """Очистка экрана"""
    os.system('clear' if os.name != 'nt' else 'cls')

class RateLimiter:
    """Ограничитель скорости для запросов"""
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def wait_if_needed(self):
        """Ожидание если превышен лимит"""
        now = time.time()
        self.requests = [req for req in self.requests if now - req < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.requests = []
        
        self.requests.append(now)

if __name__ == "__main__":
    # Тесты утилит
    print_banner("UTILS TEST")
    print_success("Успех!")
    print_error("Ошибка!")
    print_warning("Предупреждение!")
    print_info("Информация!")
    
    data = "Hello CTF"
    print(f"\nОригинал: {data}")
    print(f"Base64: {encode_base64(data)}")
    print(f"HEX: {hex_encode(data)}")
    print(f"MD5: {calculate_hash(data.encode(), 'md5')}")






