import tkinter as tk
from ui.record_page import RecordPage
from ui.log_page import LogPage

class MainUI(tk.Tk):
    def __init__(self, config_path, output_path, log_path):
        super().__init__()
        self.title("数据采集系统")
        self.geometry("800x600")

        # 配置路径
        self.config_path = config_path
        self.output_path = output_path
        self.log_path = log_path

        # 创建菜单栏
        self.create_menu()

        # 容器管理所有子页面
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # 子页面字典
        self.pages = {}
        self.create_pages()

        # 默认显示数据记录页面
        self.show_page("RecordPage")

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # 添加功能菜单
        menu = tk.Menu(menu_bar, tearoff=0)
        menu.add_command(label="数据记录", command=lambda: self.show_page("RecordPage"))
        menu.add_command(label="日志查看", command=lambda: self.show_page("LogPage"))
        menu_bar.add_cascade(label="功能", menu=menu)

    def create_pages(self):
        # 初始化所有子页面
        self.pages["RecordPage"] = RecordPage(self.container, self.config_path, self.output_path)
        self.pages["LogPage"] = LogPage(self.container, self.log_path)

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        # 切换子页面
        page = self.pages[page_name]
        page.tkraise()
