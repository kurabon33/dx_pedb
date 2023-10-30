import sqlite3
import csv

#dbの作成または接続
con = sqlite3.connect("dx_ef_list.db")
cur = con.cursor()

#テーブルの作成、存在しない場合のみ
create_test = "CREATE TABLE IF NOT EXISTS DX_ef_list (name TEXT, level INTEGER, timing TEXT, skill TEXT, diffculty TEXT, target TEXT, range TEXT, cost TEXT, limited TEXT, prere TEXT, effect TEXT, syndrome TEXT, books TEXT, kinds TEXT)"
cur.execute(create_test)

#テーブルのデータの削除
delete_test = "DELETE FROM dx_ef_list"
cur.execute(delete_test)

#csvファイルの指定
open_csv = open("ef_list_cmp.csv")

#csvファイルを読み込む
read_csv = csv.reader(open_csv)

#next()関数を用いて最初の行(列名)はスキップさせる
next_row = next(read_csv)

#csvデータをINSERTする
rows = []
for row in read_csv:
    rows.append(row)

#executemany()で複数のINSERTを実行する
cur.executemany(
    "INSERT INTO dx_ef_list (name, level, timing, skill, diffculty, target, range, cost, limited, prere, effect, syndrome, books, kinds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)

#テーブルの変更内容保存とcsvファイルを閉じる
con.commit()
open_csv.close()

#テーブルの確認
select_test = "SELECT name, skill, syndrome, effect FROM dx_ef_list where name like '%骨の剣%'"
select_test = "SELECT name, level, timing, skill, diffculty, target, range, cost, limited, kinds, effect, books FROM dx_ef_list where syndrome like '%エンジェルハィロゥ%' or syndrome like '%バロール%'"

print("—————————-")
print("fetchall")
print("—————————-")
print(cur.execute(select_test))
print(cur.fetchall())
print("—————————-")
print("for文")
print("—————————-")
for i in cur.execute(select_test):
    for j in i:
        print(j)

#データベースの接続終了
con.close
