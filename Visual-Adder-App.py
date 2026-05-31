import tkinter as tk

# --- 論理ゲートのロジック ---
def half_adder(a, b):
    s = a ^ b
    c = a & b
    return s, c

def full_adder(a, b, cin):
    s1, c1 = half_adder(a, b)
    s2, c2 = half_adder(s1, cin)
    cout = c1 | c2
    return s2, cout

# --- GUIアプリケーション ---
class VisualAdderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("可視化機能付き 加算器シミュレータ")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # 状態保持用変数
        self.var_a = tk.IntVar(value=0)
        self.var_b = tk.IntVar(value=0)
        self.var_cin = tk.IntVar(value=0)
        self.mode = tk.StringVar(value="HA") # "HA": 半加算器, "FA": 全加算器

        self.create_widgets()
        self.update_circuit()

    def create_widgets(self):
        # 1. コントロールパネル（上部）
        frame_ctrl = tk.LabelFrame(self.root, text=" 入力コントロール ", font=("Helvetica", 12, "bold"), padx=10, pady=10)
        frame_ctrl.pack(fill="x", padx=15, pady=10)

        # モード切替
        tk.Label(frame_ctrl, text="回路選択:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        tk.Radiobutton(frame_ctrl, text="半加算器 (Half Adder)", variable=self.mode, value="HA", command=self.update_circuit).grid(row=0, column=1, sticky="w")
        tk.Radiobutton(frame_ctrl, text="全加算器 (Full Adder)", variable=self.mode, value="FA", command=self.update_circuit).grid(row=0, column=2, sticky="w")

        # 入力スイッチ
        tk.Label(frame_ctrl, text="信号入力 (ON=1):", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.chk_a = tk.Checkbutton(frame_ctrl, text="入力 A", variable=self.var_a, command=self.update_circuit)
        self.chk_a.grid(row=1, column=1, sticky="w")
        
        self.chk_b = tk.Checkbutton(frame_ctrl, text="入力 B", variable=self.var_b, command=self.update_circuit)
        self.chk_b.grid(row=1, column=2, sticky="w")
        
        self.chk_cin = tk.Checkbutton(frame_ctrl, text="下位桁上げ (Cin)", variable=self.var_cin, command=self.update_circuit)
        self.chk_cin.grid(row=1, column=3, sticky="w")

        # 2. キャンバスエリア（下部：ここに回路図を描画）
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)

    def get_color(self, val):
        """信号が1なら赤（通電）、0なら黒（非通電）のカラーコードを返す"""
        return "#FF3333" if val == 1 else "#333333"

    def draw_block(self, x, y, width, height, text, bg_color="#E0F7FA"):
        """回路のブロック（半加算器など）を描画する補助関数"""
        self.canvas.create_rectangle(x, y, x + width, y + height, fill=bg_color, outline="black", width=2)
        self.canvas.create_text(x + width/2, y + height/2, text=text, font=("Helvetica", 11, "bold"))

    def update_circuit(self):
        """入力を読み込み、計算して回路図を再描画するメイン処理"""
        self.canvas.delete("all")  # 画面を一度クリア
        
        a = self.var_a.get()
        b = self.var_b.get()
        cin = self.var_cin.get()
        mode = self.mode.get()

        if mode == "HA":
            # --- 半加算器の処理 ---
            self.chk_cin.config(state="disabled") # Cinを無効化
            s, c = half_adder(a, b)
            
            # タイトル
            self.canvas.create_text(100, 25, text="【半加算器 回路ブロック】", font=("Helvetica", 12, "bold"), anchor="w")

            # 入力線の描画（色が変わる）
            self.canvas.create_line(50, 80, 150, 80, fill=self.get_color(a), width=3)
            self.canvas.create_text(40, 80, text=f"A = {a}", anchor="e", font=("Helvetica", 11, "bold"))
            
            self.canvas.create_line(50, 140, 150, 140, fill=self.get_color(b), width=3)
            self.canvas.create_text(40, 140, text=f"B = {b}", anchor="e", font=("Helvetica", 11, "bold"))

            # 半加算器本体のボックス
            self.draw_block(150, 50, 140, 130, "半加算器\n(Half Adder)", "#E3F2FD")

            # 出力線の描画
            self.canvas.create_line(290, 80, 400, 80, fill=self.get_color(s), width=3)
            self.canvas.create_text(410, 80, text=f"Sum (和) = {s}", anchor="w", font=("Helvetica", 11, "bold"), fill="blue")
            
            self.canvas.create_line(290, 140, 400, 140, fill=self.get_color(c), width=3)
            self.canvas.create_text(410, 140, text=f"Carry (桁上げ) = {c}", anchor="w", font=("Helvetica", 11, "bold"), fill="orange")

        else:
            # --- 全加算器の処理 ---
            self.chk_cin.config(state="normal") # Cinを有効化
            
            # 内部の挙動を計算
            s1, c1 = half_adder(a, b)
            s2, c2 = half_adder(s1, cin)
            cout = c1 | c2

            self.canvas.create_text(100, 25, text="【全加算器 構成図（2つの半加算器とORゲート）】", font=("Helvetica", 12, "bold"), anchor="w")

            # 入力 A, B -> HA1
            self.canvas.create_line(40, 80, 120, 80, fill=self.get_color(a), width=3)
            self.canvas.create_text(35, 80, text=f"A={a}", anchor="e", font=("Helvetica", 10, "bold"))
            self.canvas.create_line(40, 120, 120, 120, fill=self.get_color(b), width=3)
            self.canvas.create_text(35, 120, text=f"B={b}", anchor="e", font=("Helvetica", 10, "bold"))
            
            # 半加算器 1
            self.draw_block(120, 60, 100, 90, "半加算器 1")

            # HA1 からの出力 (S1 -> HA2へ, C1 -> ORゲートへ)
            self.canvas.create_line(220, 80, 300, 80, fill=self.get_color(s1), width=3) # S1
            self.canvas.create_line(220, 130, 260, 130, fill=self.get_color(c1), width=3)
            self.canvas.create_line(260, 130, 260, 240, fill=self.get_color(c1), width=3)
            self.canvas.create_line(260, 240, 460, 240, fill=self.get_color(c1), width=3) # C1 -> OR

            # 入力 Cin -> HA2
            self.canvas.create_line(40, 170, 280, 170, fill=self.get_color(cin), width=3)
            self.canvas.create_line(280, 170, 280, 120, fill=self.get_color(cin), width=3)
            self.canvas.create_line(280, 120, 300, 120, fill=self.get_color(cin), width=3) # Cin -> HA2
            self.canvas.create_text(35, 170, text=f"Cin={cin}", anchor="e", font=("Helvetica", 10, "bold"))

            # 半加算器 2
            self.draw_block(300, 60, 100, 90, "半加算器 2")

            # HA2 からの出力 (S2 -> 最終Sum, C2 -> ORゲートへ)
            self.canvas.create_line(400, 80, 580, 80, fill=self.get_color(s2), width=3) # 最終Sum
            self.canvas.create_text(590, 80, text=f"Sum (和) = {s2}", anchor="w", font=("Helvetica", 11, "bold"), fill="blue")

            self.canvas.create_line(400, 130, 420, 130, fill=self.get_color(c2), width=3)
            self.canvas.create_line(420, 130, 420, 200, fill=self.get_color(c2), width=3)
            self.canvas.create_line(420, 200, 460, 200, fill=self.get_color(c2), width=3) # C2 -> OR

            # OR ゲート
            self.draw_block(460, 190, 80, 70, "OR ゲート", "#FFF9C4")

            # 最終桁上げ Cout
            self.canvas.create_line(540, 225, 580, 225, fill=self.get_color(cout), width=3)
            self.canvas.create_text(590, 225, text=f"Cout (桁上げ) = {cout}", anchor="w", font=("Helvetica", 11, "bold"), fill="orange")

# アプリケーションの起動
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualAdderApp(root)
    root.mainloop()
