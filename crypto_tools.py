#!/usr/bin/env python3
"""
Cryptography Tools - Инструменты для криптографии и взлома
"""

import hashlib
import base64
import binascii
import string
import itertools
import argparse
import sys
from typing import Optional, List
from Crypto.Cipher import AES, DES, DES3
from Crypto.Util.Padding import pad, unpad
from utils import *

class HashCracker:
    """Взломщик хешей"""
    
    def __init__(self):
        self.algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
    
    def crack_hash(self, target_hash: str, algorithm: str = 'md5', 
                   wordlist: Optional[List[str]] = None, max_length: int = 6) -> Optional[str]:
        """Взлом хеша"""
        print_info(f"Взлом {algorithm.upper()} хеша: {target_hash}")
        
        if algorithm not in self.algorithms:
            print_error(f"Неподдерживаемый алгоритм: {algorithm}")
            return None
        
        hasher_func = self.algorithms[algorithm]
        
        # Использование словаря или брутфорс
        if wordlist:
            return self._crack_with_wordlist(target_hash, hasher_func, wordlist)
        else:
            return self._crack_bruteforce(target_hash, hasher_func, max_length)
    
    def _crack_with_wordlist(self, target_hash: str, hasher_func, wordlist: List[str]) -> Optional[str]:
        """Взлом по словарю"""
        print_info(f"Проверка {len(wordlist)} паролей из словаря...")
        
        for i, word in enumerate(wordlist):
            word = word.strip()
            hash_obj = hasher_func()
            hash_obj.update(word.encode())
            if hash_obj.hexdigest() == target_hash:
                print_success(f"Найден пароль: {word}")
                return word
            
            if i % 1000 == 0:
                progress_bar(i, len(wordlist))
        
        print()
        print_error("Пароль не найден в словаре")
        return None
    
    def _crack_bruteforce(self, target_hash: str, hasher_func, max_length: int) -> Optional[str]:
        """Брутфорс взлом"""
        chars = string.ascii_lowercase + string.digits
        print_info(f"Брутфорс до длины {max_length}...")
        
        for length in range(1, max_length + 1):
            print_info(f"Проверка паролей длины {length}...")
            count = 0
            total = len(chars) ** length
            
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                hash_obj = hasher_func()
                hash_obj.update(password.encode())
                
                if hash_obj.hexdigest() == target_hash:
                    print_success(f"Найден пароль: {password}")
                    return password
                
                count += 1
                if count % 10000 == 0:
                    progress_bar(count, total)
            print()
        
        print_error("Пароль не найден")
        return None

class CipherTools:
    """Инструменты шифрования/дешифрования"""
    
    @staticmethod
    def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
        """Шифр Цезаря"""
        if decrypt:
            shift = -shift
        
        result = []
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted = (ord(char) - ascii_offset + shift) % 26
                result.append(chr(shifted + ascii_offset))
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def caesar_bruteforce(ciphertext: str) -> List[tuple]:
        """Брутфорс шифра Цезаря (все 26 вариантов)"""
        results = []
        for shift in range(26):
            decrypted = CipherTools.caesar_cipher(ciphertext, shift, decrypt=True)
            results.append((shift, decrypted))
        return results
    
    @staticmethod
    def rot13(text: str) -> str:
        """ROT13 шифрование/дешифрование"""
        return CipherTools.caesar_cipher(text, 13)
    
    @staticmethod
    def xor_cipher(data: bytes, key: bytes) -> bytes:
        """XOR шифрование"""
        return bytes(a ^ b for a, b in zip(data, itertools.cycle(key)))
    
    @staticmethod
    def xor_bruteforce(ciphertext: bytes, max_key_length: int = 4) -> List[tuple]:
        """Брутфорс XOR шифра"""
        results = []
        
        for key_length in range(1, max_key_length + 1):
            for key in itertools.product(range(256), repeat=key_length):
                key_bytes = bytes(key)
                try:
                    decrypted = CipherTools.xor_cipher(ciphertext, key_bytes)
                    # Проверка на читаемость
                    if all(32 <= b <= 126 or b in [9, 10, 13] for b in decrypted):
                        results.append((key_bytes.hex(), decrypted.decode('ascii', errors='ignore')))
                except:
                    pass
        
        return results
    
    @staticmethod
    def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
        """Шифр Виженера"""
        result = []
        key = key.upper()
        key_index = 0
        
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                key_char = key[key_index % len(key)]
                shift = ord(key_char) - 65
                
                if decrypt:
                    shift = -shift
                
                shifted = (ord(char) - ascii_offset + shift) % 26
                result.append(chr(shifted + ascii_offset))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)

class EncodingTools:
    """Инструменты кодирования/декодирования"""
    
    @staticmethod
    def encode_base64(data: str) -> str:
        """Base64 кодирование"""
        return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def decode_base64(data: str) -> str:
        """Base64 декодирование"""
        try:
            return base64.b64decode(data).decode()
        except:
            return "Ошибка декодирования"
    
    @staticmethod
    def encode_base32(data: str) -> str:
        """Base32 кодирование"""
        return base64.b32encode(data.encode()).decode()
    
    @staticmethod
    def decode_base32(data: str) -> str:
        """Base32 декодирование"""
        try:
            return base64.b32decode(data).decode()
        except:
            return "Ошибка декодирования"
    
    @staticmethod
    def encode_hex(data: str) -> str:
        """HEX кодирование"""
        return binascii.hexlify(data.encode()).decode()
    
    @staticmethod
    def decode_hex(data: str) -> str:
        """HEX декодирование"""
        try:
            return binascii.unhexlify(data).decode()
        except:
            return "Ошибка декодирования"
    
    @staticmethod
    def url_encode(data: str) -> str:
        """URL кодирование"""
        from urllib.parse import quote
        return quote(data)
    
    @staticmethod
    def url_decode(data: str) -> str:
        """URL декодирование"""
        from urllib.parse import unquote
        return unquote(data)
    
    @staticmethod
    def detect_encoding(data: str) -> str:
        """Определение типа кодирования"""
        # Base64
        try:
            base64.b64decode(data)
            if all(c in string.ascii_letters + string.digits + '+/=' for c in data):
                return "Base64"
        except:
            pass
        
        # Hex
        if all(c in string.hexdigits for c in data):
            return "Hexadecimal"
        
        # Binary
        if all(c in '01' for c in data):
            return "Binary"
        
        return "Unknown"

def main():
    parser = argparse.ArgumentParser(
        description="Crypto Tools - CTF криптография",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --crack-hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5
  %(prog)s --caesar "KHOOR" --shift 3 --decrypt
  %(prog)s --caesar-bruteforce "KHOOR"
  %(prog)s --encode "Hello" --encoding base64
  %(prog)s --decode "SGVsbG8=" --encoding base64
  %(prog)s --rot13 "Uryyb"
        """
    )
    
    parser.add_argument('--crack-hash', metavar='HASH', help='Хеш для взлома')
    parser.add_argument('--type', choices=['md5', 'sha1', 'sha256', 'sha512'], 
                       default='md5', help='Тип хеша')
    parser.add_argument('--wordlist', help='Файл словаря для взлома')
    parser.add_argument('--max-length', type=int, default=6, help='Макс длина для брутфорса')
    
    parser.add_argument('--caesar', metavar='TEXT', help='Текст для шифра Цезаря')
    parser.add_argument('--shift', type=int, help='Сдвиг для шифра Цезаря')
    parser.add_argument('--decrypt', action='store_true', help='Дешифровать')
    parser.add_argument('--caesar-bruteforce', metavar='TEXT', help='Брутфорс шифра Цезаря')
    
    parser.add_argument('--rot13', metavar='TEXT', help='ROT13 шифрование/дешифрование')
    
    parser.add_argument('--vigenere', metavar='TEXT', help='Текст для шифра Виженера')
    parser.add_argument('--key', help='Ключ для шифра Виженера')
    
    parser.add_argument('--encode', metavar='TEXT', help='Текст для кодирования')
    parser.add_argument('--decode', metavar='TEXT', help='Текст для декодирования')
    parser.add_argument('--encoding', choices=['base64', 'base32', 'hex', 'url'],
                       help='Тип кодирования')
    
    parser.add_argument('--detect', metavar='TEXT', help='Определить тип кодирования')
    
    args = parser.parse_args()
    
    print_banner("CRYPTO TOOLS")
    
    # Взлом хеша
    if args.crack_hash:
        wordlist = None
        if args.wordlist:
            try:
                with open(args.wordlist, 'r') as f:
                    wordlist = f.readlines()
            except Exception as e:
                print_error(f"Ошибка чтения словаря: {e}")
        
        cracker = HashCracker()
        result = cracker.crack_hash(args.crack_hash, args.type, wordlist, args.max_length)
    
    # Шифр Цезаря
    elif args.caesar:
        if args.shift is None:
            print_error("Укажите сдвиг через --shift")
            sys.exit(1)
        result = CipherTools.caesar_cipher(args.caesar, args.shift, args.decrypt)
        print_success(f"Результат: {result}")
    
    # Брутфорс Цезаря
    elif args.caesar_bruteforce:
        results = CipherTools.caesar_bruteforce(args.caesar_bruteforce)
        print_info("Все возможные варианты:")
        for shift, text in results:
            print(f"Сдвиг {shift:2d}: {text}")
    
    # ROT13
    elif args.rot13:
        result = CipherTools.rot13(args.rot13)
        print_success(f"Результат: {result}")
    
    # Виженер
    elif args.vigenere:
        if not args.key:
            print_error("Укажите ключ через --key")
            sys.exit(1)
        result = CipherTools.vigenere_cipher(args.vigenere, args.key, args.decrypt)
        print_success(f"Результат: {result}")
    
    # Кодирование
    elif args.encode:
        if not args.encoding:
            print_error("Укажите тип кодирования через --encoding")
            sys.exit(1)
        
        encoders = {
            'base64': EncodingTools.encode_base64,
            'base32': EncodingTools.encode_base32,
            'hex': EncodingTools.encode_hex,
            'url': EncodingTools.url_encode
        }
        result = encoders[args.encoding](args.encode)
        print_success(f"{args.encoding.upper()}: {result}")
    
    # Декодирование
    elif args.decode:
        if not args.encoding:
            # Попытка автоопределения
            detected = EncodingTools.detect_encoding(args.decode)
            print_info(f"Обнаружено кодирование: {detected}")
        
        if not args.encoding:
            print_error("Укажите тип кодирования через --encoding")
            sys.exit(1)
        
        decoders = {
            'base64': EncodingTools.decode_base64,
            'base32': EncodingTools.decode_base32,
            'hex': EncodingTools.decode_hex,
            'url': EncodingTools.url_decode
        }
        result = decoders[args.encoding](args.decode)
        print_success(f"Декодировано: {result}")
    
    # Определение кодирования
    elif args.detect:
        encoding = EncodingTools.detect_encoding(args.detect)
        print_success(f"Обнаружено: {encoding}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()




