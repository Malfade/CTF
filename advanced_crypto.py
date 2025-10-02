#!/usr/bin/env python3
"""
Advanced Crypto Tools - Продвинутые инструменты криптографии
"""

import argparse
import sys
import base64
import binascii
import hashlib
import string
import itertools
import math
import random
from typing import List, Dict, Optional, Tuple
try:
    from Crypto.Cipher import AES, DES, DES3, Blowfish
    from Crypto.Util.Padding import pad, unpad
    from Crypto.PublicKey import RSA, DSA, ECC
    from Crypto.Signature import DSS
    from Crypto.Hash import SHA256, SHA1, MD5
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print_warning("pycryptodome не установлен - криптографические функции недоступны")
from utils import *

class AdvancedCipherTools:
    """Продвинутые инструменты шифрования"""
    
    def __init__(self):
        self.cipher_methods = {
            'aes': self._aes_encrypt,
            'des': self._des_encrypt,
            'des3': self._des3_encrypt,
            'blowfish': self._blowfish_encrypt,
            'rc4': self._rc4_encrypt,
            'vigenere': self._vigenere_encrypt,
            'rail_fence': self._rail_fence_encrypt,
            'columnar': self._columnar_encrypt
        }
    
    def encrypt_text(self, text: str, method: str, key: str, **kwargs) -> str:
        """Шифрование текста различными методами"""
        if not CRYPTO_AVAILABLE and method in ['aes', 'des', 'des3', 'blowfish']:
            print_error("Криптографические функции недоступны - установите pycryptodome")
            return None
            
        print_info(f"Шифрование методом {method.upper()}...")
        
        if method not in self.cipher_methods:
            print_error(f"Неподдерживаемый метод: {method}")
            return None
        
        try:
            result = self.cipher_methods[method](text, key, **kwargs)
            print_success(f"Текст зашифрован методом {method.upper()}")
            return result
        except Exception as e:
            print_error(f"Ошибка шифрования: {e}")
            return None
    
    def decrypt_text(self, ciphertext: str, method: str, key: str, **kwargs) -> str:
        """Дешифрование текста"""
        if not CRYPTO_AVAILABLE and method in ['aes', 'des', 'des3', 'blowfish']:
            print_error("Криптографические функции недоступны - установите pycryptodome")
            return None
            
        print_info(f"Дешифрование методом {method.upper()}...")
        
        decrypt_methods = {
            'aes': self._aes_decrypt,
            'des': self._des_decrypt,
            'des3': self._des3_decrypt,
            'blowfish': self._blowfish_decrypt,
            'rc4': self._rc4_decrypt,
            'vigenere': self._vigenere_decrypt,
            'rail_fence': self._rail_fence_decrypt,
            'columnar': self._columnar_decrypt
        }
        
        if method not in decrypt_methods:
            print_error(f"Неподдерживаемый метод: {method}")
            return None
        
        try:
            result = decrypt_methods[method](ciphertext, key, **kwargs)
            print_success(f"Текст дешифрован методом {method.upper()}")
            return result
        except Exception as e:
            print_error(f"Ошибка дешифрования: {e}")
            return None
    
    def _aes_encrypt(self, text: str, key: str, mode: str = 'ECB') -> str:
        """AES шифрование"""
        key_bytes = key.encode()[:32]  # AES-256
        if len(key_bytes) < 32:
            key_bytes = key_bytes.ljust(32, b'\0')
        
        cipher = AES.new(key_bytes, AES.MODE_ECB if mode == 'ECB' else AES.MODE_CBC)
        padded_text = pad(text.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted).decode()
    
    def _aes_decrypt(self, ciphertext: str, key: str, mode: str = 'ECB') -> str:
        """AES дешифрование"""
        key_bytes = key.encode()[:32]
        if len(key_bytes) < 32:
            key_bytes = key_bytes.ljust(32, b'\0')
        
        cipher = AES.new(key_bytes, AES.MODE_ECB if mode == 'ECB' else AES.MODE_CBC)
        encrypted = base64.b64decode(ciphertext)
        decrypted = cipher.decrypt(encrypted)
        return unpad(decrypted, AES.block_size).decode()
    
    def _des_encrypt(self, text: str, key: str) -> str:
        """DES шифрование"""
        key_bytes = key.encode()[:8]
        if len(key_bytes) < 8:
            key_bytes = key_bytes.ljust(8, b'\0')
        
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        padded_text = pad(text.encode(), DES.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted).decode()
    
    def _des_decrypt(self, ciphertext: str, key: str) -> str:
        """DES дешифрование"""
        key_bytes = key.encode()[:8]
        if len(key_bytes) < 8:
            key_bytes = key_bytes.ljust(8, b'\0')
        
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        encrypted = base64.b64decode(ciphertext)
        decrypted = cipher.decrypt(encrypted)
        return unpad(decrypted, DES.block_size).decode()
    
    def _des3_encrypt(self, text: str, key: str) -> str:
        """3DES шифрование"""
        key_bytes = key.encode()[:24]
        if len(key_bytes) < 24:
            key_bytes = key_bytes.ljust(24, b'\0')
        
        cipher = DES3.new(key_bytes, DES3.MODE_ECB)
        padded_text = pad(text.encode(), DES3.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted).decode()
    
    def _des3_decrypt(self, ciphertext: str, key: str) -> str:
        """3DES дешифрование"""
        key_bytes = key.encode()[:24]
        if len(key_bytes) < 24:
            key_bytes = key_bytes.ljust(24, b'\0')
        
        cipher = DES3.new(key_bytes, DES3.MODE_ECB)
        encrypted = base64.b64decode(ciphertext)
        decrypted = cipher.decrypt(encrypted)
        return unpad(decrypted, DES3.block_size).decode()
    
    def _blowfish_encrypt(self, text: str, key: str) -> str:
        """Blowfish шифрование"""
        key_bytes = key.encode()[:56]  # Blowfish поддерживает до 56 байт
        cipher = Blowfish.new(key_bytes, Blowfish.MODE_ECB)
        padded_text = pad(text.encode(), Blowfish.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted).decode()
    
    def _blowfish_decrypt(self, ciphertext: str, key: str) -> str:
        """Blowfish дешифрование"""
        key_bytes = key.encode()[:56]
        cipher = Blowfish.new(key_bytes, Blowfish.MODE_ECB)
        encrypted = base64.b64decode(ciphertext)
        decrypted = cipher.decrypt(encrypted)
        return unpad(decrypted, Blowfish.block_size).decode()
    
    def _rc4_encrypt(self, text: str, key: str) -> str:
        """RC4 шифрование"""
        # Простая реализация RC4
        key_bytes = key.encode()
        S = list(range(256))
        j = 0
        
        # KSA (Key Scheduling Algorithm)
        for i in range(256):
            j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
            S[i], S[j] = S[j], S[i]
        
        # PRGA (Pseudo-Random Generation Algorithm)
        i = j = 0
        encrypted = []
        for byte in text.encode():
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = S[(S[i] + S[j]) % 256]
            encrypted.append(byte ^ k)
        
        return base64.b64encode(bytes(encrypted)).decode()
    
    def _rc4_decrypt(self, ciphertext: str, key: str) -> str:
        """RC4 дешифрование (то же что и шифрование)"""
        return self._rc4_encrypt(ciphertext, key)
    
    def _vigenere_encrypt(self, text: str, key: str) -> str:
        """Шифр Виженера"""
        key = key.upper()
        result = []
        key_index = 0
        
        for char in text.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result.append(encrypted_char)
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _vigenere_decrypt(self, ciphertext: str, key: str) -> str:
        """Дешифрование Виженера"""
        key = key.upper()
        result = []
        key_index = 0
        
        for char in ciphertext.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                result.append(decrypted_char)
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _rail_fence_encrypt(self, text: str, key: str, rails: int = 3) -> str:
        """Rail Fence шифрование"""
        if rails <= 1:
            return text
        
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for char in text:
            fence[rail].append(char)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        return ''.join(''.join(row) for row in fence)
    
    def _rail_fence_decrypt(self, ciphertext: str, key: str, rails: int = 3) -> str:
        """Rail Fence дешифрование"""
        if rails <= 1:
            return ciphertext
        
        # Создаем паттерн
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for _ in ciphertext:
            fence[rail].append('*')
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        # Заполняем паттерн
        index = 0
        for row in fence:
            for i in range(len(row)):
                row[i] = ciphertext[index]
                index += 1
        
        # Читаем по паттерну
        result = []
        rail = 0
        direction = 1
        
        for _ in ciphertext:
            result.append(fence[rail].pop(0))
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        return ''.join(result)
    
    def _columnar_encrypt(self, text: str, key: str) -> str:
        """Columnar Transposition шифрование"""
        # Удаляем пробелы и приводим к верхнему регистру
        text = text.replace(' ', '').upper()
        key = key.upper()
        
        # Создаем матрицу
        cols = len(key)
        rows = math.ceil(len(text) / cols)
        
        # Заполняем матрицу
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                index = i * cols + j
                if index < len(text):
                    row.append(text[index])
                else:
                    row.append('X')  # Padding
            matrix.append(row)
        
        # Сортируем колонки по ключу
        key_order = sorted(range(len(key)), key=lambda x: key[x])
        
        # Читаем по отсортированным колонкам
        result = []
        for col in key_order:
            for row in matrix:
                result.append(row[col])
        
        return ''.join(result)
    
    def _columnar_decrypt(self, ciphertext: str, key: str) -> str:
        """Columnar Transposition дешифрование"""
        key = key.upper()
        cols = len(key)
        rows = math.ceil(len(ciphertext) / cols)
        
        # Определяем порядок колонок
        key_order = sorted(range(len(key)), key=lambda x: key[x])
        
        # Создаем матрицу
        matrix = [[''] * cols for _ in range(rows)]
        
        # Заполняем матрицу по колонкам
        index = 0
        for col in key_order:
            for row in range(rows):
                if index < len(ciphertext):
                    matrix[row][col] = ciphertext[index]
                    index += 1
        
        # Читаем по строкам
        result = []
        for row in matrix:
            result.extend(row)
        
        return ''.join(result).rstrip('X')

class RSAOperations:
    """Операции с RSA"""
    
    def generate_rsa_keys(self, key_size: int = 2048) -> Tuple[str, str]:
        """Генерация RSA ключей"""
        if not CRYPTO_AVAILABLE:
            print_error("Криптографические функции недоступны - установите pycryptodome")
            return None, None
            
        print_info(f"Генерация RSA ключей ({key_size} бит)...")
        
        try:
            key = RSA.generate(key_size)
            private_key = key.export_key().decode()
            public_key = key.publickey().export_key().decode()
            
            print_success("RSA ключи сгенерированы")
            return private_key, public_key
        except Exception as e:
            print_error(f"Ошибка генерации ключей: {e}")
            return None, None
    
    def rsa_encrypt(self, text: str, public_key: str) -> str:
        """RSA шифрование"""
        print_info("RSA шифрование...")
        
        try:
            key = RSA.import_key(public_key)
            cipher = key.encrypt(text.encode(), 32)[0]
            return base64.b64encode(cipher).decode()
        except Exception as e:
            print_error(f"Ошибка RSA шифрования: {e}")
            return None
    
    def rsa_decrypt(self, ciphertext: str, private_key: str) -> str:
        """RSA дешифрование"""
        print_info("RSA дешифрование...")
        
        try:
            key = RSA.import_key(private_key)
            encrypted = base64.b64decode(ciphertext)
            decrypted = key.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            print_error(f"Ошибка RSA дешифрования: {e}")
            return None
    
    def rsa_sign(self, text: str, private_key: str) -> str:
        """RSA подпись"""
        print_info("RSA подпись...")
        
        try:
            key = RSA.import_key(private_key)
            hash_obj = SHA256.new(text.encode())
            signature = key.sign(hash_obj, '')
            return base64.b64encode(signature[0]).decode()
        except Exception as e:
            print_error(f"Ошибка RSA подписи: {e}")
            return None
    
    def rsa_verify(self, text: str, signature: str, public_key: str) -> bool:
        """RSA проверка подписи"""
        print_info("RSA проверка подписи...")
        
        try:
            key = RSA.import_key(public_key)
            hash_obj = SHA256.new(text.encode())
            sig_bytes = base64.b64decode(signature)
            key.verify(hash_obj, (int.from_bytes(sig_bytes, 'big'),))
            print_success("Подпись действительна")
            return True
        except Exception as e:
            print_error(f"Подпись недействительна: {e}")
            return False

class HashAnalysis:
    """Анализ хешей"""
    
    def __init__(self):
        self.hash_functions = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha224': hashlib.sha224,
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384,
            'sha512': hashlib.sha512,
            'blake2b': hashlib.blake2b,
            'blake2s': hashlib.blake2s
        }
    
    def identify_hash_type(self, hash_value: str) -> List[str]:
        """Определение типа хеша по длине"""
        hash_length = len(hash_value)
        
        possible_types = {
            32: ['md5'],
            40: ['sha1'],
            56: ['sha224'],
            64: ['sha256', 'blake2s'],
            96: ['sha384'],
            128: ['sha512', 'blake2b']
        }
        
        return possible_types.get(hash_length, ['unknown'])
    
    def rainbow_table_attack(self, target_hash: str, wordlist: List[str], 
                           algorithm: str = 'md5') -> Optional[str]:
        """Атака по радужной таблице"""
        print_info(f"Rainbow table атака на {algorithm.upper()} хеш...")
        
        if algorithm not in self.hash_functions:
            print_error(f"Неподдерживаемый алгоритм: {algorithm}")
            return None
        
        hasher = self.hash_functions[algorithm]
        
        for i, word in enumerate(wordlist):
            word = word.strip()
            hash_obj = hasher()
            hash_obj.update(word.encode())
            
            if hash_obj.hexdigest() == target_hash.lower():
                print_success(f"Найден пароль: {word}")
                return word
            
            if i % 10000 == 0:
                progress_bar(i, len(wordlist))
        
        print()
        print_error("Пароль не найден в радужной таблице")
        return None
    
    def dictionary_attack(self, target_hash: str, dictionary: List[str], 
                         algorithm: str = 'md5') -> Optional[str]:
        """Словарная атака"""
        print_info(f"Словарная атака на {algorithm.upper()} хеш...")
        
        if algorithm not in self.hash_functions:
            print_error(f"Неподдерживаемый алгоритм: {algorithm}")
            return None
        
        hasher = self.hash_functions[algorithm]
        
        for i, word in enumerate(dictionary):
            word = word.strip()
            
            # Пробуем различные варианты
            variants = [
                word,
                word.lower(),
                word.upper(),
                word.capitalize(),
                word + '123',
                '123' + word,
                word + '!',
                word + '@',
                word + '#'
            ]
            
            for variant in variants:
                hash_obj = hasher()
                hash_obj.update(variant.encode())
                
                if hash_obj.hexdigest() == target_hash.lower():
                    print_success(f"Найден пароль: {variant}")
                    return variant
            
            if i % 1000 == 0:
                progress_bar(i, len(dictionary))
        
        print()
        print_error("Пароль не найден в словаре")
        return None

class SteganographyAdvanced:
    """Продвинутая стеганография"""
    
    def __init__(self):
        pass
    
    def lsb_analysis(self, image_path: str) -> Dict:
        """Анализ LSB стеганографии"""
        print_info(f"LSB анализ изображения: {image_path}")
        
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Анализ младших битов
            lsb_analysis = {
                'image_size': img.size,
                'mode': img.mode,
                'lsb_patterns': {},
                'entropy': 0,
                'suspicious_regions': []
            }
            
            # Анализ каждого канала
            if len(img_array.shape) == 3:  # RGB
                for channel in range(3):
                    channel_data = img_array[:, :, channel]
                    lsb_data = channel_data & 1
                    
                    # Подсчет паттернов
                    unique, counts = np.unique(lsb_data, return_counts=True)
                    lsb_analysis['lsb_patterns'][f'channel_{channel}'] = dict(zip(unique, counts))
            
            # Вычисление энтропии
            lsb_analysis['entropy'] = self._calculate_entropy(img_array)
            
            print_success("LSB анализ завершен")
            return lsb_analysis
            
        except Exception as e:
            print_error(f"Ошибка LSB анализа: {e}")
            return {}
    
    def _calculate_entropy(self, image_array) -> float:
        """Вычисление энтропии изображения"""
        try:
            import numpy as np
            
            # Вычисляем гистограмму
            hist, _ = np.histogram(image_array.flatten(), bins=256, range=(0, 256))
            hist = hist / hist.sum()
            
            # Убираем нулевые значения
            hist = hist[hist > 0]
            
            # Вычисляем энтропию
            entropy = -np.sum(hist * np.log2(hist))
            return entropy
            
        except:
            return 0.0
    
    def frequency_analysis(self, text: str) -> Dict:
        """Частотный анализ текста"""
        print_info("Частотный анализ текста...")
        
        # Подсчет частоты символов
        char_freq = {}
        for char in text.lower():
            if char.isalpha():
                char_freq[char] = char_freq.get(char, 0) + 1
        
        # Сортировка по частоте
        sorted_freq = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Анализ соответствия английскому языку
        english_freq = {
            'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
            's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
            'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
            'p': 1.9, 'b': 1.3, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
            'q': 0.10, 'z': 0.07
        }
        
        total_chars = sum(char_freq.values())
        analysis = {
            'character_frequency': dict(sorted_freq),
            'total_characters': total_chars,
            'english_similarity': 0,
            'most_common': sorted_freq[:5] if sorted_freq else []
        }
        
        # Вычисление сходства с английским
        similarity = 0
        for char, freq in char_freq.items():
            if char in english_freq:
                expected_freq = english_freq[char] * total_chars / 100
                actual_freq = freq
                similarity += min(expected_freq, actual_freq) / max(expected_freq, actual_freq)
        
        analysis['english_similarity'] = similarity / len(english_freq) * 100
        
        print_success("Частотный анализ завершен")
        return analysis

def main():
    parser = argparse.ArgumentParser(description='Advanced Crypto Tools')
    parser.add_argument('--encrypt', help='Текст для шифрования')
    parser.add_argument('--decrypt', help='Текст для дешифрования')
    parser.add_argument('--method', choices=['aes', 'des', 'des3', 'blowfish', 'rc4', 'vigenere', 'rail_fence', 'columnar'], 
                       default='aes', help='Метод шифрования')
    parser.add_argument('--key', required=True, help='Ключ шифрования')
    parser.add_argument('--rails', type=int, default=3, help='Количество рельсов для Rail Fence')
    parser.add_argument('--generate-rsa', type=int, metavar='SIZE', help='Генерация RSA ключей указанного размера')
    parser.add_argument('--rsa-encrypt', help='Текст для RSA шифрования')
    parser.add_argument('--rsa-decrypt', help='Текст для RSA дешифрования')
    parser.add_argument('--public-key', help='RSA публичный ключ')
    parser.add_argument('--private-key', help='RSA приватный ключ')
    parser.add_argument('--sign', help='Текст для подписи')
    parser.add_argument('--verify', help='Текст для проверки подписи')
    parser.add_argument('--signature', help='Подпись для проверки')
    parser.add_argument('--crack-hash', help='Хеш для взлома')
    parser.add_argument('--hash-type', choices=['md5', 'sha1', 'sha256', 'sha512'], 
                       default='md5', help='Тип хеша')
    parser.add_argument('--wordlist', help='Путь к словарю')
    parser.add_argument('--identify-hash', help='Хеш для определения типа')
    parser.add_argument('--lsb-analysis', help='Путь к изображению для LSB анализа')
    parser.add_argument('--frequency-analysis', help='Текст для частотного анализа')
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    results = []
    
    # Инициализация инструментов
    cipher_tools = AdvancedCipherTools()
    rsa_tools = RSAOperations()
    hash_analysis = HashAnalysis()
    stego_tools = SteganographyAdvanced()
    
    # Шифрование
    if args.encrypt:
        result = cipher_tools.encrypt_text(args.encrypt, args.method, args.key, rails=args.rails)
        if result:
            results.append({'type': 'encryption', 'method': args.method, 'result': result})
            print_success(f"Зашифрованный текст: {result}")
    
    # Дешифрование
    elif args.decrypt:
        result = cipher_tools.decrypt_text(args.decrypt, args.method, args.key, rails=args.rails)
        if result:
            results.append({'type': 'decryption', 'method': args.method, 'result': result})
            print_success(f"Дешифрованный текст: {result}")
    
    # Генерация RSA ключей
    elif args.generate_rsa:
        private_key, public_key = rsa_tools.generate_rsa_keys(args.generate_rsa)
        if private_key and public_key:
            results.append({'type': 'rsa_keys', 'private': private_key, 'public': public_key})
            print_success("RSA ключи сгенерированы")
            print_info(f"Приватный ключ:\n{private_key}")
            print_info(f"Публичный ключ:\n{public_key}")
    
    # RSA шифрование
    elif args.rsa_encrypt and args.public_key:
        result = rsa_tools.rsa_encrypt(args.rsa_encrypt, args.public_key)
        if result:
            results.append({'type': 'rsa_encryption', 'result': result})
            print_success(f"RSA зашифрованный текст: {result}")
    
    # RSA дешифрование
    elif args.rsa_decrypt and args.private_key:
        result = rsa_tools.rsa_decrypt(args.rsa_decrypt, args.private_key)
        if result:
            results.append({'type': 'rsa_decryption', 'result': result})
            print_success(f"RSA дешифрованный текст: {result}")
    
    # RSA подпись
    elif args.sign and args.private_key:
        result = rsa_tools.rsa_sign(args.sign, args.private_key)
        if result:
            results.append({'type': 'rsa_signature', 'result': result})
            print_success(f"RSA подпись: {result}")
    
    # RSA проверка подписи
    elif args.verify and args.signature and args.public_key:
        result = rsa_tools.rsa_verify(args.verify, args.signature, args.public_key)
        results.append({'type': 'rsa_verification', 'result': result})
    
    # Взлом хеша
    elif args.crack_hash:
        if args.wordlist:
            try:
                with open(args.wordlist, 'r', encoding='utf-8') as f:
                    wordlist = f.readlines()
                result = hash_analysis.dictionary_attack(args.crack_hash, wordlist, args.hash_type)
            except Exception as e:
                print_error(f"Ошибка чтения словаря: {e}")
                result = None
        else:
            # Простой брутфорс
            common_passwords = [
                'password', '123456', 'admin', 'root', 'user', 'test',
                'qwerty', 'abc123', 'password123', 'admin123'
            ]
            result = hash_analysis.dictionary_attack(args.crack_hash, common_passwords, args.hash_type)
        
        if result:
            results.append({'type': 'hash_cracked', 'password': result, 'hash': args.crack_hash})
    
    # Определение типа хеша
    elif args.identify_hash:
        hash_types = hash_analysis.identify_hash_type(args.identify_hash)
        results.append({'type': 'hash_identification', 'hash': args.identify_hash, 'possible_types': hash_types})
        print_success(f"Возможные типы хеша: {', '.join(hash_types)}")
    
    # LSB анализ
    elif args.lsb_analysis:
        result = stego_tools.lsb_analysis(args.lsb_analysis)
        if result:
            results.append({'type': 'lsb_analysis', 'result': result})
            print_success(f"LSB анализ завершен. Энтропия: {result.get('entropy', 0):.2f}")
    
    # Частотный анализ
    elif args.frequency_analysis:
        result = stego_tools.frequency_analysis(args.frequency_analysis)
        if result:
            results.append({'type': 'frequency_analysis', 'result': result})
            print_success(f"Частотный анализ завершен. Сходство с английским: {result.get('english_similarity', 0):.1f}%")
    
    else:
        parser.print_help()
        sys.exit(0)
    
    # Вывод результатов
    print(f"\n{Colors.HEADER}{'=' * 50}{Colors.RESET}")
    print_success(f"Выполнено операций: {len(results)}")
    
    if args.save and results:
        save_results(results, "advanced_crypto", "json")

if __name__ == "__main__":
    main()
