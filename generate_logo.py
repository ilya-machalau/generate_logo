import os
from PIL import Image
import pillow_heif

# Регистрируем плагин HEIF для Pillow
pillow_heif.register_heif_opener()

def generate_image_file(format, size_mb, filename, approximate_resolution=(5000, 5000)):
    """
    Генерирует изображение заданного формата с шумным контентом,
    пытаясь приблизиться к указанному размеру файла.
    
    ВНИМАНИЕ: Размер может сильно отличаться от целевого из-за сжатия.
    Придется подбирать approximate_resolution экспериментально.
    """
    
    width, height = approximate_resolution
    
    # Создаем изображение с случайным шумом (RGB)
    # Изображение с шумом хуже всего сжимается, что помогает набрать объем.
    print(f"Генерация изображения {format} с разрешением {width}x{height}...")
    
    # Для растровых форматов
    if format.lower() in ['jpg', 'jpeg', 'png', 'webp', 'heic', 'heif']:
        try:
            # Создаем случайные пиксели. Это может быть медленно для больших разрешений.
            image_data = os.urandom(width * height * 3) # 3 байта на пиксель (RGB)
            img = Image.frombytes('RGB', (width, height), image_data)
            
            # Настройка параметров сохранения в зависимости от формата
            save_params = {}
            if format.lower() == 'jpg' or format.lower() == 'jpeg':
                save_params['quality'] = 100 # Максимальное качество
                save_params['optimize'] = False
            elif format.lower() == 'webp':
                save_params['quality'] = 100 # Максимальное качество
                save_params['lossless'] = True # Или без потерь для большего размера
            elif format.lower() in ['heic', 'heif']:
                # Для HEIC/HEIF через pillow-heif параметры могут отличаться.
                # Качество 100 обычно обеспечивает хороший размер.
                save_params['quality'] = 100

            # Пытаемся сохранить
            img.save(filename, format=format, **save_params)
            
        except MemoryError:
            print(f"Ошибка: Недостаточно памяти для создания изображения такого разрешения ({width}x{height}).")
            return
    
    # Для SVG (векторный формат)
    elif format.lower() == 'svg':
        # Создать файл SVG такого размера сложно программно, не создавая гигантское количество векторов.
        # Лучший способ - создать очень сложное векторное изображение.
        # Но для теста мы можем просто создать текстовый SVG файл с кучей путей/фигур.
        generate_large_svg(filename, size_mb)
        return

    else:
        print(f"Ошибка: Формат {format} не поддерживается этой функцией.")
        return

    # Проверка получившегося размера
    actual_size_bytes = os.path.getsize(filename)
    actual_size_mb = actual_size_bytes / (1024 * 1024)
    print(f"Файл {filename} создан. Размер: {actual_size_mb:.2f} МБ")
    print(f"Целевой размер: {size_mb} МБ. Разница: {(actual_size_mb - size_mb):.2f} МБ")
    
    if actual_size_mb < size_mb:
        print("СОВЕТ: Увеличьте `approximate_resolution` в коде для этого формата.")
    else:
        print("СОВЕТ: Уменьшите `approximate_resolution` в коде для этого формата.")


def generate_large_svg(filename, target_size_mb):
    """
    Создает файл SVG большого размера, добавляя кучу случайных путей.
    """
    target_size_bytes = target_size_mb * 1024 * 1024
    
    print(f"Генерация SVG файла (~{target_size_mb} МБ)...")
    
    with open(filename, 'w') as f:
        # Начало SVG файла
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1000" height="1000">\n')
        
        # Добавляем кучу случайных путей
        current_size = len('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1000" height="1000">\n')
        
        import random
        
        while current_size < target_size_bytes - 200: # Оставляем место для закрывающего тега
            # Генерируем случайный путь
            path_data = f'<path d="M {random.randint(0, 1000)} {random.randint(0, 1000)} L {random.randint(0, 1000)} {random.randint(0, 1000)} Q {random.randint(0, 1000)} {random.randint(0, 1000)} {random.randint(0, 1000)} {random.randint(0, 1000)} Z" stroke="rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})" fill="none" stroke-width="1"/>\n'
            f.write(path_data)
            current_size += len(path_data)
        
        # Закрывающий тег
        f.write('</svg>')
        
    actual_size_bytes = os.path.getsize(filename)
    actual_size_mb = actual_size_bytes / (1024 * 1024)
    print(f"Файл {filename} создан. Размер: {actual_size_mb:.2f} МБ")
    print(f"Целевой размер: {target_size_mb} МБ. Разница: {(actual_size_mb - target_size_mb):.2f} МБ")


# --- ИТОГОВАЯ ГЕНЕРАЦИЯ (Все файлы < 20 МБ) ---

print("\n=== Генерация финальных файлов до 20 МБ ===")

# Был 21.9 МБ при 2700 -> Уменьшаем до 2550
generate_image_file('PNG', 20, 'logo_final_20.png', approximate_resolution=(1920, 2550))

# Был 8.8 МБ при 2100 -> Увеличиваем до 3150
generate_image_file('JPEG', 20, 'logo_final_20.jpg', approximate_resolution=(1920, 2550))

# Был 7.7 МБ при 1600 -> Увеличиваем до 2550
generate_image_file('WEBP', 20, 'logo_final_20.webp', approximate_resolution=(1920, 2550))

# Был 22.5 МБ при 3800 -> Уменьшаем до 3500
generate_image_file('HEIF', 20, 'logo_final_20.heic', approximate_resolution=(1920, 2550))

# SVG: ставим цель 19 МБ для гарантии
generate_image_file('SVG', 19, 'logo_final_20.svg')

print("\n=== Негативный кейс (> 21 МБ) ===")
# Берем 2800 для уверенного превышения
generate_image_file('PNG', 21, 'logo_negative_21.png', approximate_resolution=(2800, 2800))