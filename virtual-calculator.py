import cv2
import numpy as np
import mediapipe as mp


class Button:
    def __init__(self, width, height, position, text):
        self.width = width
        self.height = height
        self.position = position
        self.text = text

    def draw(self, image):
        cv2.rectangle(image, self.position, (self.position[0] + self.width, self.position[1] + self.height))


# Обычно камера имеет номер 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Создаем детектор
handsDetector = mp.solutions.hands.Hands(min_detection_confidence=0.87, max_num_hands=1)

while cap.isOpened():
    # Читаем очередной кадр
    ret, img = cap.read()

    # Переворачиваем для удобства использования
    img = cv2.flip(img, 1)

    # Переводим его в формат RGB для распознавания
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Распознаем руку
    results = handsDetector.process(img,)

    # Рисуем распознанное, если распозналось
    if results.multi_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(img, results.multi_hand_landmarks[0])

    # Отражаем обратно, переводим в BGR и показываем результат
    res_img = cv2.cvtColor(np.fliplr(img), cv2.COLOR_RGB2BGR)

    # Задерживаем на 1 миллисекунду, ждем нажатия q
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break

    # Показываем изображение
    cv2.imshow("camera", res_img)

# Освобождаем ресурсы
handsDetector.close()
