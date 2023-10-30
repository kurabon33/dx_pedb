import pyautogui

pyautogui.sleep(10)

syn_list = ["eh", "br", "bd", "bs", "km", "ez", "hm", "mf", "nm", "ok", "sm", "sr", "ub"]
LR = "L"
line = 2
row = 0

for i in range(12):
    line = 2
    row = 0
    for syn in syn_list:
        e_c = 0
        for j in range(1):
            for k in range(1):
                if e_c != -1:
                    if LR == "L":
                        left = 144 + row * 273
                    else:
                        left = 152 + row * 273
                    top = 368 + line * 409
                    width = 235
                    height = 360
                    screenshot = pyautogui.screenshot(region = (left, top, width, height))
                    screenshot.save(f'dx/{syn}/{syn}_ra_{i}.png')
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