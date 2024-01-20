# 数値は環境によって変わる
# エフェクトアーカイブの一般エフェクト用

import pyautogui

pyautogui.sleep(10)

LR = "L"
line = 1
row = 0
e_c = 0

# 行数分回す
for j in range(14):
    # 列数分回す
    for k in range(3):
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
        # 列を更新
        row += 1
        # 列の値によって次の行へ
        if row > 2:
            row = 0
            line += 1
            # 行の値によって次のページへ
            if line > 2:
                # ページの左右の更新
                if LR == "L":
                    LR = "R"
                else:
                    LR = "L"
                pyautogui.press("right")
                pyautogui.sleep(1)
                line = 0