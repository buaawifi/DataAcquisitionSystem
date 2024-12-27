import logging
import os

# 获取日志目录
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 定义日志文件路径
RUN_LOG_FILE = os.path.join(LOG_DIR, "data_acquisition_system.log")  # 运行日志
DEBUG_LOG_FILE = os.path.join(LOG_DIR, "debug.log")                  # 调试日志

def get_logger(name: str, log_type: str = "run") -> logging.Logger:
    """
    获取配置好的日志记录器。
    Args:
        name (str): 调用日志记录器的模块名。
        log_type (str): 日志类型，可选值为 "run" 或 "debug"。
    Returns:
        logging.Logger: 配置好的日志记录器。
    """
    logger = logging.getLogger(f"{name}_{log_type}")
    logger.setLevel(logging.DEBUG if log_type == "debug" else logging.INFO)

    # 防止重复添加处理器
    if not logger.handlers:
        if log_type == "run":
            # 运行日志处理器
            file_handler = logging.FileHandler(RUN_LOG_FILE, mode='a')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s'))
            logger.addHandler(file_handler)

        elif log_type == "debug":
            # 调试日志处理器
            file_handler = logging.FileHandler(DEBUG_LOG_FILE, mode='a')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s'))
            logger.addHandler(file_handler)

        # 控制台处理器（仅用于调试日志）
        if log_type == "debug":
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s'))
            logger.addHandler(console_handler)

    return logger
