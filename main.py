
import sys
import argparse
from pathlib import Path
from decryptor import multi_restart_decryption, rus_alp

def get_optimal_params(text_length):
    
    if text_length < 200:
        return 12, 30000
    elif text_length < 500:
        return 10, 25000
    elif text_length < 1000:
        return 8, 20000
    elif text_length < 2000:
        return 7, 18000
    else:
        return 5, 15000

def read_encrypted_file(filepath):
    try:
        filepath = Path(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if not text:
            print(f"Файл пустой: {filepath}")
            return None
            
        print(f"загружено {len(text)} символов из {filepath.name}")
        return text
        
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return None
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None

def save_decrypted_file(text, filepath):
    try:
        filepath = Path(filepath)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Результат сохранен в {filepath}")
        return True
    
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False

def decrypt_file(input_file, output_file=None, restarts=None, iterations=None):

    encrypted_text = read_encrypted_file(input_file)
    if not encrypted_text:
        return False
    
    text_len = len([c for c in encrypted_text.lower() if c in rus_alp])
    print(f"Длина текста (русские буквы): {text_len}")
    
    if restarts is None or iterations is None:
        auto_restarts, auto_iterations = get_optimal_params(text_len)
        restarts = restarts or auto_restarts
        iterations = iterations or auto_iterations
        print(f"автоматически подобраны параметры: рестартов={restarts}, итераций={iterations}")
    else:
        print(f"используются указанные параметры: рестартов={restarts}, итераций={iterations}")
    
    print(f"\nИзначальный текст:")
    print(f"{encrypted_text[:150]}\n")
    
    print(f"{'-'*70}")
    print("НАЧАЛО РАСШИФРОВКИ")
    print(f"{'-'*70}\n")
    
    _, decrypted_text = multi_restart_decryption(
        encrypted_text,
        num_restarts=restarts,
        iterations=iterations
    )
    

    print(f"\n{'!'*70}")
    print("РЕЗУЛЬТАТ РАСШИФРОВКИ")
    print(f"{'!'*70}\n")
    print(decrypted_text)
    print(f"\n{'!'*70}\n")
    
    if output_file:
        save_decrypted_file(decrypted_text, output_file)
    
    return True

def main():
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

        print("-"*70)
        sys.exit(1)
    
    main()