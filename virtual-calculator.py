import cv2
import numpy as np
import mediapipe as mp


class Button:
    def __init__(self, width, height, position, text):
        self.width = width
        self.height = height
        self.position = position
        self.text = text

    def clicked(self, x, y):
        # Попала ли точка в поле кнопки по оси х
        if self.position[0] < x < self.position[0] + self.width:
            # Попала ли точка в поле кнопки по оси y
            if self.position[1] < y < self.position[1] + self.height:
                return True, self.text
        return False, 0

    def draw(self, image):
        # Рисуем контур прямоугольника
        cv2.rectangle(image, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                      (25, 25, 25), 3)

        # Рисуем текст
        if self.text == "AC" or self.text == "DEL":
            cv2.putText(image, self.text, (self.position[0] + 75, self.position[1] + 35), cv2.FONT_HERSHEY_PLAIN, 2,
                        (25, 25, 25), 2)
        else:
            cv2.putText(image, self.text, (self.position[0] + 38, self.position[1] + 58), cv2.FONT_HERSHEY_PLAIN, 2,
                        (25, 25, 25), 2)


# Обычно камера имеет номер 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Кнопки
buttonsText = [['7', '4', '1', '0'],
               ['8', '5', '2', '.'],
               ['9', '6', '3', '/'],
               ['*', '-', '+', '=']]
buttons = []
for i in range(4):
    for j in range(4):
        x = i * 100 + 800
        y = j * 100 + 125
        buttons.append(Button(100, 100, (x, y), buttonsText[i][j]))

# Кнопка clear
x = 800
y = 525
buttons.append(Button(200, 50, (x, y), "AC"))

# Кнопка delete
x = 1000
y = 525
buttons.append(Button(200, 50, (x, y), "DEL"))

# Переменные
op = ""
delay = 0

# Создаем детектор
handsDetector = mp.solutions.hands.Hands(min_detection_confidence=0.1, max_num_hands=1)

while cap.isOpened():
    # Читаем очередной кадр
    ret, img = cap.read()
    # Переводим его в формат RGB для распознавания
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Отражаем горизонтально
    res_img = cv2.cvtColor(np.fliplr(img), cv2.COLOR_RGB2BGR)

    # Создание экрана калькулятора
    cv2.rectangle(res_img, (800, 25), (1200, 125), (25, 25, 25), 3)
    # cv2.rectangle(res_img, (800, 100), (1200, 200), (240, 248, 255), cv2.FILLED)

    # Распознаем руку
    results = handsDetector.process(res_img, )

    # Рисуем распознанное, если распозналось
    if results.multi_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(res_img,
                                                  results.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)

        # Координаты указательного пальца
        x8 = results.multi_hand_landmarks[0].landmark[8].x * img.shape[1]
        y8 = results.multi_hand_landmarks[0].landmark[8].y * img.shape[0]
        # Координаты среднего пальца
        x12 = results.multi_hand_landmarks[0].landmark[12].x * img.shape[1]
        y12 = results.multi_hand_landmarks[0].landmark[12].y * img.shape[0]

        # Расстояние между ними
        distance = int(np.hypot((x12 - x8), (y12 - y8)))
        if distance < 43:
            # Проверяем нажата ли кнопка и какая
            for button in buttons:
                ret = button.clicked(x8, y8)
                if ret[0] and delay == 0:
                    delay = 1
                    value = ret[1]
                    # Обрабатываем операции
                    if op == "Error" or op == "Size error":
                        op = ""
                    if value == '=':
                        try:
                            res = eval(op)
                        except:
                            op = "Error"
                        else:
                            if len(str(res)) > 12:
                                # Форматирование строки
                                try:
                                    sn = "{:.2e}".format(res)
                                except:
                                    op = "Size error"
                                else:
                                    n = len(sn[sn.index("e") + 1:])
                                    rounded = round(res, (9 - n))
                                    res = "{:e}".format(res)
                            op = str(res)
                    elif value == "AC":
                        op = ""
                    elif value == "DEL":
                        op = op[:-1]
                    else:
                        op += value
    # Рисование кнопок
    for button in buttons:
        button.draw(res_img)

    # Задержка
    if delay != 0:
        delay += 1
        if delay > 15:
            delay = 0

    # Вывод результата калькулятора
    if len(op) > 12:  # Смотрим, чтобы строка не выходила за рамку калькулятора
        cv2.putText(res_img, op[-12:], (810, 90), cv2.FONT_HERSHEY_PLAIN, 3, (25, 25, 25), 3)
    else:
        cv2.putText(res_img, op, (810, 90), cv2.FONT_HERSHEY_PLAIN, 3, (25, 25, 25), 3)
    print(op)

    # Задерживаем на 1 миллисекунду, ждем нажатия q
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break

    # Показываем изображение
    cv2.imshow("camera", res_img)

# Освобождаем ресурсы
handsDetector.close()
