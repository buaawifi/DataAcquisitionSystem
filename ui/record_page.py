import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from modules.data_processor import DataProcessor

class RecordPage(tk.Frame):
    def __init__(self, parent, config_path, output_path):
        super().__init__(parent)
        self.processor = DataProcessor(config_path, output_path)
        self.is_recording = False
        self.data = []

        # 创建按钮
        self.start_button = tk.Button(self, text="开始记录", command=self.toggle_recording)
        self.start_button.pack()

        # 创建图表
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("体积流量 vs 时间")
        self.ax.set_xlabel("时间")
        self.ax.set_ylabel("体积流量")
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack()

    def toggle_recording(self):
        if self.is_recording:
            self.processor.stop_recording()
            self.is_recording = False
            self.start_button.config(text="开始记录")
        else:
            self.is_recording = True
            self.start_button.config(text="停止记录")
            self.processor.start_recording(self.update_plot)

    def update_plot(self, timestamp, flow_rate):
        self.data.append((timestamp, flow_rate))
        self.ax.clear()
        times, flow_rates = zip(*self.data[-50:])  # 只显示最近 50 条记录
        self.ax.plot(times, flow_rates, marker='o')
        self.ax.set_title("体积流量 vs 时间")
        self.ax.set_xlabel("时间")
        self.ax.set_ylabel("体积流量")
        self.canvas.draw()
