# csvファイルを結合させる
from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
import glob
import os
import re
import csv

# シンドロームのリスト
syn_list = ["eh", "br", "bd", "bs", "km", "ez", "hm", "mf", "nm", "ok", "sm", "sr", "ub", "rb", "cm"]
# 列名
ef_list = [["名前","最大レベル","タイミング","技能","難易度","対象","射程","侵蝕値","制限","前提条件","効果","シンドローム","ルルブ","種別"]]

# シンドローム分回してcsvファイルを読み込みリストに
for syn in syn_list:
    csv_path = f"dx_csv/{syn}_ef_list.csv"
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        list_of_rows = list(csv_reader)
        # 先頭行（列名）は飛ばしてリストを結合していく
        ef_list += list_of_rows[1:]

# 一応printで確認
print(list_of_rows)

# 結合したリストをcsvファイルに書き込む
csv_path = f"dx_csv_add/ef_list_cmp.csv"
with open(csv_path, 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=',')
    writer.writerows(ef_list)