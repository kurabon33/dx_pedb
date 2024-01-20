# 数値は環境によって変わる
# その他のルルブのエフェクト用
import pyautogui

pyautogui.sleep(10)

# シンドロームのリスト
syn_list = ["eh", "br", "bd", "bs", "km", "ez", "hm", "mf", "nm", "ok", "sm", "sr", "ub"]
LR = "L"
line = 1
row = 0
e_c = 0

# シンドローム分回す
for syn in syn_list:
    # そのルルブに収録されているシンドロームあたりのエフェクト数
    num = 5
    e_c = 0
    # 先頭のセルはシンドローム名なのでnum+1回分回す
    for i in range(num+1):
        # 先頭は飛ばす
        if i != 0:
            # 位置を指定してスクリーンショット
            if LR == "L":
                left = 144 + row * 273
            else:
                left = 152 + row * 273
            top = 368 + line * 409
            width = 235
            height = 360
            screenshot = pyautogui.screenshot(region = (left, top, width, height))
            screenshot.save(f'../make_csv/results/{syn}/output_{syn}_hr_{i}.png')
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