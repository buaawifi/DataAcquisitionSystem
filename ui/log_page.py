import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class LogPage(tk.Frame):
    def __init__(self, parent, log_path):
        super().__init__(parent)
        self.log_path = log_path

        # 创建滚动文本框用于显示日志
        self.text_area = ScrolledText(self, wrap=tk.WORD, height=20, width=80)
        self.text_area.pack(fill="both", expand=True)

        # 创建刷新按钮
        self.refresh_button = tk.Button(self, text="刷新日志", command=self.load_logs)
        self.refresh_button.pack()

        # 加载日志
        self.load_logs()

    def load_logs(self):
        try:
            with open(self.log_path, 'r') as log_file:
                logs = log_file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, logs)
        except FileNotFoundError:
            self.text_area.insert(tk.END, "日志文件未找到！")
