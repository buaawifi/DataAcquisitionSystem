from ui.main_ui import MainUI

if __name__ == "__main__":
    config_path = "config/config.json"
    output_path = "data/recorded_data.xlsx"
    log_path = "data/logs.txt"

    app = MainUI(config_path, output_path, log_path)
    app.mainloop()
