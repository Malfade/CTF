#!/usr/bin/env python3
"""
Phishing Monitor - Интерактивный мониторинг фишинговой атаки
ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!
"""

import os
import time
import json
import glob
import sys
from datetime import datetime

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    print("\033[91m" + "="*80)
    print("🎣 PHISHING MONITOR - CTF REAL-TIME MONITORING")
    print("="*80 + "\033[0m")
    print("\033[93m⚠️  ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!\033[0m")
    print()

def print_status(server_port, target_domain):
    print(f"\033[94m🌐 Сервер: http://localhost:{server_port}\033[0m")
    print(f"\033[94m🎯 Цель: {target_domain}\033[0m")
    print(f"\033[94m📁 Данные: phishing_data/\033[0m")
    print()

def get_credentials_count():
    data_dir = "phishing_data"
    if not os.path.exists(data_dir):
        return 0
    json_files = glob.glob(os.path.join(data_dir, "credentials_*.json"))
    return len(json_files)

def get_latest_credentials():
    data_dir = "phishing_data"
    if not os.path.exists(data_dir):
        return []
    
    json_files = glob.glob(os.path.join(data_dir, "credentials_*.json"))
    if not json_files:
        return []
    
    # Сортируем по времени модификации
    json_files.sort(key=os.path.getmtime, reverse=True)
    
    latest_creds = []
    for file_path in json_files[:5]:  # Последние 5
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                latest_creds.append(data)
        except:
            continue
    
    return latest_creds

def print_credentials(creds):
    if not creds:
        print("\033[90m📊 Пока нет собранных данных...\033[0m")
        return
    
    print(f"\033[92m📊 Последние {len(creds)} записей:\033[0m")
    print()
    
    for i, cred in enumerate(creds, 1):
        username = cred.get('username', 'N/A')
        target = cred.get('target', 'N/A')
        timestamp = cred.get('timestamp', 'N/A')
        
        print(f"\033[96m[{i}]\033[0m \033[93m{username}\033[0m -> \033[94m{target}\033[0m")
        print(f"     \033[90m{timestamp}\033[0m")
        print()

def print_instructions():
    print("\033[95m💡 Инструкции:\033[0m")
    print("  • Отправьте URL жертве в CTF")
    print("  • Данные будут появляться здесь в реальном времени")
    print("  • Нажмите Ctrl+C для выхода")
    print()

def main():
    if len(sys.argv) != 3:
        print("Использование: python3 phishing_monitor.py <port> <domain>")
        sys.exit(1)
    
    server_port = sys.argv[1]
    target_domain = sys.argv[2]
    last_count = 0
    
    try:
        while True:
            clear_screen()
            print_banner()
            print_status(server_port, target_domain)
            
            # Получаем текущее количество данных
            current_count = get_credentials_count()
            
            if current_count > last_count:
                print(f"\033[92m🎉 НОВЫЕ ДАННЫЕ! Всего: {current_count}\033[0m")
                last_count = current_count
            else:
                print(f"\033[94m📊 Всего данных: {current_count}\033[0m")
            
            print()
            
            # Показываем последние данные
            latest_creds = get_latest_credentials()
            print_credentials(latest_creds)
            
            print_instructions()
            
            # Обновляем каждые 2 секунды
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\033[91m👋 Мониторинг остановлен\033[0m")

if __name__ == "__main__":
    main()

