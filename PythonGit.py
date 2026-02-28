import cv2 # pyright: ignore[reportMissingImports]
import numpy as np # pyright: ignore[reportMissingImports]

def advanced_kaleidoscope(image_path, num_segments=6, output_path='advanced_kaleido.jpg'):
    """
    Создает калейдоскоп с автоматическим определением центра по границам.
    """
    img = cv2.imread(image_path)
    if img is None:
        print("Ошибка загрузки изображения")
        return
    
    height, width = img.shape[:2]
    
    # 1. Определяем область с наибольшей концентрацией границ
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Скользящее окно 11x11 для поиска максимума границ [citation:2]
    window_size = 11
    max_edges = 0
    best_center = (width // 2, height // 2)
    
    for y in range(0, height - window_size, window_size):
        for x in range(0, width - window_size, window_size):
            window = edges[y:y+window_size, x:x+window_size]
            edge_count = np.sum(window)
            if edge_count > max_edges:
                max_edges = edge_count
                best_center = (x + window_size//2, y + window_size//2)
    
    # 2. Смещаем изображение так, чтобы центр оказался в центре кадра
    M = np.float32([[1, 0, width//2 - best_center[0]],
                    [0, 1, height//2 - best_center[1]]])
    centered = cv2.warpAffine(img, M, (width, height))
    
    # 3. Создаем треугольный сегмент
    center = (width // 2, height // 2)
    angle_step = 360 // num_segments
    
    # Маска для одного сегмента (60° для 6 сегментов)
    mask = np.zeros((height, width), dtype=np.uint8)
    triangle_points = np.array([
        center,
        (width, height),
        (width, 0)
    ], np.int32)
    cv2.fillPoly(mask, [triangle_points], 255)
    
    # 4. Вырезаем сегмент и создаем вращающиеся копии
    segment = cv2.bitwise_and(centered, centered, mask=mask)
    
    kaleidoscope = np.zeros_like(img)
    for i in range(num_segments):
        M_rot = cv2.getRotationMatrix2D(center, i * angle_step, 1.0)
        rotated = cv2.warpAffine(segment, M_rot, (width, height))
        kaleidoscope = cv2.add(kaleidoscope, rotated)
    
    cv2.imwrite(output_path, kaleidoscope)
    cv2.imshow('Advanced Kaleidoscope', kaleidoscope)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Использование
advanced_kaleidoscope('input.jpg', num_segments=8)
