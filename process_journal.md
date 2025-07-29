## Process of Development
1. Since all the calculator buttons are similar, I started by developing the Button class.
2. Next, I created a window to display the feed from the laptop camera.
3. After that, I implemented a hand detector using MediaPipe.
4. Using a loop, I drew all the calculator buttons in the window.
5. Initially, the buttons were filled with color, but I found it more convenient to see the fingers, so I removed the color.
6. Then, I worked on detecting button presses. Inspired by a video about the top 25 computer vision projects, I implemented a press detection system based on the distance between the index and middle fingers.
7. Through experimentation, I determined that the optimal distance value (at 30 cm) was 43.
8. After that, I began building the calculator logic. I found the eval() function very useful, as it evaluates basic mathematical operations from a string.
9. I spent a considerable amount of time dealing with the issue of character limits on the calculator screen—only 12 characters fit at most.
10. To solve this, I decided to display only the first 12 characters during input. For results longer than 12 characters, I rounded and converted them to scientific notation.
11. I also added a delay after each button press to prevent accidental double presses while the user moves their fingers apart.
12. I spent a long time thinking about how to handle exceptions (like division by zero) that caused errors in the calculator.
13. The solution was simple: I used a try-except block to catch errors and display "Error" whenever eval() failed.
14. Another issue was that hand detection worked poorly on the right side of the screen—the detector often lost track of the hand.
15. It turned out the problem was that the buttons were drawn before hand detection, meaning the detector tried to recognize the hand through the button grid, which didn’t work well.
16. To fix this, I moved the button-drawing loop after the hand detection process.
17. Finally, I added the AC (All Clear) and DEL (Delete) buttons and shifted the calculator slightly upward to prevent hand detection from failing when users pressed the lower buttons.
