# 数値は環境によって変わる
# ページごとにシンドロームが変わるルルブの場合はこれを使う
# 現在はエフェクトアーカイブのエネミーエフェクトのスクショに用いた状態
import pyautogui

pyautogui.sleep(10)

# シンドロームのリスト
syn_list = ["eh", "br", "bd", "bs", "km", "ez", "hm", "mf", "nm", "ok", "sm", "sr", "ub", "rb"]
LR = "L"
# シンドローム分回す
for syn in syn_list:
    # 一行目がシンドローム名になっているので飛ばす用のフラグ
    skip_firstline = True
    e_c = 0
    # ブラムストーカーは従者用エフェクトでページ数が多い場合があるので個別にページ数を設定
    if syn == "bs":
        page = 1
    else:
        page = 1
    # ページ数分回す
    for i in range(page):
        # 一行目を飛ばすかの判定
        if skip_firstline:
            loop = range(1,3)
            skip_firstline = False
        else:
            loop = range(3)
        # 縦×横の二重ループを回してスクショをとる
        for j in loop:
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
        # 見開きで左のページか右のページかで微妙に位置が異なるので一ページごとに更新する
        if LR == "L":
            LR = "R"
        else:
            LR = "L"
        pyautogui.press("right")
        pyautogui.sleep(1)