import pyautogui
import time
import random

time.sleep(4)
lx,ly= pyautogui.size()
print(lx,ly)
for i in range(20):
  pyautogui.moveTo(random.randint(0,1920),random.randint(50,1000),0.001)
  for j in range(2):
     pyautogui.moveRel(random.randint(-2,2),random.randint(-2,2))
  pyautogui.moveTo(random.randint(0,1920),random.randint(50,1000),0.001)
  for j in range(2):
     pyautogui.moveRel(random.randint(-2,2),random.randint(-2,2))
    