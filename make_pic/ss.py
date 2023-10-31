# 数値は環境によって変わる
import pyautogui

pyautogui.sleep(10)

syn_list = ["eh", "br", "bd", "bs", "km", "ez", "hm", "mf", "nm", "ok", "sm", "sr", "ub", "rb"]
LR = "L"
for syn in syn_list:
    e_c = 0
    if syn == "bs":
        page = 1
    else:
        page = 1
    for i in range(page):
        for j in range(1,3):
            for k in range(3):
                if LR == "L":
                    left = 144 + k * 273
                else:
                    left = 152 + k * 273
                top = 368 + j * 409
                width = 235
                height = 360
                screenshot = pyautogui.screenshot(region = (left, top, width, height))
                screenshot.save(f'../make_csv/results/{syn}/output_{syn}_e_ea_{e_c}.png')
                e_c += 1
        if LR == "L":
            LR = "R"
        else:
            LR = "L"
        pyautogui.press("right")
        pyautogui.sleep(1)
#    if LR == "L":
#            LR = "R"
#    else:
#        LR = "L"
#    pyautogui.press("right")
#    pyautogui.sleep(1)