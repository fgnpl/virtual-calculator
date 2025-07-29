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
        # Check if point is within button's x-axis bounds
        if self.position[0] < x < self.position[0] + self.width:
            # Check if point is within button's y-axis bounds
            if self.position[1] < y < self.position[1] + self.height:
                return True, self.text
        return False, 0

    def draw(self, image):
        # Draw rectangle outline
        cv2.rectangle(image, self.position, (self.position[0] + self.width, self.position[1] + self.height),
                      (25, 25, 25), 3)

        # Draw text
        if self.text == "AC" or self.text == "DEL":
            cv2.putText(image, self.text, (self.position[0] + 75, self.position[1] + 35), cv2.FONT_HERSHEY_PLAIN, 2,
                        (25, 25, 25), 2)
        else:
            cv2.putText(image, self.text, (self.position[0] + 38, self.position[1] + 58), cv2.FONT_HERSHEY_PLAIN, 2,
                        (25, 25, 25), 2)


# Typically camera has index 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Buttons
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

# Clear button
x = 800
y = 525
buttons.append(Button(200, 50, (x, y), "AC"))

# Delete button
x = 1000
y = 525
buttons.append(Button(200, 50, (x, y), "DEL"))

# Variables
op = ""
delay = 0

# Create detector
handsDetector = mp.solutions.hands.Hands(min_detection_confidence=0.1, max_num_hands=1)

while cap.isOpened():
    # Read next frame
    ret, img = cap.read()
    # Convert to RGB format for recognition
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Flip horizontally
    res_img = cv2.cvtColor(np.fliplr(img), cv2.COLOR_RGB2BGR)

    # Create calculator screen
    cv2.rectangle(res_img, (800, 25), (1200, 125), (25, 25, 25), 3)
    # cv2.rectangle(res_img, (800, 100), (1200, 200), (240, 248, 255), cv2.FILLED)

    # Detect hand
    results = handsDetector.process(res_img, )

    # Draw detection if successful
    if results.multi_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(res_img,
                                                  results.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)

        # Index finger coordinates
        x8 = results.multi_hand_landmarks[0].landmark[8].x * img.shape[1]
        y8 = results.multi_hand_landmarks[0].landmark[8].y * img.shape[0]
        # Middle finger coordinates
        x12 = results.multi_hand_landmarks[0].landmark[12].x * img.shape[1]
        y12 = results.multi_hand_landmarks[0].landmark[12].y * img.shape[0]

        # Distance between fingers
        distance = int(np.hypot((x12 - x8), (y12 - y8)))
        if distance < 43:
            # Check which button is pressed
            for button in buttons:
                ret = button.clicked(x8, y8)
                if ret[0] and delay == 0:
                    delay = 1
                    value = ret[1]
                    # Process operations
                    if op == "Error" or op == "Size error":
                        op = ""
                    if value == '=':
                        try:
                            res = eval(op)
                        except:
                            op = "Error"
                        else:
                            if len(str(res)) > 12:
                                # String formatting
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
    # Draw buttons
    for button in buttons:
        button.draw(res_img)

    # Delay
    if delay != 0:
        delay += 1
        if delay > 15:
            delay = 0

    # Display calculator result
    if len(op) > 12:  # Ensure string doesn't exceed calculator frame
        cv2.putText(res_img, op[-12:], (810, 90), cv2.FONT_HERSHEY_PLAIN, 3, (25, 25, 25), 3)
    else:
        cv2.putText(res_img, op, (810, 90), cv2.FONT_HERSHEY_PLAIN, 3, (25, 25, 25), 3)
    print(op)

    # Wait 1 millisecond, check for 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break

    # Display image
    cv2.imshow("camera", res_img)

# Release resources
handsDetector.close()
