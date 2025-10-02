#!/usr/bin/env python3
"""
Steganography Tools - Инструменты стеганографии
"""

import argparse
import sys
from PIL import Image
import os
from utils import *

class ImageSteganography:
    """Стеганография в изображениях"""
    
    @staticmethod
    def text_to_binary(text: str) -> str:
        """Конвертация текста в бинарный формат"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def binary_to_text(binary: str) -> str:
        """Конвертация бинарных данных в текст"""
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)
    
    @staticmethod
    def hide_text_in_image(image_path: str, secret_text: str, output_path: str):
        """Скрытие текста в изображении (LSB метод)"""
        print_info(f"Скрытие текста в {image_path}...")
        
        try:
            # Открываем изображение
            img = Image.open(image_path)
            img = img.convert('RGB')
            pixels = list(img.getdata())
            
            # Добавляем маркер конца сообщения
            secret_text += "<<<END>>>"
            binary_secret = ImageSteganography.text_to_binary(secret_text)
            
            # Проверка размера
            if len(binary_secret) > len(pixels) * 3:
                print_error("Изображение слишком маленькое для сообщения")
                return False
            
            # Встраиваем данные в младшие биты
            data_index = 0
            new_pixels = []
            
            for pixel in pixels:
                if data_index < len(binary_secret):
                    r, g, b = pixel
                    
                    # Изменяем младший бит каждого канала
                    if data_index < len(binary_secret):
                        r = (r & 0xFE) | int(binary_secret[data_index])
                        data_index += 1
                    if data_index < len(binary_secret):
                        g = (g & 0xFE) | int(binary_secret[data_index])
                        data_index += 1
                    if data_index < len(binary_secret):
                        b = (b & 0xFE) | int(binary_secret[data_index])
                        data_index += 1
                    
                    new_pixels.append((r, g, b))
                else:
                    new_pixels.append(pixel)
            
            # Создаем новое изображение
            stego_img = Image.new('RGB', img.size)
            stego_img.putdata(new_pixels)
            stego_img.save(output_path)
            
            print_success(f"Текст скрыт в {output_path}")
            print_info(f"Размер сообщения: {len(secret_text)} символов")
            return True
            
        except Exception as e:
            print_error(f"Ошибка: {e}")
            return False
    
    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """Извлечение текста из изображения (LSB метод)"""
        print_info(f"Извлечение текста из {image_path}...")
        
        try:
            img = Image.open(image_path)
            img = img.convert('RGB')
            pixels = list(img.getdata())
            
            # Извлекаем младшие биты
            binary_data = ""
            for pixel in pixels:
                r, g, b = pixel
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)
            
            # Конвертируем в текст
            text = ""
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                if len(byte) == 8:
                    char = chr(int(byte, 2))
                    text += char
                    
                    # Проверка маркера конца
                    if text.endswith("<<<END>>>"):
                        text = text[:-9]  # Удаляем маркер
                        print_success("Текст извлечен")
                        return text
            
            print_warning("Маркер конца не найден, возможно изображение не содержит скрытого сообщения")
            return text[:200]  # Возвращаем первые 200 символов
            
        except Exception as e:
            print_error(f"Ошибка: {e}")
            return ""
    
    @staticmethod
    def analyze_image(image_path: str):
        """Анализ изображения на наличие стеганографии"""
        print_info(f"Анализ {image_path}...")
        
        try:
            img = Image.open(image_path)
            
            print_success(f"Формат: {img.format}")
            print_success(f"Режим: {img.mode}")
            print_success(f"Размер: {img.size}")
            print_success(f"Размер файла: {os.path.getsize(image_path)} bytes")
            
            # Проверка метаданных
            if hasattr(img, '_getexif') and img._getexif():
                print_warning("Обнаружены EXIF данные")
                exif = img._getexif()
                for tag_id, value in exif.items():
                    print_info(f"  {tag_id}: {value}")
            
            # Статистический анализ LSB
            img_rgb = img.convert('RGB')
            pixels = list(img_rgb.getdata())
            
            lsb_analysis = {'0': 0, '1': 0}
            for pixel in pixels[:1000]:  # Анализируем первые 1000 пикселей
                r, g, b = pixel
                lsb_analysis[str(r & 1)] += 1
                lsb_analysis[str(g & 1)] += 1
                lsb_analysis[str(b & 1)] += 1
            
            total = lsb_analysis['0'] + lsb_analysis['1']
            ratio_0 = lsb_analysis['0'] / total * 100
            ratio_1 = lsb_analysis['1'] / total * 100
            
            print_info(f"LSB статистика (первые 1000 пикселей):")
            print_info(f"  0: {ratio_0:.2f}%")
            print_info(f"  1: {ratio_1:.2f}%")
            
            # Если распределение близко к 50/50, возможна стеганография
            if 45 <= ratio_0 <= 55:
                print_warning("Распределение LSB подозрительное - возможна стеганография!")
            else:
                print_success("LSB распределение выглядит нормально")
            
        except Exception as e:
            print_error(f"Ошибка анализа: {e}")

class FileSteganography:
    """Стеганография в файлах"""
    
    @staticmethod
    def hide_file_in_image(image_path: str, secret_file: str, output_path: str):
        """Скрытие файла в изображении"""
        print_info(f"Скрытие {secret_file} в {image_path}...")
        
        try:
            # Читаем секретный файл
            with open(secret_file, 'rb') as f:
                secret_data = f.read()
            
            # Кодируем в base64 для безопасности
            import base64
            encoded_data = base64.b64encode(secret_data).decode()
            
            # Используем метод скрытия текста
            success = ImageSteganography.hide_text_in_image(
                image_path, 
                f"<<<FILE:{os.path.basename(secret_file)}>>>{encoded_data}",
                output_path
            )
            
            if success:
                print_success(f"Файл скрыт в {output_path}")
            
            return success
            
        except Exception as e:
            print_error(f"Ошибка: {e}")
            return False
    
    @staticmethod
    def extract_file_from_image(image_path: str, output_dir: str = "."):
        """Извлечение файла из изображения"""
        print_info(f"Извлечение файла из {image_path}...")
        
        try:
            # Извлекаем данные
            data = ImageSteganography.extract_text_from_image(image_path)
            
            # Проверяем маркер файла
            if data.startswith("<<<FILE:"):
                end_marker = data.index(">>>")
                filename = data[8:end_marker]
                encoded_data = data[end_marker + 3:]
                
                # Декодируем из base64
                import base64
                file_data = base64.b64decode(encoded_data)
                
                # Сохраняем файл
                output_path = os.path.join(output_dir, filename)
                with open(output_path, 'wb') as f:
                    f.write(file_data)
                
                print_success(f"Файл извлечен: {output_path}")
                return output_path
            else:
                print_warning("Маркер файла не найден")
                return None
                
        except Exception as e:
            print_error(f"Ошибка: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(
        description="Steganography Tools - CTF стеганография",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --hide-text image.png "Secret message" output.png
  %(prog)s --extract-text stego.png
  %(prog)s --analyze image.png
  %(prog)s --hide-file image.png secret.txt output.png
  %(prog)s --extract-file stego.png
        """
    )
    
    parser.add_argument('--hide-text', metavar=('IMAGE', 'TEXT', 'OUTPUT'), nargs=3,
                       help='Скрыть текст в изображении')
    parser.add_argument('--extract-text', metavar='IMAGE', help='Извлечь текст из изображения')
    parser.add_argument('--analyze', metavar='IMAGE', help='Анализ изображения')
    parser.add_argument('--hide-file', metavar=('IMAGE', 'FILE', 'OUTPUT'), nargs=3,
                       help='Скрыть файл в изображении')
    parser.add_argument('--extract-file', metavar='IMAGE', help='Извлечь файл из изображения')
    parser.add_argument('--output-dir', default='.', help='Директория для извлеченных файлов')
    
    args = parser.parse_args()
    
    print_banner("STEGANOGRAPHY TOOLS")
    
    if args.hide_text:
        image, text, output = args.hide_text
        ImageSteganography.hide_text_in_image(image, text, output)
    
    elif args.extract_text:
        text = ImageSteganography.extract_text_from_image(args.extract_text)
        if text:
            print(f"\n{Colors.SUCCESS}Извлеченный текст:{Colors.RESET}")
            print(text)
    
    elif args.analyze:
        ImageSteganography.analyze_image(args.analyze)
    
    elif args.hide_file:
        image, file, output = args.hide_file
        FileSteganography.hide_file_in_image(image, file, output)
    
    elif args.extract_file:
        FileSteganography.extract_file_from_image(args.extract_file, args.output_dir)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()







