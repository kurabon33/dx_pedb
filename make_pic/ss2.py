# 数値は環境によって変わる
# レネゲイスアージのアージエフェクト用
import pyautogui

pyautogui.sleep(10)

# シンドロームのリスト
# ウロボロスのアージは別途スクショすること
syn_list = ["eh", "br", "bd", "bs", "km", "ez", "hm", "mf", "nm", "ok", "sm", "sr"]
LR = "L"
e_c = 0

# 衝動の種類分回す
for i in range(12):
    line = 2
    row = 0
    # シンドローム分回す
    for syn in syn_list:
        # 位置を指定してスクリーンショット
        if LR == "L":
            left = 144 + row * 273
        else:
            left = 152 + row * 273
        top = 368 + line * 409
        width = 235
        height = 360
        screenshot = pyautogui.screenshot(region = (left, top, width, height))
        screenshot.save(f'../make_csv/results/{syn}/output_{syn}_ra_{i}.png')
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
    e_c += 1