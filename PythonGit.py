import cv2 # type: ignore
import numpy as np # type: ignore

print("=" * 60)
print("🎨 ЗАПУСК ГЕНЕРАТОРА КАЛЕЙДОСКОПА")
print("=" * 60)

# Создаем тестовое изображение
print("\n⏳ Создание узора...")
size = 400
pattern = np.zeros((size, size, 3), dtype=np.uint8)

np.random.seed(42)
for i in range(50):
    color = (np.random.randint(0, 255), 
            np.random.randint(0, 255), 
            np.random.randint(0, 255))
    center = (np.random.randint(0, size), np.random.randint(0, size))
    radius = np.random.randint(10, 100)
    cv2.circle(pattern, center, radius, color, -1)

print("✅ Узор создан")

# Создаем калейдоскоп
print("⏳ Обработка калейдоскопа...")
h, w = pattern.shape[:2]
center = (w // 2, h // 2)
result = np.zeros_like(pattern)
segments = 8
sector_angle = 360 // segments

for i in range(segments):
    angle = i * sector_angle
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(pattern, M, (w, h))
    
    mask = np.zeros((h, w), dtype=np.uint8)
    pts = [center]
    for a in range(angle - sector_angle//2, angle + sector_angle//2 + 1, 5):
        rad = np.radians(a)
        x = int(center[0] + max(w, h) * np.cos(rad))
        y = int(center[1] + max(w, h) * np.sin(rad))
        pts.append((x, y))
    pts = np.array(pts, dtype=np.int32)
    cv2.fillPoly(mask, [pts], 255)
    
    result[mask == 255] = rotated[mask == 255]

print("✅ Калейдоскоп создан")

# Сохраняем
cv2.imwrite("kaleidoscope_output.png", result)
cv2.imwrite("original.png", pattern)

print("\n" + "=" * 60)
print("✅ ГОТОВО!")
print("=" * 60)
print("📁 Файлы сохранены:")
print("   • original.png")
print("   • kaleidoscope_output.png")
print("\n👉 Откройте файл kaleidoscope_output.png из папки!")
print("=" * 60)
