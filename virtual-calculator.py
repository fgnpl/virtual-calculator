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
        # Рисуем контур прямоугольника
        cv2.rectangle(image, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                      (25, 25, 25), 3)

        # Заполянем цветом
        cv2.rectangle(image, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                      (199, 199, 199), cv2.FILLED)
        # Рисуем текст
        cv2.putText(image, self.text, (self.position[0] + 38, self.position[1] + 58), cv2.FONT_HERSHEY_PLAIN, 2,
                    (50, 50, 50), 2)


# Обычно камера имеет номер 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Кнопки
buttonsText = [['7', '4', '1', '0'],
               ['8', '5', '2', '/'],
               ['9', '6', '3', '.'],
               ['*', '-', '+', '=']]
buttons = []
for i in range(4):
    for j in range(4):
        x = i * 100 + 800
        y = j * 100 + 150
        buttons.append(Button(100, 100, (x, y), buttonsText[i][j]))

# Реализация калькулятора
op = ""

# Создаем детектор
handsDetector = mp.solutions.hands.Hands(min_detection_confidence=0.87, max_num_hands=1)

while cap.isOpened():
    # Читаем очередной кадр
    ret, img = cap.read()

    # Переводим его в формат RGB для распознавания
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Распознаем руку
    results = handsDetector.process(img,)

    # Рисуем распознанное, если распозналось
    if results.multi_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(img, results.multi_hand_landmarks[0])

    # Отражаем горизонтально, переводим в BGR и показываем результат
    res_img = cv2.cvtColor(np.fliplr(img), cv2.COLOR_RGB2BGR)

    # Создание экрана калькулятора
    cv2.rectangle(res_img, (800, 50), (1200, 170), (50, 50, 50), 3)
    cv2.rectangle(res_img, (800, 50), (1200, 170), (150, 150, 150), cv2.FILLED)

    # Рисование кнопок
    for button in buttons:
        button.draw(res_img)

    # Работа калькулятора

    # Вывод результата
    cv2.putText(res_img, op, (810, 110), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # Задерживаем на 1 миллисекунду, ждем нажатия q
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break

    # Показываем изображение
    cv2.imshow("camera", res_img)

# Освобождаем ресурсы
handsDetector.close()