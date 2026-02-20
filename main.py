# main.py

import sys
import argparse
from pathlib import Path
from decryptor import multi_restart_decryption, rus_alp

def get_optimal_params(text_length):
    """
    Возвращает оптимальные параметры (restarts, iterations) в зависимости от длины текста.
    Значения подобраны эмпирически для гарантированного качества.
    """
    if text_length < 200:
        # Очень короткий текст – нужно больше попыток, так как мало статистики
        return 12, 30000
    elif text_length < 500:
        # Короткий текст
        return 10, 25000
    elif text_length < 1000:
        # Средний текст
        return 8, 20000
    elif text_length < 2000:
        # Длинный текст
        return 7, 18000
    else:
        # Очень длинный текст (статистики много, можно немного уменьшить число рестартов)
        return 5, 15000

def read_encrypted_file(filepath):
    """Читает зашифрованный текст из файла"""
    try:
        filepath = Path(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            print(f"[ERROR] Файл пустой: {filepath}")
            return None
            
        print(f"[OK] Загружено {len(text)} символов из {filepath.name}")
        return text
        
    except FileNotFoundError:
        print(f"[ERROR] Файл не найден: {filepath}")
        return None
    except UnicodeDecodeError:
        print(f"[ERROR] Ошибка кодировки файла. Попробуйте сохранить в UTF-8")
        return None
    except Exception as e:
        print(f"[ERROR] Ошибка чтения файла: {e}")
        return None

def save_decrypted_file(text, filepath):
    """Сохраняет расшифрованный текст в файл"""
    try:
        filepath = Path(filepath)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"[OK] Результат сохранен в {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Ошибка сохранения: {e}")
        return False

def decrypt_file(input_file, output_file=None, restarts=None, iterations=None):
    """
    Главная функция расшифровки
    
    Args:
        input_file: путь к файлу с зашифрованным текстом
        output_file: путь для сохранения результата (опционально)
        restarts: количество рестартов (если None, выбирается автоматически)
        iterations: количество итераций (если None, выбирается автоматически)
    """
    # Читаем зашифрованный текст
    encrypted_text = read_encrypted_file(input_file)
    
    if not encrypted_text:
        return False
    
    # Вычисляем длину текста (только русские буквы)
    text_len = len([c for c in encrypted_text.lower() if c in rus_alp])
    print(f"[INFO] Длина текста (русские буквы): {text_len}")
    
    # Определяем параметры
    if restarts is None or iterations is None:
        auto_restarts, auto_iterations = get_optimal_params(text_len)
        restarts = restarts or auto_restarts
        iterations = iterations or auto_iterations
        print(f"[INFO] Автоматически подобраны параметры: рестартов={restarts}, итераций={iterations}")
    else:
        print(f"[INFO] Используются указанные параметры: рестартов={restarts}, итераций={iterations}")
    
    # Показываем фрагмент
    print(f"\nЗашифрованный текст (первые 150 символов):")
    print(f"  {encrypted_text[:150]}{'...' if len(encrypted_text) > 150 else ''}\n")
    
    # Расшифровываем
    print(f"{'='*70}")
    print("НАЧАЛО РАСШИФРОВКИ")
    print(f"{'='*70}\n")
    
    _, decrypted_text = multi_restart_decryption(
        encrypted_text,
        num_restarts=restarts,
        iterations=iterations
    )
    
    # Выводим результат
    print(f"\n{'='*70}")
    print("РЕЗУЛЬТАТ РАСШИФРОВКИ")
    print(f"{'='*70}\n")
    print(decrypted_text)
    print(f"\n{'='*70}\n")
    
    # Сохраняем если указан выходной файл
    if output_file:
        save_decrypted_file(decrypted_text, output_file)
    
    return True

def main():
    """Главная функция с парсингом аргументов"""
    parser = argparse.ArgumentParser(
        description='Расшифровка текстов, зашифрованных методом простой замены',
        epilog='Пример: python main.py encrypted.txt -o result.txt'
    )
    
    parser.add_argument(
        'input',
        help='Путь к файлу с зашифрованным текстом'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Путь для сохранения расшифрованного текста (необязательно)',
        default=None
    )
    
    parser.add_argument(
        '--restarts',
        type=int,
        help='Количество рестартов (если не указано, выбирается автоматически)',
        default=None
    )
    
    parser.add_argument(
        '--iterations',
        type=int,
        help='Количество итераций hill climbing (если не указано, выбирается автоматически)',
        default=None
    )
    
    args = parser.parse_args()
    
    success = decrypt_file(args.input, args.output, args.restarts, args.iterations)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("="*70)
        print("  ДЕШИФРАТОР - Расшифровка методом простой замены")
        print("="*70)
        print("\nИспользование:")
        print("  python main.py <входной_файл> [-o <выходной_файл>] [--restarts N] [--iterations M]")
        print("\nПримеры:")
        print("  python main.py encrypted.txt")
        print("  python main.py encrypted.txt -o decrypted.txt")
        print("  python main.py encrypted.txt --restarts 10 --iterations 20000")
        print("\nДля справки:")
        print("  python main.py --help")
        print("="*70)
        sys.exit(1)
    
    main()