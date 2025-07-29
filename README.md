# Virtual Calculator  
This program allows you to operate a simple virtual calculator using your computer's camera.  

The calculator supports addition, subtraction, multiplication, and division. To raise a number to a power, represent the operation on the calculator as `x**n`, where `n` is the exponent. For decimal numbers, use a dot (`.`).  

## Notes:  
1. If you enter a dot followed by a fractional part without an integer part, the integer part will default to zero.  
2. To ensure the calculation result fits on the calculator screen, the program uses rounding, which depends on the number's length. For numbers longer than 12 characters (including the dot), a loss of precision may occur.  
3. In case of other errors—including division by zero and syntax errors—the display will show "Error."  
4. The calculator is not designed to work with numbers close to or exceeding Python's limit values: from 2.2250738585072014e-308 to 1.7976931348623157e+308.  

## Buttons  
1. The **AC** button clears everything on the calculator screen.  
2. The **DEL** button removes the last entered element.  
3. To press a button, bring your index and middle fingers together so that their on-screen representation touches the desired button. The program registers this gesture (where the distance between the fingers is minimal) as a button press.  
4. For optimal performance, your hand should ideally be about 30 centimeters from the camera. Otherwise, the program may not work correctly.  

## Hand Recognition  
1. If dots and lines appear on your hand, it means the program has recognized it.  
2. Otherwise, move your hand closer to the camera and wait until it is recognized.  

To exit the program, press **'q'** on the keyboard.
