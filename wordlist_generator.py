#!/usr/bin/env python3
"""
Wordlist Generator - Генератор словарей для брутфорса
"""

import argparse
import sys
import itertools
import string
from typing import List
from utils import *

class WordlistGenerator:
    """Генератор словарей"""
    
    def __init__(self):
        self.wordlist = []
    
    def generate_numeric(self, min_length: int, max_length: int) -> List[str]:
        """Генерация числовых комбинаций"""
        print_info(f"Генерация числовых комбинаций ({min_length}-{max_length} символов)...")
        
        words = []
        for length in range(min_length, max_length + 1):
            for combo in itertools.product(string.digits, repeat=length):
                words.append(''.join(combo))
        
        print_success(f"Сгенерировано: {len(words)} вариантов")
        return words
    
    def generate_alpha(self, min_length: int, max_length: int, case: str = 'lower') -> List[str]:
        """Генерация буквенных комбинаций"""
        print_info(f"Генерация буквенных комбинаций ({min_length}-{max_length} символов)...")
        
        if case == 'lower':
            chars = string.ascii_lowercase
        elif case == 'upper':
            chars = string.ascii_uppercase
        else:  # mixed
            chars = string.ascii_letters
        
        words = []
        for length in range(min_length, max_length + 1):
            print_info(f"Длина {length}...")
            for combo in itertools.product(chars, repeat=length):
                words.append(''.join(combo))
                if len(words) % 100000 == 0:
                    print(f"  Сгенерировано: {len(words)}", end='\r')
        
        print()
        print_success(f"Сгенерировано: {len(words)} вариантов")
        return words
    
    def generate_alphanumeric(self, min_length: int, max_length: int) -> List[str]:
        """Генерация алфавитно-числовых комбинаций"""
        print_info(f"Генерация алфавитно-числовых комбинаций ({min_length}-{max_length} символов)...")
        
        chars = string.ascii_lowercase + string.digits
        words = []
        
        for length in range(min_length, max_length + 1):
            print_info(f"Длина {length}...")
            for combo in itertools.product(chars, repeat=length):
                words.append(''.join(combo))
                if len(words) % 100000 == 0:
                    print(f"  Сгенерировано: {len(words)}", end='\r')
        
        print()
        print_success(f"Сгенерировано: {len(words)} вариантов")
        return words
    
    def generate_custom(self, charset: str, min_length: int, max_length: int) -> List[str]:
        """Генерация с пользовательским набором символов"""
        print_info(f"Генерация с charset: {charset} ({min_length}-{max_length} символов)...")
        
        words = []
        for length in range(min_length, max_length + 1):
            print_info(f"Длина {length}...")
            for combo in itertools.product(charset, repeat=length):
                words.append(''.join(combo))
                if len(words) % 100000 == 0:
                    print(f"  Сгенерировано: {len(words)}", end='\r')
        
        print()
        print_success(f"Сгенерировано: {len(words)} вариантов")
        return words
    
    def generate_from_pattern(self, pattern: str) -> List[str]:
        """
        Генерация по паттерну
        @@ = буква нижнего регистра
        @# = цифра
        @? = любой символ
        @! = специальный символ
        """
        print_info(f"Генерация по паттерну: {pattern}")
        
        # Заменяем паттерны на наборы символов
        pattern_parts = []
        i = 0
        while i < len(pattern):
            if i < len(pattern) - 1 and pattern[i] == '@':
                if pattern[i+1] == '@':
                    pattern_parts.append(string.ascii_lowercase)
                    i += 2
                elif pattern[i+1] == '#':
                    pattern_parts.append(string.digits)
                    i += 2
                elif pattern[i+1] == '?':
                    pattern_parts.append(string.ascii_lowercase + string.digits)
                    i += 2
                elif pattern[i+1] == '!':
                    pattern_parts.append('!@#$%^&*')
                    i += 2
                else:
                    pattern_parts.append([pattern[i]])
                    i += 1
            else:
                pattern_parts.append([pattern[i]])
                i += 1
        
        # Генерация комбинаций
        words = []
        for combo in itertools.product(*pattern_parts):
            words.append(''.join(combo))
        
        print_success(f"Сгенерировано: {len(words)} вариантов")
        return words
    
    def generate_common_passwords(self) -> List[str]:
        """Генерация популярных паролей"""
        print_info("Генерация популярных паролей...")
        
        common = [
            'password', 'Password', 'PASSWORD', 'Password123',
            '123456', '12345678', '123456789',
            'qwerty', 'QWERTY', 'qwerty123',
            'admin', 'Admin', 'administrator',
            'root', 'toor',
            'letmein', 'welcome', 'monkey',
            'dragon', 'master', 'sunshine',
            'princess', 'football', 'shadow',
        ]
        
        # Добавляем вариации с годами
        years = [str(y) for y in range(2000, 2026)]
        variations = []
        
        for pwd in common:
            variations.append(pwd)
            for year in years:
                variations.append(f"{pwd}{year}")
                variations.append(f"{pwd}!{year}")
                variations.append(f"{pwd}_{year}")
        
        print_success(f"Сгенерировано: {len(variations)} вариантов")
        return variations
    
    def apply_rules(self, base_words: List[str]) -> List[str]:
        """Применение правил к базовым словам (leet speak, suffixes)"""
        print_info("Применение правил трансформации...")
        
        result = list(base_words)  # Копируем оригиналы
        
        leet_map = {
            'a': ['a', '4', '@'],
            'e': ['e', '3'],
            'i': ['i', '1', '!'],
            'o': ['o', '0'],
            's': ['s', '5', '$'],
            't': ['t', '7'],
            'l': ['l', '1'],
        }
        
        suffixes = ['', '!', '123', '1', '2', '12', '2024', '2025']
        
        for word in base_words:
            # Leet speak
            word_lower = word.lower()
            for char, replacements in leet_map.items():
                if char in word_lower:
                    for replacement in replacements[1:]:  # Пропускаем оригинал
                        leet_word = word_lower.replace(char, replacement)
                        result.append(leet_word)
                        result.append(leet_word.capitalize())
            
            # Suffixes
            for suffix in suffixes[1:]:  # Пропускаем пустой
                result.append(word + suffix)
                result.append(word.capitalize() + suffix)
        
        # Удаляем дубликаты
        result = list(set(result))
        
        print_success(f"После трансформаций: {len(result)} вариантов")
        return result
    
    def save_wordlist(self, words: List[str], filename: str):
        """Сохранение словаря в файл"""
        try:
            output_dir = "wordlists"
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for word in words:
                    f.write(word + '\n')
            
            print_success(f"Словарь сохранен: {filepath}")
            print_info(f"Размер: {len(words)} строк, {os.path.getsize(filepath)} bytes")
            
        except Exception as e:
            print_error(f"Ошибка сохранения: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Wordlist Generator - Генератор словарей",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --numeric --min 4 --max 6 -o pins.txt
  %(prog)s --alpha --min 3 --max 5 --case lower -o words.txt
  %(prog)s --alphanumeric --min 4 --max 4 -o passwords.txt
  %(prog)s --custom "abc123" --min 3 --max 4 -o custom.txt
  %(prog)s --pattern "@@@@####" -o pattern.txt
  %(prog)s --common -o common_passwords.txt
  %(prog)s --common --apply-rules -o common_variations.txt

Паттерны:
  @@ = буква (a-z)
  @# = цифра (0-9)
  @? = буква или цифра
  @! = специальный символ
        """
    )
    
    parser.add_argument('--numeric', action='store_true', help='Числовой словарь')
    parser.add_argument('--alpha', action='store_true', help='Буквенный словарь')
    parser.add_argument('--alphanumeric', action='store_true', help='Алфавитно-числовой словарь')
    parser.add_argument('--custom', metavar='CHARSET', help='Пользовательский набор символов')
    parser.add_argument('--pattern', metavar='PATTERN', help='Генерация по паттерну')
    parser.add_argument('--common', action='store_true', help='Популярные пароли')
    
    parser.add_argument('--min', type=int, default=1, help='Минимальная длина')
    parser.add_argument('--max', type=int, default=4, help='Максимальная длина')
    parser.add_argument('--case', choices=['lower', 'upper', 'mixed'], 
                       default='lower', help='Регистр букв')
    
    parser.add_argument('--apply-rules', action='store_true', 
                       help='Применить правила трансформации')
    
    parser.add_argument('-o', '--output', required=True, help='Файл для сохранения')
    
    args = parser.parse_args()
    
    print_banner("WORDLIST GENERATOR")
    
    generator = WordlistGenerator()
    words = []
    
    # Предупреждение о больших словарях
    if args.max > 6 and not args.numeric:
        print_warning("ВНИМАНИЕ: Большая длина может создать огромный файл!")
        if not get_user_confirmation("Продолжить?"):
            sys.exit(0)
    
    # Генерация
    if args.numeric:
        words = generator.generate_numeric(args.min, args.max)
    
    elif args.alpha:
        words = generator.generate_alpha(args.min, args.max, args.case)
    
    elif args.alphanumeric:
        words = generator.generate_alphanumeric(args.min, args.max)
    
    elif args.custom:
        words = generator.generate_custom(args.custom, args.min, args.max)
    
    elif args.pattern:
        words = generator.generate_from_pattern(args.pattern)
    
    elif args.common:
        words = generator.generate_common_passwords()
    
    else:
        print_error("Выберите тип генерации!")
        parser.print_help()
        sys.exit(1)
    
    # Применение правил
    if args.apply_rules and words:
        words = generator.apply_rules(words)
    
    # Сохранение
    if words:
        generator.save_wordlist(words, args.output)
    else:
        print_error("Словарь пуст!")

if __name__ == "__main__":
    main()







