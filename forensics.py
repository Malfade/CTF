#!/usr/bin/env python3
"""
Forensics Tools - Инструменты для форензики
"""

import os
import sys
import argparse
import hashlib
import magic
import binascii
from datetime import datetime
from typing import List, Dict, Optional
from utils import *

class FileAnalyzer:
    """Анализатор файлов"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        
        if not os.path.exists(filepath):
            print_error(f"Файл не найден: {filepath}")
            sys.exit(1)
    
    def get_file_hashes(self) -> Dict[str, str]:
        """Вычисление хешей файла"""
        print_info("Вычисление хешей...")
        
        hashes = {}
        algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        
        with open(self.filepath, 'rb') as f:
            data = f.read()
        
        for algo in algorithms:
            hasher = hashlib.new(algo)
            hasher.update(data)
            hashes[algo] = hasher.hexdigest()
            print_success(f"{algo.upper()}: {hashes[algo]}")
        
        return hashes
    
    def get_file_info(self) -> Dict:
        """Получение информации о файле"""
        print_info("Сбор информации о файле...")
        
        stats = os.stat(self.filepath)
        
        info = {
            'name': os.path.basename(self.filepath),
            'path': os.path.abspath(self.filepath),
            'size': stats.st_size,
            'created': datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'accessed': datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'mode': oct(stats.st_mode),
        }
        
        # Определение типа файла
        try:
            info['mime_type'] = magic.from_file(self.filepath, mime=True)
            info['file_type'] = magic.from_file(self.filepath)
        except:
            info['mime_type'] = 'unknown'
            info['file_type'] = 'unknown'
        
        print_success(f"Имя: {info['name']}")
        print_success(f"Размер: {info['size']} bytes")
        print_success(f"Тип: {info['file_type']}")
        print_success(f"MIME: {info['mime_type']}")
        print_success(f"Создан: {info['created']}")
        print_success(f"Изменен: {info['modified']}")
        
        return info
    
    def search_strings(self, min_length: int = 4, max_results: int = 100) -> List[str]:
        """Поиск читаемых строк в файле"""
        print_info(f"Поиск строк (минимум {min_length} символов)...")
        
        strings = []
        current_string = ""
        
        with open(self.filepath, 'rb') as f:
            data = f.read()
        
        for byte in data:
            if 32 <= byte <= 126:  # Печатаемые ASCII символы
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        
        # Последняя строка
        if len(current_string) >= min_length:
            strings.append(current_string)
        
        print_success(f"Найдено строк: {len(strings)}")
        
        # Показываем первые N результатов
        for i, s in enumerate(strings[:max_results]):
            print(f"  [{i+1}] {s}")
        
        if len(strings) > max_results:
            print_info(f"... и еще {len(strings) - max_results} строк")
        
        return strings
    
    def hex_dump(self, length: int = 256, offset: int = 0):
        """Hex dump файла"""
        print_info(f"Hex dump (offset: {offset}, length: {length})...")
        
        with open(self.filepath, 'rb') as f:
            f.seek(offset)
            data = f.read(length)
        
        for i in range(0, len(data), 16):
            hex_part = ' '.join(f'{b:02x}' for b in data[i:i+16])
            ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[i:i+16])
            print(f"{offset + i:08x}  {hex_part:<48}  {ascii_part}")
    
    def find_magic_bytes(self) -> List[Dict]:
        """Поиск магических байтов (сигнатур файлов)"""
        print_info("Поиск сигнатур файлов...")
        
        # Известные магические байты
        magic_bytes = {
            b'\x89PNG\r\n\x1a\n': 'PNG Image',
            b'\xff\xd8\xff': 'JPEG Image',
            b'GIF87a': 'GIF Image (87a)',
            b'GIF89a': 'GIF Image (89a)',
            b'PK\x03\x04': 'ZIP Archive',
            b'PK\x05\x06': 'ZIP Archive (empty)',
            b'Rar!\x1a\x07': 'RAR Archive',
            b'%PDF': 'PDF Document',
            b'\x7fELF': 'ELF Executable',
            b'MZ': 'PE Executable',
            b'<?xml': 'XML Document',
            b'#!/bin/bash': 'Bash Script',
            b'#!/bin/sh': 'Shell Script',
            b'#!/usr/bin/python': 'Python Script',
        }
        
        found = []
        
        with open(self.filepath, 'rb') as f:
            data = f.read()
        
        for magic, description in magic_bytes.items():
            if data.startswith(magic):
                found.append({'magic': magic.hex(), 'type': description, 'offset': 0})
                print_success(f"Обнаружено: {description} (magic: {magic.hex()})")
            
            # Поиск в файле
            offset = data.find(magic)
            if offset > 0:
                found.append({'magic': magic.hex(), 'type': description, 'offset': offset})
                print_warning(f"Найдено внутри: {description} на смещении {offset}")
        
        return found
    
    def entropy_analysis(self) -> float:
        """Анализ энтропии файла (для обнаружения шифрования/сжатия)"""
        print_info("Анализ энтропии...")
        
        import math
        from collections import Counter
        
        with open(self.filepath, 'rb') as f:
            data = f.read()
        
        if len(data) == 0:
            return 0.0
        
        # Подсчет частоты байтов
        byte_counts = Counter(data)
        entropy = 0
        
        for count in byte_counts.values():
            probability = count / len(data)
            entropy -= probability * math.log2(probability)
        
        print_success(f"Энтропия: {entropy:.4f}")
        
        if entropy > 7.5:
            print_warning("Высокая энтропия - возможно шифрование или сжатие!")
        elif entropy < 3.0:
            print_info("Низкая энтропия - вероятно текстовые данные")
        else:
            print_info("Средняя энтропия - смешанные данные")
        
        return entropy

class MemoryDumper:
    """Анализ дампов памяти"""
    
    @staticmethod
    def extract_strings_from_dump(dump_file: str, output_file: str, min_length: int = 6):
        """Извлечение строк из дампа памяти"""
        print_info(f"Извлечение строк из {dump_file}...")
        
        strings = []
        current_string = ""
        
        with open(dump_file, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                
                for byte in chunk:
                    if 32 <= byte <= 126:
                        current_string += chr(byte)
                    else:
                        if len(current_string) >= min_length:
                            strings.append(current_string)
                        current_string = ""
        
        # Сохранение результатов
        with open(output_file, 'w', encoding='utf-8') as f:
            for s in strings:
                f.write(s + '\n')
        
        print_success(f"Извлечено строк: {len(strings)}")
        print_success(f"Сохранено в: {output_file}")
        
        return strings
    
    @staticmethod
    def search_patterns(dump_file: str, patterns: List[bytes]) -> Dict:
        """Поиск паттернов в дампе"""
        print_info("Поиск паттернов...")
        
        results = {pattern: [] for pattern in patterns}
        
        with open(dump_file, 'rb') as f:
            data = f.read()
        
        for pattern in patterns:
            offset = 0
            while True:
                offset = data.find(pattern, offset)
                if offset == -1:
                    break
                results[pattern].append(offset)
                print_success(f"Найден паттерн {pattern.hex()} на смещении {offset}")
                offset += 1
        
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Forensics Tools - Инструменты форензики",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --analyze file.bin
  %(prog)s --file file.bin --hashes
  %(prog)s --file file.bin --strings --min-length 6
  %(prog)s --file file.bin --hex-dump --length 512
  %(prog)s --file file.bin --magic-bytes
  %(prog)s --file file.bin --entropy
        """
    )
    
    parser.add_argument('--file', required=True, help='Файл для анализа')
    parser.add_argument('--analyze', action='store_true', help='Полный анализ файла')
    parser.add_argument('--hashes', action='store_true', help='Вычислить хеши')
    parser.add_argument('--info', action='store_true', help='Информация о файле')
    parser.add_argument('--strings', action='store_true', help='Поиск строк')
    parser.add_argument('--min-length', type=int, default=4, help='Минимальная длина строки')
    parser.add_argument('--hex-dump', action='store_true', help='Hex dump')
    parser.add_argument('--length', type=int, default=256, help='Длина hex dump')
    parser.add_argument('--offset', type=int, default=0, help='Смещение для hex dump')
    parser.add_argument('--magic-bytes', action='store_true', help='Поиск магических байтов')
    parser.add_argument('--entropy', action='store_true', help='Анализ энтропии')
    parser.add_argument('--save', action='store_true', help='Сохранить результаты')
    
    args = parser.parse_args()
    
    print_banner("FORENSICS TOOLS")
    
    analyzer = FileAnalyzer(args.file)
    results = {}
    
    if args.analyze:
        # Полный анализ
        results['info'] = analyzer.get_file_info()
        results['hashes'] = analyzer.get_file_hashes()
        results['magic'] = analyzer.find_magic_bytes()
        results['entropy'] = analyzer.entropy_analysis()
        print()
        analyzer.hex_dump(length=256)
    
    elif args.hashes:
        results['hashes'] = analyzer.get_file_hashes()
    
    elif args.info:
        results['info'] = analyzer.get_file_info()
    
    elif args.strings:
        results['strings'] = analyzer.search_strings(args.min_length)
    
    elif args.hex_dump:
        analyzer.hex_dump(args.length, args.offset)
    
    elif args.magic_bytes:
        results['magic'] = analyzer.find_magic_bytes()
    
    elif args.entropy:
        results['entropy'] = analyzer.entropy_analysis()
    
    else:
        parser.print_help()
        sys.exit(0)
    
    if args.save and results:
        save_results(results, "forensics", "json")

if __name__ == "__main__":
    main()







