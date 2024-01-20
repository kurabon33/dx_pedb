import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import sqlite3
import textwrap

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

# ツリーの見た目設定
def fixture_treeview_tag_config(style):
    def fixed_map(option):
        return [elm for elm in style.map('Treeview', query_opt=option) if
          elm[:2] != ('!disabled', '!selected')]
    style.map('Treeview',
        foreground=fixed_map('foreground'),
        background=fixed_map('background'))

# 描画に用いるフレームをクラスにする
class MainFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        self.canvas = master
        super().__init__(self.canvas, **kwargs, style='AAA.TFrame')
        self.create_canvas()
        self.create_main()
        self.create_serch()
        self.create_result()

    # canvasの作成
    def create_canvas(self):
        self.canvas.create_window((0,0), window=self, anchor=tk.NW, width=self.canvas.cget('width'), height=self.canvas.cget('height'))

    # メインページの要素配置
    def create_main(self):
        self.frame_titl = ttk.Frame(self, style='AAA.TFrame')
        label_1 = ttk.Label(self.frame_titl, text='ぱーふぇくとえふぇくとでーたべーす（仮）', foreground='red',background="black",font =("Helvetica",20)).pack()
        self.image_2 = tk.PhotoImage(file='dx3_logo.ppm')
        label_2 = ttk.Label(self.frame_titl, image=self.image_2).pack()
        self.frame_titl.pack(anchor=tk.N, fill=tk.BOTH, pady=2)

        self.frame_serch = ttk.Frame(self, style='AAA.TFrame')
        label = ttk.Label(self.frame_serch, text='キーワードから検索').grid(row= 0, column=1) 
        self.serch_keyword1 = ttk.Entry(self.frame_serch, width=30)
        self.serch_keyword1.grid(row= 0, column=2)
        button = ttk.Button(self.frame_serch, text = '検索', command = lambda: self.change_app("main_frame", "result_frame")).grid(row= 0, column=3)
        self.frame_serch.pack(anchor=tk.N, fill=tk.X, pady=2)

        self.frame_com_serch = ttk.Frame(self)
        button = ttk.Button(self.frame_com_serch, text = '詳細検索', command = lambda: self.change_app("main_frame", "serch_frame")).pack(anchor=tk.N, expand=1, fill=tk.BOTH)
        self.frame_com_serch.pack(anchor=tk.N, expand=1, fill=tk.X, pady=2)
 
    # 詳細検索画面の要素を設定だけする
    def create_serch(self):
        #こっから詳細検索画面
        self.frame1 = ttk.Frame(self, style='AAA.TFrame')
        label_1 = ttk.Label(self.frame1, text='ぱーふぇくとえふぇくとでーたべーす（仮）', foreground='red',background="black",font =("Helvetica",20)).pack()
        self.image_2a = tk.PhotoImage(file='dx3_logo.ppm')
        label_2 = ttk.Label(self.frame1, image=self.image_2a).pack()

        self.frame2 = ttk.Frame(self)
        label = ttk.Label(self.frame2, text='キーワード').grid(row= 0, column=1) 
        self.serch_keyword = ttk.Entry(self.frame2, width=50)
        self.serch_keyword.grid(row= 0, column=2)
        
        self.frame3 = ttk.Frame(self)
        label = ttk.Label(self.frame3, text='シンドローム').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
        self.syn_item = ["エンジェルハィロゥ","バロール","ブラックドッグ","ブラム＝ストーカー","キュマイラ","エグザイル","ハヌマーン","モルフェウス","ノイマン","オルクス","サラマンダー","ソラリス","ウロボロス","レネゲイドビーイング","一般"]
        self.syn_check = {}
        make_check_box(self.syn_item, self.syn_check, self.frame3)

        self.frame4 = ttk.Frame(self)
        label = ttk.Label(self.frame4, text='タイミング').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
        self.time_item = ["メジャー","マイナー","オート","常時","セットアップ","イニシアチブ","クリンナップ","リアクション","効果参照"]
        self.time_check = {}
        make_check_box(self.time_item, self.time_check, self.frame4)

        self.frame5 = ttk.Frame(self)
        label = ttk.Label(self.frame5, text='技能').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
        self.skl_item = ["―","〈白兵〉","〈射撃〉","〈RC〉","〈交渉〉","シンドローム","効果参照","〈回避〉","〈運転:〉","〈知覚〉","〈芸術:〉","〈意志〉","〈知識:〉","〈調達〉","〈情報:〉","【肉体】","【感覚】","【精神】","【社会】"]
        self.skl_check = {}
        make_check_box(self.skl_item, self.skl_check, self.frame5)

        self.frame6 = ttk.Frame(self)
        label = ttk.Label(self.frame6, text='対象').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
        self.trg_item = ["―","自身","単体","範囲","シーン","LV+1体","2体","3体","効果参照","解説参照"]
        self.trg_check = {}
        make_check_box(self.trg_item, self.trg_check, self.frame6)

        self.frame7 = ttk.Frame(self)
        label = ttk.Label(self.frame7, text='射程').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
        self.rng_item = ["―","至近","武器","視界","10m","20m","効果参照"]
        self.rng_check = {}
        make_check_box(self.rng_item, self.rng_check, self.frame7)

        self.frame8 = ttk.Frame(self)
        label = ttk.Label(self.frame8, text='制限').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
        self.lmt_item = ["―","80%","100%","120%","ピュア","リミット","従者専用","効果参照"]
        self.lmt_check = {}
        make_check_box(self.lmt_item, self.lmt_check, self.frame8)

        self.frame9 = ttk.Frame(self)
        label = ttk.Label(self.frame9, text='種別').grid(row= 0, column=0, sticky=tk.W+ tk.E) 
        self.knd_item = ["―","イージー","エネミー"]
        self.knd_check = {}
        make_check_box(self.knd_item, self.knd_check, self.frame9)

        self.frame10 = ttk.Frame(self)
        button = ttk.Button(self.frame10,
                        text = "戻る",
                        command = lambda: self.change_app("serch_frame", "main_frame")
                        ).grid(row=0, column=0, sticky="nsew", pady=2)
        button2 = ttk.Button(self.frame10,
                        text = "検索",
                        command = lambda: self.change_app("serch_frame", "result_frame")
                        ).grid(row=0, column=1, sticky="nsew", pady=2)
      
    # 検索画面の要素を設定だけする
    def create_result(self):
        #ここから検索結果画面
        self.label1_self = ttk.Label(self, text="検索結果")

        self.frame_serch_result = ttk.Frame(self, style='AAA.TFrame')

        column = ("エフェクト名","最大レベル","タイミング","技能","難易度","対象","射程","侵蝕値","制限","種別","効果")
        self.tree = ttk.Treeview(self.frame_serch_result, columns=column)
        self.tree.pack(expand=1, fill=tk.BOTH)

        # スクロールバーの追加
        scrollbar = ttk.Scrollbar(self.frame_serch_result, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.button_change_main_frame_s_result2 = ttk.Button(self, text="メインウィンドウに移動", command=lambda: self.change_app("result_frame", "serch_frame"))

        self.space_frame = ttk.Frame(self, style='AAA.TFrame') 
        label = ttk.Label(self.space_frame, padding=[10,self.canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)

        self.frame_input_error = ttk.Frame(self.frame_serch_result, style='AAA.TFrame')
        label_input_error = ttk.Label(self.frame_serch_result, text="検索条件を入力、選択してください！", font=40).pack(expand=1, fill=tk.BOTH, pady=2)
        self.frame_input_error.pack(expand=1, fill=tk.BOTH)

    # 画面遷移の処理
    def change_app(self, nowwindow, towindow):
        self.main_frames = [self.frame_titl, self.frame_serch, self.frame_com_serch]
        self.serch_frames = [self.frame1,self.frame2,self.frame3,self.frame4,self.frame5,self.frame6,self.frame7,self.frame8,self.frame9,self.frame10]
        self.result_frames = [self.label1_self, self.frame_serch_result, self.button_change_main_frame_s_result2 ,self.space_frame, self.frame_input_error]
        if towindow == "result_frame":
            ttk.Style().configure("AAA.TFrame", background="#DCDAD5")
            for f in self.result_frames:
                f.destroy()
            self.serch_ef(nowwindow)
            for f in self.serch_frames:
                f.pack_forget()
            for f in self.main_frames:
                f.pack_forget()
        if towindow == "serch_frame":
            ttk.Style().configure("AAA.TFrame", background="black")
            for f in self.result_frames:
                f.destroy()
            self.canvas.config(scrollregion=(0,0,800,600))
            for f in self.serch_frames:
                f.pack(anchor=tk.N, expand=1, fill=tk.BOTH, pady=2)
            for f in self.main_frames:
                f.pack_forget()
        if towindow == "main_frame":
            ttk.Style().configure("AAA.TFrame", background="black")
            self.frame_titl.pack(anchor=tk.N, fill=tk.BOTH, pady=2)
            self.frame_serch.pack(anchor=tk.N, fill=tk.X, pady=2)
            self.frame_com_serch.pack(anchor=tk.N, expand=1, fill=tk.X, pady=2)
            for f in self.serch_frames:
                f.pack_forget()
        self.tkraise()

    # 検索の処理
    def serch_ef(self, nowwindow):
        c_list = [self.syn_check, self.time_check, self.skl_check, self.trg_check, self.rng_check, self.lmt_check, self.knd_check]
        i_list = [self.syn_item, self.time_item, self.skl_item, self.trg_item, self.rng_item, self.lmt_item, self.knd_item]
        pick_list = ["syndrome", "timing", "skill", "target", "range", "limited", "kinds"]
        con = sqlite3.connect("dx_ef_list.db")
        cur = con.cursor()
        select_ef = "SELECT name, level, timing, skill, diffculty, target, range, cost, limited, kinds, effect FROM dx_ef_list"
        dex = 0
        if nowwindow == "serch_frame":
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
        if nowwindow == "serch_frame":
            keyword = self.serch_keyword.get()
        elif nowwindow == "main_frame":
            keyword = self.serch_keyword1.get()
        keyword = keyword.replace('　',' ')
        keyword_list = keyword.split(' ')
        select_letter = ""
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
        self.label1_self = ttk.Label(self, text="検索結果")
        self.label1_self.pack()
        self.button_change_main_frame_s_result2 = ttk.Button(self, text="メインウィンドウに移動", command=lambda: self.change_app("result_frame", "serch_frame"))
        self.button_change_main_frame_s_result2.pack()
        if select_ef != "SELECT name, level, timing, skill, diffculty, target, range, cost, limited, kinds, effect FROM dx_ef_list":
            cur.execute(select_ef)
            ef_list = cur.fetchall()
            if len(ef_list) == 0:
                self.frame_input_error.destroy()
                self.space_frame.destroy()
                self.frame_input_error = ttk.Frame(self, style='AAA.TFrame')
                self.frame_input_error.pack()
                label_input_error = ttk.Label(self.frame_input_error, text="条件に一致するエフェクトがありません！", font=40).pack(expand=1, fill=tk.BOTH, pady=2)
                self.space_frame = ttk.Frame(self, style='AAA.TFrame') 
                label = ttk.Label(self.space_frame, padding=[10,self.canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)
                self.space_frame.pack(expand=1, fill=tk.BOTH)
            else:
                self.make_result(ef_list, nowwindow)
        else:
            self.frame_input_error.destroy()
            self.space_frame.destroy()
            self.frame_input_error = ttk.Frame(self, style='AAA.TFrame')
            self.frame_input_error.pack()
            label_input_error = ttk.Label(self.frame_input_error, text="検索条件を入力、選択してください！", font=40).pack(expand=1, fill=tk.BOTH, pady=2)
            self.space_frame = ttk.Frame(self, style='AAA.TFrame') 
            label = ttk.Label(self.space_frame, padding=[10,self.canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)
            self.space_frame.pack(expand=1, fill=tk.BOTH)


    # 検索結果を表示する
    def make_result(self, result_list, nowwindow):
        self.frame_serch_result.destroy()
        self.space_frame.destroy()
        self.frame_serch_result = ttk.Frame(self, style='AAA.TFrame')
        self.frame_serch_result.pack(expand=1, fill=tk.BOTH)
        columns = ("エフェクト名","最大レベル","タイミング","技能","難易度","対象","射程","侵蝕値","制限","種別","効果")
        self.tree = ttk.Treeview(self.frame_serch_result, columns=columns)
        self.tree.bind("<<TreeviewSelect>>", self.make_effect)
        self.tree.column('#0',width=0, stretch='no')
        font1 = tkFont.Font(family='Meiryo', size=7)
        style_tree = ttk.Style()
        style_tree.configure("Treeview.Heading", font=('Meiryo', 8, "bold"))
        style_tree.configure("Treeview", font=('Meiryo', 7, "bold"), relief="SOLID")
        fixture_treeview_tag_config(style_tree)
        self.tree.tag_configure('odd', background='#eeeeee')
        self.tree.tag_configure('even', background='#DFDFDF')
        for col_name in columns:
            self.tree.heading(col_name, text=col_name)
            width1 = font1.measure(col_name)+11
            self.tree.column(col_name, width=width1+10)
        for i, _ in enumerate(result_list[0]):
            if i != 10:
                max_str = max([x[i] for x in result_list], key=lambda x:len(str(x))) or "    "
                if type(max_str) is str:
                    max_str = max(max_str.split("\n"), key=len)
                width1 = font1.measure(max_str) + 16
                header1 = self.tree.column(self.tree['columns'][i], width=None)
                if width1 > header1:
                    self.tree.column(self.tree['columns'][i], width=width1)
        fill_width = 0
        for i in range(len(result_list[0])):
            if i != 10:
                fill_width += self.tree.column(self.tree['columns'][i], width=None)
        effect_width = int(self.canvas.cget("width")) - fill_width - 16
        self.tree.column(self.tree['columns'][10], width = effect_width)
        cells = []
        column_e_width = self.tree.column(self.tree['columns'][10], width=None)
        for i, result in enumerate(result_list):
            info_list = list(result)
            tag = ["odd", "even"][i % 2]
            text_ef_n = ""
            width_text_ef = 0
            count_t_n = 0
            for j, t in enumerate(info_list[10]):
                width_text_ef += font1.measure(t)
                if (width_text_ef+10) > column_e_width:
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
                            break
                else:
                    for k in range(count_t_n):
                        width_text_ef = font1.measure(info_list[10][f_ad_text:f_ad_text+count_t_n+k])
                        if (width_text_ef+10) > column_e_width:
                            text_ef_n += info_list[10][f_ad_text:f_ad_text+count_t_n+k-1] + "\n"
                            f_ad_text = f_ad_text + count_t_n + k - 1
                            break
                        else:
                            if f_ad_text+count_t_n+k >= len(info_list[10]):
                                text_ef_n += info_list[10][f_ad_text:]
                                f_ad_text = f_ad_text + count_t_n + k
                                break

            info_list[10] = text_ef_n
            self.tree.insert(parent="", index="end", values=info_list, tags=(tag,))
            cells.append(info_list[10])
        longest_cell = max(cells, key=lambda x:x.count("\n"))
        max_row_lines = longest_cell.count("\n") + 1   
        style_tree.configure("Treeview", rowheight = 14 * max_row_lines)
        self.tree.configure(height= (int(self.canvas.cget("height"))-77)//(14 * max_row_lines))
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        style_scbar = ttk.Style()
        style_scbar.configure("Scrollbar", width=16)
        scrollbar = ttk.Scrollbar(self.frame_serch_result, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=1)

        self.space_frame = ttk.Frame(self, style='AAA.TFrame') 
        label = ttk.Label(self.space_frame, padding=[10,self.canvas.cget('height'),10]).pack(expand=1, fill=tk.BOTH)
        self.space_frame.pack(expand=1, fill=tk.BOTH)

    # エフェクトの詳細を表示する
    def make_effect(self, event):
        self.result_frames = [self.label1_self, self.frame_serch_result, self.button_change_main_frame_s_result2 ,self.space_frame, self.frame_input_error]
        for f in self.result_frames:
            f.pack_forget()
        record_id = self.tree.focus()
        effect_info = self.tree.item(record_id, 'values')
        effect_name = effect_info[0]
        print(effect_name)
        con = sqlite3.connect("dx_ef_list.db")
        cur = con.cursor()
        s2 = ttk.Style()
        s2.configure('BBB.TFrame', background='white')
        frame_effect_info = ttk.Frame(self, style='BBB.TFrame')
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
        button = ttk.Button(frame_effect_info, text="戻る", command=lambda: self.eraser(frame_effect_info), style='CCC.TButton').pack()#.grid(row=10, column=0, columnspan=2, sticky="nesw")
        frame_effect_info.pack(anchor=tk.CENTER, expand=1, fill=tk.BOTH)

    # エフェクト詳細画面を閉じて検索結果を表示する
    def eraser(self, frame_d):
        frame_d.destroy()
        self.label1_self.pack()
        self.button_change_main_frame_s_result2.pack()
        self.frame_serch_result.pack(expand=1, fill=tk.BOTH)
        self.space_frame.pack(expand=1, fill=tk.BOTH)

# 実際に動かす
root = tk.Tk()

s = ttk.Style()
s.theme_use('clam')
s.configure('AAA.TFrame', background='black')

root.geometry('980x600') 
root.resizable(True, True)
root.title('DX3rdぱーふぇくとえふぇくとでーたべーす（仮）')
root.iconbitmap('dx3_logo.ico')
root.configure(bg="black")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Canvas Widget を生成
canvas = tk.Canvas(root, width = root.winfo_width(), height = root.winfo_height())
canvas.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

main_frame = MainFrame(canvas)

main_frame.pack(expand=1, fill=tk.BOTH)
main_frame.tkraise()
root.mainloop()