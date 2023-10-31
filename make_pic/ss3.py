# 数値は環境によって変わる
import pyautogui

pyautogui.sleep(10)

LR = "L"
line = 1
row = 0
e_c = 0

for j in range(14):
    for k in range(3):
        if e_c == -1:
            row += 1
            e_c += 1
        else:
            if LR == "L":
                left = 144 + row * 273
            else:
                left = 152 + row * 273
            top = 368 + line * 409
            width = 235
            height = 360
            screenshot = pyautogui.screenshot(region = (left, top, width, height))
            screenshot.save(f'../make_csv/results/cm/output_cm_e_ea_{e_c}.png')
            e_c += 1
            row += 1
        if row > 2:
            row = 0
            line += 1
        if line > 2:
            if LR == "L":
                LR = "R"
            else:
                LR = "L"
            pyautogui.press("right")
            pyautogui.sleep(1)
            line = 0