import random
from pathlib import Path

rus_alp = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
rus_alp_set = set(rus_alp)  

def generate_key():
    alph_list = list(rus_alp)
    random.shuffle(alph_list)
    key = "".join(alph_list)
    return key

def encrypt(text, key):
    zamena = {}
    for i, letter in enumerate(rus_alp):
        zamena[letter] = key[i]
    
    encrypt = []
    for char in text.lower():
        if char in zamena:
            encrypt.append(zamena[char])
        else:
            encrypt.append(char)
    
    return "".join(encrypt)

def count_frequencies(text):
    letter_count = {}
    total_letters = 0
    
    for char in text.lower():
        if char in rus_alp:
            letter_count[char] = letter_count.get(char, 0) + 1
            total_letters += 1
    
    frequencies = {}
    for letter, count in letter_count.items():
        frequencies[letter] = count / total_letters
    
    return frequencies

RUSSIAN_FREQ = {
    'о': 0.10983,  
    'е': 0.08483,
    'а': 0.07998,
    'и': 0.07367,
    'н': 0.06700,
    'т': 0.06318,
    'с': 0.05473,
    'р': 0.04746,
    'в': 0.04533,
    'л': 0.04343,
    'к': 0.03486,
    'м': 0.03203,
    'д': 0.02977,
    'п': 0.02804,
    'у': 0.02615,
    'я': 0.02001,
    'ы': 0.01898,
    'ь': 0.01735,
    'г': 0.01687,
    'з': 0.01641,
    'б': 0.01592,
    'ч': 0.01450,
    'й': 0.01208,
    'х': 0.00966,
    'ж': 0.00940,
    'ш': 0.00718,
    'ю': 0.00639,
    'ц': 0.00486,
    'щ': 0.00361,
    'э': 0.00331,
    'ф': 0.00267,
    'ъ': 0.00037,
    'ё': 0.00013
}

RUSSIAN_BIGRAMS = {
    'ст': 0.0234, 'но': 0.0210, 'ен': 0.0201, 'то': 0.0194, 'на': 0.0194,
    'ов': 0.0169, 'ни': 0.0166, 'ра': 0.0158, 'во': 0.0155, 'ко': 0.0154,
    'ро': 0.0144, 'ом': 0.0143, 'не': 0.0142, 'ан': 0.0138, 'ет': 0.0136,
    'та': 0.0135, 'ал': 0.0134, 'ол': 0.0132, 'ел': 0.0130, 'ли': 0.0129,
    'го': 0.0128, 'по': 0.0128, 'ин': 0.0127, 'ос': 0.0125, 'ва': 0.0124,
    'ор': 0.0123, 'ер': 0.0122, 'ри': 0.0122, 'ес': 0.0121, 'од': 0.0120,
    'от': 0.0119, 'ед': 0.0119, 'пр': 0.0118, 'те': 0.0118, 'ка': 0.0117,
    'ла': 0.0114, 'до': 0.0113, 'ил': 0.0111, 'ем': 0.0110, 'об': 0.0110,
    'ас': 0.0107, 'де': 0.0106, 'ре': 0.0105, 'ле': 0.0105, 'из': 0.0104,
    'ме': 0.0103, 'за': 0.0103, 'ог': 0.0102, 'ло': 0.0102, 'тр': 0.0101
}

RUSSIAN_WORDS_BASE = {
    'я', 'мы', 'он', 'она', 'они', 'это', 'тот', 'все', 'сам', 'там',
    'меня', 'мама', 'папа', 'дом', 'большой', 'большая', 'семья', 'человек',
    'сестра', 'брат', 'бабушка', 'дедушка', 'живем', 'вместе', 'собака',
    'кошка', 'встает', 'раньше', 'всех', 'потому', 'что', 'рано', 'работа',
    'работает', 'доктор', 'обычно', 'готовит', 'завтрак', 'обожаю',
    'каша', 'блины', 'после', 'идем', 'школа', 'учится', 'класс', 'пятый',
    'второй', 'любим', 'учиться', 'играть', 'друг', 'больше', 'всего',
    'люблю', 'география', 'когда', 'приходим', 'домой', 'смотрим',
    'телевизор', 'потом', 'ужинаем', 'делаем', 'урок', 'иногда', 'помогаем',
    'мама', 'огород', 'где', 'они', 'выращивают', 'овощи', 'фрукты',
    'деревня', 'овсяный', 'моя', 'мой', 'нам', 'есть', 'был', 'была', 'были',
    'программирование', 'программа', 'алгоритм', 'алгоритмы', 
    'структура', 'структуры', 'данные', 'код', 'функция',
    'изучаю', 'несколько', 'месяц', 'месяцев', 'очень', 'нравится',
    'особенно', 'интересный', 'интересны', 'сегодня', 'написал',
    'свой', 'свою', 'первый', 'первая', 'первую', 'для', 'расшифровка',
    'увлекательный', 'увлекательное', 'занятие', 'уже', 'мне'
}

def load_russian_dictionary():
    dictionary_path = Path(__file__).parent / 'russian_words.txt'
    
    try:
        print(f"Загрузка словаря из: {dictionary_path}")
        
        loaded_words = set()
        with open(dictionary_path, 'r', encoding='windows-1251') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    loaded_words.add(word)
        
        print(f"[OK] Загружено {len(loaded_words)} слов из файла")
        
        # Объединяем с базовым словарем
        all_words = loaded_words.union(RUSSIAN_WORDS_BASE)
        print(f"[OK] Всего слов в словаре: {len(all_words)}")
        
        return all_words
        
    except FileNotFoundError:
        print(f"[ERROR] Файл не найден: {dictionary_path}")
        print("Используется только базовый словарь, не рекомендуется!!!!!")
        return RUSSIAN_WORDS_BASE
        
    except Exception as e:
        print(f"[ERROR] Ошибка загрузки: {e}")
        print("Используется только базовый словарь, не рекомендуется!!!!!")
        return RUSSIAN_WORDS_BASE

RUSSIAN_WORDS = load_russian_dictionary()

def decrypt_with_key(encrypted_text, key_mapping):
    result = ""
    for char in encrypted_text.lower():
        decrypted_char = key_mapping.get(char, char)
        result += decrypted_char
    
    return result

def preprocess_text(text):
    clean_text = ''.join(c for c in text.lower() if c in rus_alp_set)
    
    words = text.lower().split()
    clean_words = [''.join(c for c in word if c in rus_alp_set) for word in words]
    
    return clean_text, clean_words

def score_text_fast(clean_text, clean_words):
    
    bigram_score = sum(
        RUSSIAN_BIGRAMS.get(clean_text[i:i+2], 0)
        for i in range(len(clean_text) - 1)
    )
    
    dict_score = sum(0.5 for word in clean_words if word in RUSSIAN_WORDS)
    
    final_score = bigram_score * 1.8 + dict_score * 1.5
    
    return final_score

def simple_frequency_attack(encrypted_text):

    encrypted_freq = count_frequencies(encrypted_text)

    encrypted_sorted = sorted(encrypted_freq.items(), key=lambda x: x[1], reverse=True)
    russian_sorted = sorted(RUSSIAN_FREQ.items(), key=lambda x: x[1], reverse=True)
    
    key_mapping = {}
    for i in range(min(len(encrypted_sorted), len(russian_sorted))):
        encrypted_letter = encrypted_sorted[i][0]
        russian_letter = russian_sorted[i][0]
        key_mapping[encrypted_letter] = russian_letter
    
    print("---замены---")
    for enc, rus in list(key_mapping.items())[:5]:  
        print(f"{enc} => {rus}")
    
    return key_mapping

def improved_hill_climbing(encrypted_text, initial_key, iterations=10000):

    current_key = initial_key.copy()  # Копируем словарь
    current_decrypted = decrypt_with_key(encrypted_text, current_key) # Расшифровываем текст с ключом
    clean_text, clean_words = preprocess_text(current_decrypted)
    current_score = score_text_fast(clean_text, clean_words)
    

    best_key = current_key.copy()
    best_score = current_score
    best_decrypted = current_decrypted
    
    print(f"Начальный score: {current_score:.3f}")
    
    improvements = 0
    stuck_counter = 0
    letters = list(current_key.keys()) # Список букв чтобы их случайно менять
    

    for iteration in range(iterations):
        letter1, letter2 = random.sample(letters, 2)
        
        current_key[letter1], current_key[letter2] = current_key[letter2], current_key[letter1]
        
        new_decrypted = decrypt_with_key(encrypted_text, current_key)
        clean_text, clean_words = preprocess_text(new_decrypted)
        new_score = score_text_fast(clean_text, clean_words)
        
        if new_score > current_score:
            current_score = new_score
            improvements += 1
            stuck_counter = 0
            
            if new_score > best_score:
                best_score = new_score
                best_key = current_key.copy()
                best_decrypted = new_decrypted
                
        else:
            current_key[letter1], current_key[letter2] = current_key[letter2], current_key[letter1]
            stuck_counter += 1
        

        if stuck_counter > 1000:         # перезапуск при застревании
            current_key = best_key.copy()
            
            for _ in range(5): #Тасуем ключ 5 раз, чтобы выйти из локального максимума
                letter1, letter2 = random.sample(letters, 2)
                current_key[letter1], current_key[letter2] = current_key[letter2], current_key[letter1]
            

            current_decrypted = decrypt_with_key(encrypted_text, current_key)
            clean_text, clean_words = preprocess_text(current_decrypted)
            current_score = score_text_fast(clean_text, clean_words)
            stuck_counter = 0
        

        if (iteration + 1) % 2000 == 0:
            print(f"итерация {iteration + 1}: best={best_score:.3f}, улучшений={improvements}")
    
    print(f"\n--------- ИТОГО ----------")
    print(f"Лучший score: {best_score:.4f}")
    print(f"Улучшений сделано: {improvements}")
    
    return best_key, best_decrypted

def multi_restart_decryption(encrypted_text, num_restarts=3, iterations=10000):

    
    print("--- Многократный запуск ---\n")
    
    best_overall_score = 0
    best_overall_key = None
    best_overall_text = None
    
    for restart in range(num_restarts):
        print(f"\n--- ЗАПУСК {restart + 1}/{num_restarts} ---")
        
        initial_key = simple_frequency_attack(encrypted_text)
        
        if restart > 0:
            letters = list(initial_key.keys())
            for _ in range(restart * 3):
                l1, l2 = random.sample(letters, 2)
                initial_key[l1], initial_key[l2] = initial_key[l2], initial_key[l1]
        

        key, text = improved_hill_climbing(encrypted_text, initial_key, iterations)
        
        clean_text, clean_words = preprocess_text(text)
        score = score_text_fast(clean_text, clean_words)
        
        print(f"Результат: score = {score:.3f}")
        
        if score > best_overall_score:
            best_overall_score = score
            best_overall_key = key
            best_overall_text = text
            print(f"  *** НОВЫЙ ЛУЧШИЙ! ***")
    
    print(f"\n{'-'*40}")
    print(f"ИТОГОВЫЙ РЕЗУЛЬТАТ: Score = {best_overall_score:.3f}")
    print(f"{'-'*40}\n")
    
    return best_overall_key, best_overall_text
