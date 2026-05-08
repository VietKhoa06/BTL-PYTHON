import tkinter as tk
from tkinter import messagebox, ttk
import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlayerCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("So sanh chi so 2 cau thu")
        self.root.geometry("900x700")

        self.api_url = "http://127.0.0.1:5000/api/player"
        self.players_data = [None, None]
        self.stats_columns = ['90s', 'CrdY', 'CrdR', 'Fls', 'Fld', 'Off', 'Crs', 'Int', 'TklW', 'OG']
        self.check_vars = {}
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Player 1:").grid(row=0, column=0)
        self.ent_p1 = tk.Entry(input_frame)
        self.ent_p1.grid(row=0, column=1, padx=5)
        tk.Button(input_frame, text="Search", command=lambda: self.search_player(0)).grid(row=0, column=2)

        tk.Label(input_frame, text="Player 2:").grid(row=0, column=3, padx=(20, 0))
        self.ent_p2 = tk.Entry(input_frame)
        self.ent_p2.grid(row=0, column=4, padx=5)
        tk.Button(input_frame, text="Search", command=lambda: self.search_player(1)).grid(row=0, column=5)

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        self.stats_frame = tk.Frame(self.result_frame)
        self.stats_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.root, text="So sánh / Compare", bg="green", fg="white",
                  font=('Arial', 12, 'bold'), command=self.draw_radar_chart).pack(pady=10)

    def search_player(self, idx):
        name = self.ent_p1.get() if idx == 0 else self.ent_p2.get()
        if not name:
            messagebox.showwarning("Chú ý", "Vui lòng nhập tên cầu thủ")
            return

        try:
            response = requests.get(self.api_url, params={'name': name})
            if response.status_code == 200:
                data = response.json()['data']
                self.players_data[idx] = data
                self.display_stats()
            else:
                messagebox.showerror("Lỗi", response.json().get('message', 'Không tìm thấy'))
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới API: {e}")

    def display_stats(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        tk.Label(self.stats_frame, text="Chỉ số", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w')
        tk.Label(self.stats_frame, text="Cầu thủ 1", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=20)
        tk.Label(self.stats_frame, text="Cầu thủ 2", font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=20)

        for i, col in enumerate(self.stats_columns):
            if col not in self.check_vars:
                self.check_vars[col] = tk.BooleanVar(value=True)

            tk.Checkbutton(self.stats_frame, text=col, variable=self.check_vars[col]).grid(row=i + 1, column=0,
                                                                                           sticky='w')
            val1 = self.players_data[0].get(col, "N/a") if self.players_data[0] else "-"
            tk.Label(self.stats_frame, text=val1).grid(row=i + 1, column=1)

            val2 = self.players_data[1].get(col, "N/a") if self.players_data[1] else "-"
            tk.Label(self.stats_frame, text=val2).grid(row=i + 1, column=2)

    def draw_radar_chart(self):
        if not self.players_data[0] or not self.players_data[1]:
            messagebox.showwarning("Chú ý", "Vui lòng tìm kiếm đủ 2 cầu thủ để so sánh")
            return

        selected_stats = [s for s in self.stats_columns if self.check_vars[s].get()]
        if len(selected_stats) < 3:
            messagebox.showwarning("Chú ý", "Vui lòng chọn ít nhất 3 chỉ số để vẽ biểu đồ radar")
            return

        labels = np.array(selected_stats)
        values1 = [float(self.players_data[0].get(s, 0)) for s in selected_stats]
        values2 = [float(self.players_data[1].get(s, 0)) for s in selected_stats]

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values1 += values1[:1]
        values2 += values2[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

        ax.fill(angles, values1, color='red', alpha=0.25)
        ax.plot(angles, values1, color='red', linewidth=2, label=self.players_data[0]['Player'])

        ax.fill(angles, values2, color='blue', alpha=0.25)
        ax.plot(angles, values2, color='blue', linewidth=2, label=self.players_data[1]['Player'])

        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.title("So sánh chỉ số cầu thủ", size=15, color='black', y=1.1)

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Radar Chart Comparison")

        chart_window.state('zoomed')

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerCompareApp(root)
    root.mainloop()