# 画像をOCRで文字起こししてcsvファイルに書き込む
from calendar import c
from PIL import Image

import pyocr
import pyocr.builders

import glob
import re
import csv

# シンドロームのリスト
syn_list = ["eh", "br", "bd", "bs", "km", "ez", "hm", "mf", "nm", "ok", "sm", "sr", "ub", "rb", "cm"]

# シンドローム分回す
for syn in syn_list:
    # 画像ファイル群のパスの取得
    path = f"results/{syn}/*"
    files = glob.glob(path)
    # 列名
    ef_list = [["名前","最大レベル","タイミング","技能","難易度","対象","射程","侵蝕値","制限","前提条件","効果"]]
    # ファイル分回す
    for file in files:
        ef = []
        img = Image.open(file)
        # ウロボロスのアージは別にスクショを撮ったので処理する
        if file == "results/ub/ub_ra_0.png":
            w, h = img.size
            img = img.resize((w*4, h*4), Image.Resampling.LANCZOS)
            print("ウロボのアージ！")
        # OCRで文字の取得
        tools = pyocr.get_available_tools()
        tool = tools[0]
        txt = tool.image_to_string(
        img,
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        # 改行文字で区切る
        txt_list = txt.split("\n")
        txt_list = [txt for txt in txt_list if txt != '']
        # 各列用の変数の準備
        name = ""
        level = ""
        timing = ""
        skill = ""
        difficulty = ""
        target = ""
        range = ""
        cost = ""
        limited = ""
        premise = ""
        effect = ""
        start_e = 0
        counter = 0
        # 読み込んだテキスト分回す
        for text in txt_list:
            # 空白を消す
            text = text.replace(" ","")
            # 正規表現を使って文字列が列とマッチするかを確認し、マッチしていれば文字列を処理して列変数に入力する
            if re.match("最大レベル.*", text):
                text_l = re.sub("最大レベル", "", text)
                text_l = re.sub("(:|：)", "", text_l)
                if level == "":
                    level = text_l
                    countname = counter - 1
                    name = txt_list[countname].replace(" ","")
                    name = re.sub("イー(ジ|シ)ー", "", name)
                    name = re.sub("エン(シ|ジ)ェルハイ.*", "", name)
                    name = re.sub("(ハ|バ|パ)ロール", "", name)
                    name = re.sub("(ブ|プ|フ)ラッ(ク|グ)(ド|ト)ッ(ク|グ)", "", name)
                    name = re.sub("(ブ|フ)ラム.*?ストーカー", "", name)
                    name = re.sub("キ(ュ|ユ)マイラ", "", name)
                    name = re.sub("ハヌマーン", "", name)
                    name = re.sub("モルフ(ェ|エ)ウス", "", name)
                    name = re.sub("ノイマン", "", name)
                    name = re.sub("オルクス", "", name)
                    name = re.sub("ハヌマーン", "", name)
                    name = re.sub("サラマン(ダ|タ)ー", "", name)
                    name = re.sub("ソラリス", "", name)
            if re.match("(タ|ダ).*?(グ|ク).*", text):
                text_t = re.sub("(タ|ダ).*?(グ|ク)", "", text)
                text_t = re.sub("(:|：)", "", text_t)
                if re.search("リア.*?ン", text_t):
                    print("リアクション！")
                else:
                    text_t = re.sub("ア.*?ン", "", text_t)
                text_t = re.sub("(フ|ブ|プ)..(ス|ズ)", "", text_t)
                if timing == "":
                    timing = text_t
            if re.match("技能.*", text):
                text_s = re.sub("技能", "", text)
                text_s = re.sub("難.*?度.*", "", text_s)
                text_s = re.sub("(:|：)", "", text_s)
                if skill == "":
                    skill = text_s
            if re.search("難.*?度.*", text):
                text_d = re.search("難.*?度.*", text).group()
                text_d = re.sub("難.*?度", "", text_d)
                text_d = re.sub("(:|：)", "", text_d)
                if difficulty == "":
                    difficulty = text_d
            if re.match("対象.*", text):
                text_ta = re.sub("対象", "", text)
                text_ta = re.sub("射程.*", "", text_ta)
                text_ta = re.sub("(:|：)", "", text_ta)
                if target == "":
                    target = text_ta
            if re.search("射程.*", text):
                text_r = re.search("射程.*", text).group()
                text_r = re.sub("射程", "", text_r)
                text_r = re.sub("(:|：)", "", text_r)
                if range == "":
                    range = text_r
            if re.match("侵.*?値.*", text):
                text_c = re.sub("侵.*?値", "", text)
                text_c = re.sub("制限.*", "", text_c)
                text_c = re.sub("(:|：)", "", text_c)
                if cost == "":
                    cost = text_c
            if re.search("制限.*", text):
                text_lim = re.search("制限.*", text).group()
                text_lim = re.sub("制限", "", text_lim)
                text_lim = re.sub("(:|：)", "", text_lim)
                if re.search(".*?%", text_lim):
                    text_lim = re.search(".*?%", text_lim).group()
                if limited == "":
                    limited = text_lim
            if re.match("前提.*?.*", text):
                text_p = re.sub("前提..", "", text)
                text_p = re.sub("(:|：)", "", text_p)
                if premise == "":
                    premise = text_p
            if start_e == 1:
                effect += text
            if re.match("効果.*", text):
                if effect == "":
                    start_e = 1
                    text_e = re.sub("効果", "", text)
                    text_e = re.sub("(:|：)", "", text_e)
                    effect += text_e
            counter += 1
        # 抽出した変数をリストに入れる
        ef = [name, level, timing ,skill ,difficulty ,target ,range ,cost ,limited ,premise ,effect]
        # 作成したリストをappend
        ef_list.append(ef)
        # 一応printで確認
        print(txt)
        print()
        print(txt_list)
        print(ef)
        print(file)
        print()
        print()
    
    # 最終的に出来上がったリストをシンドロームごとにcsvファイルに書き込み
    out_path = f"dx_csv/{syn}_ef_list.csv"
    with open(out_path, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
        writer.writerows(ef_list) 