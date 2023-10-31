import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import sqlite3
import textwrap

# 画面遷移の処理
def change_app(nowwindow, towindow):
    c_serch_frames = [frame1,frame2,frame3,frame4,frame5,frame6,frame7,frame8,frame9,frame10]
    menu_frames = [frame_titl, frame_serch, frame_com_serch]
    result_frames = [frame_serch_result, button_change_main_frame_s_result2 ,space_frame, frame_input_error]
    if towindow == main_frame_s_result:
        for f in result_frames:
            f.destroy()
        serch_ef(nowwindow)
        for f in c_serch_frames:
            f.pack_forget()
        for f in menu_frames:
            f.pack_forget()
    if towindow == main_frame_c_serch:
        for f in result_frames:
            f.destroy()
        canvas.config(scrollregion=(0,0,800,600))
        for f in c_serch_frames:
            f.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)
        for f in menu_frames:
            f.pack_forget()
    if towindow == main_frame_menu:
        frame_titl.pack(anchor=tk.N, fill=tk.BOTH, pady=2)
        frame_serch.pack(anchor=tk.N, fill=tk.X, pady=2)
        frame_com_serch.pack(anchor=tk.N, expand=1, fill=tk.X, pady=2)
        for f in c_serch_frames:
            f.pack_forget()
    towindow.tkraise()

# チェックボックス
def make_check_box(item, check, flame):
    yoko = 0
    tate = 1
    for i in range(len(item)):
        check[i] = tk.BooleanVar()
        ttk.Checkbutton(flame,
                    variable = check[i],
                    text = item[i]
                    ).grid(row= tate, column=yoko,sticky=tk.W+tk.E)
        yoko += 1
        if yoko == 10:
            tate += 1
            yoko = 0

# 検索
def serch_ef(nowwindow):
    global main_frame_s_result, serch_keyword, serch_keyword1, frame_input_error, space_frame
    c_list = [syn_check, time_check, skl_check, trg_check, rng_check, lmt_check, knd_check]
    i_list = [syn_item, time_item, skl_item, trg_item, rng_item, lmt_item, knd_item]
    pick_list = ["syndrome", "timing", "skill", "target", "range", "limited", "kinds"]
    con = sqlite3.connect("dx_ef_list.db")
    cur = con.cursor()
    select_ef = "SELECT name, level, timing, skill, diffculty, target, range, cost, limited, kinds, effect FROM dx_ef_list"
    dex = 0
    if nowwindow == main_frame_c_serch:
        for i in range(len(c_list)):
            check = c_list[i]
            item = i_list[i]
            select_letter = ""
            for j in check:
                if check[j].get() == True:
                    if dex == 0:
                        select_letter = f" where ({pick_list[i]} like '%{item[j]}%'"
                        dex = 1
                    elif select_letter == "":
                        select_letter = f" and ({pick_list[i]} like '%{item[j]}%'"
                    else:
                        select_letter += f" or {pick_list[i]}  like '%{item[j]}%'"
            if select_letter != "":
                select_letter += ")"
            select_ef += select_letter
    if nowwindow == main_frame_c_serch:
        keyword = serch_keyword.get()
    elif nowwindow == main_frame_menu:
        keyword = serch_keyword1.get()
    keyword = keyword.replace('　',' ')
    keyword_list = keyword.split(' ')
    select_letter = ""
#    print(keyword_list)
    for key in keyword_list:
        if key != "":
            if dex == 0:
                select_letter = f" where (name like '%{key}%' or effect like '%{key}%')"
                dex = 1
            elif select_letter == "":
                select_letter = f" and (name like '%{key}%' or effect like '%{key}%')"
            else:
                select_letter += f" or (name like '%{key}%' or effect like '%{key}%')"
    select_ef += select_letter
    if select_ef != "SELECT name, level, timing, skill, diffculty, target, range, cost, limited, kinds, effect FROM dx_ef_list":
        cur.execute(select_ef)
        #print(select_ef)
        ef_list = cur.fetchall()
        if len(ef_list) == 0:
            frame_input_error.destroy()
            space_frame.destroy()
            frame_input_error = ttk.Frame(main_frame_s_result, style='AAA.TFrame')
            frame_input_error.pack()
            label_input_error = ttk.Label(frame_input_error, text="条件に一致するエフェクトがありません！", font=40).pack(expand=1, fill=tk.BOTH, pady=2)
            space_frame = ttk.Frame(main_frame_s_result, style='AAA.TFrame') 
            label = ttk.Label(space_frame, padding=[10,canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)
            space_frame.pack(expand=1, fill=tk.BOTH)
        else:
            make_result(ef_list, nowwindow)
#        print(keyword_list)
    else:
        frame_input_error.destroy()
        space_frame.destroy()
        frame_input_error = ttk.Frame(main_frame_s_result, style='AAA.TFrame')
        frame_input_error.pack()
        label_input_error = ttk.Label(frame_input_error, text="検索条件を入力、選択してください！", font=40).pack(expand=1, fill=tk.BOTH, pady=2)
        space_frame = ttk.Frame(main_frame_s_result, style='AAA.TFrame') 
        label = ttk.Label(space_frame, padding=[10,canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)
        space_frame.pack(expand=1, fill=tk.BOTH)


# 検索結果
def make_result(result_list, nowwindow):
    global frame_serch_result, button_change_main_frame_s_result2, space_frame, tree
    frame_serch_result.destroy()
    button_change_main_frame_s_result2.destroy()
    space_frame.destroy()
    frame_serch_result = ttk.Frame(main_frame_s_result, style='AAA.TFrame')
    frame_serch_result.pack(expand=1, fill=tk.BOTH)
    columns = ("エフェクト名","最大レベル","タイミング","技能","難易度","対象","射程","侵蝕値","制限","種別","効果")
    tree = ttk.Treeview(frame_serch_result, columns=column)
    tree.bind("<<TreeviewSelect>>", make_effect)
    tree.column('#0',width=0, stretch='no')
    font1 = tkFont.Font(family='Meiryo', size=7)
    style_tree = ttk.Style()
    style_tree.configure("Treeview.Heading", font=('Meiryo', 8, "bold"))
    style_tree.configure("Treeview", font=('Meiryo', 7, "bold"), relief="SOLID")
    fixture_treeview_tag_config(style_tree)
    tree.tag_configure('odd', background='#eeeeee')
    tree.tag_configure('even', background='#DFDFDF')
    for col_name in columns:
        tree.heading(col_name, text=col_name)
        width1 = font1.measure(col_name)+11
        tree.column(col_name, width=width1+10)
    for i, _ in enumerate(result_list[0]):
        if i != 10:
            max_str = max([x[i] for x in result_list], key=lambda x:len(str(x))) or "    "
            if type(max_str) is str:
                max_str = max(max_str.split("\n"), key=len)
            width1 = font1.measure(max_str) + 16
            header1 = tree.column(tree['columns'][i], width=None)
            if width1 > header1:
                tree.column(tree['columns'][i], width=width1)
    fill_width = 0
    for i in range(len(result_list[0])):
        if i != 10:
            fill_width += tree.column(tree['columns'][i], width=None)
    effect_width = int(canvas.cget("width")) - fill_width - 16
    tree.column(tree['columns'][10], width = effect_width)
    cells = []
    column_e_width = tree.column(tree['columns'][10], width=None)
    for i, result in enumerate(result_list):
        info_list = list(result)
        tag = ["odd", "even"][i % 2]
        text_ef_n = ""
        width_text_ef = 0
        count_t_n = 0
        for j, t in enumerate(info_list[10]):
            width_text_ef += font1.measure(t)
            if (width_text_ef+10) > column_e_width:
#                print(width_text_ef)
#                print(text_ef_n)
                text_ef_n += "\n"
                width_text_ef = 0
                count_t_n = j
                break
            text_ef_n += t
        f_ad_text = count_t_n
        while f_ad_text < len(info_list[10]):
            width_text_ef = font1.measure(info_list[10][f_ad_text:f_ad_text+count_t_n])
            if (width_text_ef+10) > column_e_width:
                for k in range(count_t_n):
                    width_text_ef = font1.measure(info_list[10][f_ad_text:f_ad_text+count_t_n-k])
                    if (width_text_ef+10) <= column_e_width:
                        text_ef_n += info_list[10][f_ad_text:f_ad_text+count_t_n-k] + "\n"
                        f_ad_text = f_ad_text + count_t_n - k
#                        print(width_text_ef)
#                        print(text_ef_n)
                        break
            else:
                for k in range(count_t_n):
                    width_text_ef = font1.measure(info_list[10][f_ad_text:f_ad_text+count_t_n+k])
                    if (width_text_ef+10) > column_e_width:
                        text_ef_n += info_list[10][f_ad_text:f_ad_text+count_t_n+k-1] + "\n"
                        f_ad_text = f_ad_text + count_t_n + k - 1
#                        print(width_text_ef)
#                        print(text_ef_n)
                        break
                    else:
                        if f_ad_text+count_t_n+k >= len(info_list[10]):
                            text_ef_n += info_list[10][f_ad_text:]
                            f_ad_text = f_ad_text + count_t_n + k
#                            print(width_text_ef)
#                            print(text_ef_n)
                            break

        info_list[10] = text_ef_n
        tree.insert(parent="", index="end", values=info_list, tags=(tag,))
        cells.append(info_list[10])
    longest_cell = max(cells, key=lambda x:x.count("\n"))
    max_row_lines = longest_cell.count("\n") + 1   
    style_tree.configure("Treeview", rowheight = 14 * max_row_lines)
    tree.configure(height= (int(canvas.cget("height"))-77)//(14 * max_row_lines))
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    style_scbar = ttk.Style()
    style_scbar.configure("Scrollbar", width=16)
    scrollbar = ttk.Scrollbar(frame_serch_result, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=1)

    space_frame = ttk.Frame(main_frame_s_result, style='AAA.TFrame') 
    label = ttk.Label(space_frame, padding=[10,canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)
    space_frame.pack(expand=1, fill=tk.BOTH)

# エフェクトの詳細
def make_effect(event):
    global frame_effect_info, tree
    record_id = tree.focus()
    effect_info = tree.item(record_id, 'values')
    effect_name = effect_info[0]
    print(effect_name)
    con = sqlite3.connect("dx_ef_list.db")
    cur = con.cursor()
    s2 = ttk.Style()
    s2.configure('BBB.TFrame', background='white')
    frame_effect_info = ttk.Frame(canvas, style='BBB.TFrame')
    frame_tyousei = tk.Frame(frame_effect_info, bd=2, relief=tk.SOLID, bg="white")
    select_ef = f"SELECT name, level, timing, skill, diffculty, target, range, cost, limited, prere, kinds, effect, syndrome, books FROM dx_ef_list where name == '{effect_name}'"
    for ef_infos in cur.execute(select_ef):
        text_name = tk.Text(frame_tyousei, height=1, font=("Arial", 35), background="white", borderwidth=0, width=30)
        text_name.insert(1.0, ef_infos[0])
        text_name.configure(state="disabled")
        text_name.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nesw")
        text_level = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=30)
        text_level.insert(1.0, "最大レベル：" + str(ef_infos[1]))
        text_level.configure(state="disabled")
        text_level.grid(row=2, column=0, columnspan=2, sticky="nesw")
        text_timing = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=30)
        text_timing.insert(1.0, "タイミング：" + ef_infos[2])
        text_timing.configure(state="disabled")
        text_timing.grid(row=3, column=0, columnspan=2, sticky="nesw")
        text_skill = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_skill.insert(1.0, "技能：" + ef_infos[3])
        text_skill.configure(state="disabled")
        text_skill.grid(row=4, column=0, sticky="nesw")
        text_diff = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_diff.insert(1.0, "難易度：" + ef_infos[4])
        text_diff.configure(state="disabled")
        text_diff.grid(row=4, column=1, sticky="nesw")
        text_target = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_target.insert(1.0, "対象：" + ef_infos[5])
        text_target.configure(state="disabled")
        text_target.grid(row=5, column=0, sticky="nesw")
        text_range = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_range.insert(1.0, "射程：" + ef_infos[6])
        text_range.configure(state="disabled")
        text_range.grid(row=5, column=1, sticky="nesw")
        text_cost = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_cost.insert(1.0, "侵蝕値：" + ef_infos[7])
        text_cost.configure(state="disabled")
        text_cost.grid(row=6, column=0, sticky="nesw")
        text_limit = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_limit.insert(1.0, "制限：" + ef_infos[8])
        text_limit.configure(state="disabled")
        text_limit.grid(row=6, column=1, sticky="nesw")
        text_pre = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=30)
        text_pre.insert(1.0, "前提条件：" + ef_infos[9])
        text_pre.configure(state="disabled")
        text_pre.grid(row=7, column=0, columnspan=2, sticky="nesw")
        text_kind = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=30)
        text_kind.insert(1.0, "種別：" + ef_infos[10])
        text_kind.configure(state="disabled")
        text_kind.grid(row=8, column=0, columnspan=2, sticky="nesw")
        kouka = ef_infos[11]
        kouka = kouka.replace("　　", "\n")
        kouka = kouka.replace("　", "		")
        text_eff = tk.Text(frame_tyousei, height=11, font=("Arial", 17), background="white", borderwidth=0, wrap=tk.WORD, width=30)
        text_eff.insert(1.0, "効果：" + kouka)
        text_eff.configure(state="disabled")
        text_eff.grid(row=9, column=0, columnspan=2, sticky="nesw")
        text_syn = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_syn.insert(1.0, "【" + ef_infos[12] + "】")
        text_syn.configure(state="disabled")
        text_syn.grid(row=10, column=0, sticky="nesw")
        text_book = tk.Text(frame_tyousei, height=1, font=("Arial", 17), background="white", borderwidth=0, width=15)
        text_book.insert(1.0, "【" + ef_infos[13] + "】")
        text_book.configure(state="disabled")
        text_book.grid(row=10, column=1, sticky="nes")
    frame_tyousei.pack(anchor=tk.CENTER, expand=1, fill=tk.Y)
    s3 = ttk.Style()
    s3.configure('CCC.TButton', background='white', bordercolor="black", borderwidth=2)
    button = ttk.Button(frame_effect_info, text="戻る", command=lambda: eraser(frame_effect_info), style='CCC.TButton').pack()#.grid(row=10, column=0, columnspan=2, sticky="nesw")
    frame_effect_info.pack(anchor=tk.CENTER, expand=1, fill=tk.BOTH)

def eraser(frame_d):
    frame_d.destroy()

def copy_text(txt_label):
    txt = txt_label.cget("text")
    print(txt)
    root.clipboard_append(txt)

def fixture_treeview_tag_config(style):
    def fixed_map(option):
        return [elm for elm in style.map('Treeview', query_opt=option) if
          elm[:2] != ('!disabled', '!selected')]
    style.map('Treeview',
        foreground=fixed_map('foreground'),
        background=fixed_map('background'))


root = tk.Tk()

s = ttk.Style()
s.theme_use('clam')
s.configure('AAA.TFrame', background='black')

root.geometry('980x600') 
root.resizable(0, 0)
root.title('DX3rdぱーふぇくとえふぇくとでーたべーす（仮）')
root.iconbitmap('dx3_logo.ico')
root.configure(bg="black")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Canvas Widget を生成
canvas = tk.Canvas(root, width = root.winfo_width(), height = root.winfo_height())
canvas.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

"""# Scrollbar を生成して配置
bary = tk.Scrollbar(root, orient=tk.VERTICAL)
bary.pack(side=tk.RIGHT, fill=tk.Y)


# Scrollbarを制御をCanvasに通知する処理を追加
bary.config(command=canvas.yview)


# Canvasのスクロール範囲を設定
canvas.config(scrollregion=(0,0,800,600))

# Canvasの可動域をScreoobarに通知する処理を追加
canvas.config(yscrollcommand=bary.set)"""


#こっから初期画面
main_frame_menu = ttk.Frame(canvas, style='AAA.TFrame') 
#main_frame_menu.grid(row=0, column=0, sticky="nsew")
canvas.create_window((0,0), window=main_frame_menu, anchor=tk.NW, width=canvas.cget('width'), height=canvas.cget('height'))

frame_titl = ttk.Frame(main_frame_menu, style='AAA.TFrame')
label_1 = ttk.Label(frame_titl, text='ぱーふぇくとえふぇくとでーたべーす（仮）', foreground='red',background="black",font =("Helvetica",20)).pack()
image_2 = tk.PhotoImage(file='dx3_logo.ppm')
label_2 = ttk.Label(frame_titl, image=image_2).pack()
frame_titl.pack(anchor=tk.N, fill=tk.BOTH, pady=2)

frame_serch = ttk.Frame(main_frame_menu, style='AAA.TFrame')
label = ttk.Label(frame_serch, text='キーワードから検索').grid(row= 0, column=1) 
serch_keyword1 = ttk.Entry(frame_serch, width=30)
serch_keyword1.grid(row= 0, column=2)
button = ttk.Button(frame_serch, text = '検索', command = lambda: change_app(main_frame_menu, main_frame_s_result)).grid(row= 0, column=3)
frame_serch.pack(anchor=tk.N, fill=tk.X, pady=2)

frame_com_serch = ttk.Frame(main_frame_menu)
button = ttk.Button(frame_com_serch, text = '詳細検索', command = lambda: change_app(main_frame_menu, main_frame_c_serch)).pack(anchor=tk.N, expand=1, fill=tk.BOTH)
frame_com_serch.pack(anchor=tk.N, expand=1, fill=tk.X, pady=2)


#こっから詳細検索画面
main_frame_c_serch = ttk.Frame(canvas, width=800, style='AAA.TFrame') 
#main_frame_c_serch.grid(row=0, column=0, sticky="nsew")
canvas.create_window((0,0), window=main_frame_c_serch, anchor=tk.NW, width=canvas.cget('width'), height=canvas.cget('height'))

frame1 = ttk.Frame(main_frame_c_serch, style='AAA.TFrame')
label_1 = ttk.Label(frame1, text='ぱーふぇくとえふぇくとでーたべーす（仮）', foreground='red',background="black",font =("Helvetica",20)).pack()
image_2a = tk.PhotoImage(file='dx3_logo.ppm')
label_2 = ttk.Label(frame1, image=image_2a).pack()
frame1.pack(anchor=tk.N, fill=tk.BOTH, pady=2)

frame2 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame2, text='キーワード').grid(row= 0, column=1) 
serch_keyword = ttk.Entry(frame2, width=50)
serch_keyword.grid(row= 0, column=2)
frame2.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)
 
frame3 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame3, text='シンドローム').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
syn_item = ["エンジェルハィロゥ","バロール","ブラックドッグ","ブラム＝ストーカー","キュマイラ","エグザイル","ハヌマーン","モルフェウス","ノイマン","オルクス","サラマンダー","ソラリス","ウロボロス","レネゲイドビーイング","一般"]
syn_check = {}
make_check_box(syn_item, syn_check, frame3)
frame3.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)

frame4 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame4, text='タイミング').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
time_item = ["メジャー","マイナー","オート","常時","セットアップ","イニシアチブ","クリンナップ","リアクション","効果参照"]
time_check = {}
make_check_box(time_item, time_check, frame4)
frame4.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)

frame5 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame5, text='技能').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
skl_item = ["―","〈白兵〉","〈射撃〉","〈RC〉","〈交渉〉","シンドローム","効果参照","〈回避〉","〈運転:〉","〈知覚〉","〈芸術:〉","〈意志〉","〈知識:〉","〈調達〉","〈情報:〉","【肉体】","【感覚】","【精神】","【社会】"]
skl_check = {}
make_check_box(skl_item, skl_check, frame5)
frame5.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)

frame6 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame6, text='対象').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
trg_item = ["―","自身","単体","範囲","シーン","LV+1体","2体","3体","効果参照","解説参照"]
trg_check = {}
make_check_box(trg_item, trg_check, frame6)
frame6.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)

frame7 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame7, text='射程').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
rng_item = ["―","至近","武器","視界","10m","20m","効果参照"]
rng_check = {}
make_check_box(rng_item, rng_check, frame7)
frame7.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)

frame8 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame8, text='制限').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
lmt_item = ["―","80%","100%","120%","ピュア","リミット","従者専用","効果参照"]
lmt_check = {}
make_check_box(lmt_item, lmt_check, frame8)
frame8.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)

frame9 = ttk.Frame(main_frame_c_serch)
label = ttk.Label(frame9, text='種別').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
knd_item = ["―","イージー","エネミー"]
knd_check = {}
make_check_box(knd_item, knd_check, frame9)
frame9.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)

frame10 = ttk.Frame(main_frame_c_serch)
button = ttk.Button(frame10,
                   text = "戻る",
                   command = lambda: change_app(main_frame_c_serch, main_frame_menu)
                   ).grid(row=0, column=0, sticky="nsew", pady=2)
button2 = ttk.Button(frame10,
                   text = "検索",
                   command = lambda: change_app(main_frame_c_serch, main_frame_s_result)
                   ).grid(row=0, column=1, sticky="nsew", pady=2)
frame10.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)


#こっから検索結果画面
main_frame_s_result = ttk.Frame(canvas)
#main_frame_s_result.grid(row=0, column=0, sticky="nsew")
canvas.create_window((0,0), window=main_frame_s_result, anchor=tk.NW, width= canvas.cget('width'))

label1_main_frame_s_result = ttk.Label(main_frame_s_result, text="検索結果")
label1_main_frame_s_result.pack()

frame_serch_result = ttk.Frame(main_frame_s_result, style='AAA.TFrame')
frame_serch_result.pack(expand=1, fill=tk.BOTH)

column = ("エフェクト名","最大レベル","タイミング","技能","難易度","対象","射程","侵蝕値","制限","種別","効果")
tree = ttk.Treeview(frame_serch_result, columns=column)
tree.pack(expand=1, fill=tk.BOTH)

# スクロールバーの追加
scrollbar = ttk.Scrollbar(frame_serch_result, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


button_change_main_frame_s_result = ttk.Button(main_frame_s_result, text="メインウィンドウに移動", command=lambda: change_app(main_frame_s_result, main_frame_c_serch))
button_change_main_frame_s_result.pack(anchor=tk.N)

button_change_main_frame_s_result2 = ttk.Button(main_frame_s_result, text="メインウィンドウに移動", command=lambda: change_app(main_frame_s_result, main_frame_c_serch))
button_change_main_frame_s_result2.pack(anchor=tk.N)

space_frame = ttk.Frame(main_frame_s_result, style='AAA.TFrame') 
label = ttk.Label(space_frame, padding=[10,canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)
space_frame.pack(expand=1, fill=tk.BOTH)

frame_input_error = ttk.Frame(frame_serch_result, style='AAA.TFrame')
label_input_error = ttk.Label(frame_serch_result, text="検索条件を入力、選択してください！", font=40).pack(expand=1, fill=tk.BOTH, pady=2)
frame_input_error.pack(expand=1, fill=tk.BOTH)

main_frame_menu.tkraise()
root.mainloop()