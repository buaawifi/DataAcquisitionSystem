import serial
from modules.logger import get_logger

# 创建日志记录器
run_logger = get_logger(__name__, "run")  # 运行日志
debug_logger = get_logger(__name__, "debug")  # 调试日志


def initialize_rs485(port: str, baudrate: int) -> serial.Serial:
    """
    初始化 RS485 通讯端口。
    Args:
        port (str): 串口名称，例如 'COM3' 或 '/dev/ttyUSB0'。
        baudrate (int): 波特率，例如 9600。
    Returns:
        serial.Serial: 已初始化的串口对象。
    """
    try:
        run_logger.info(f"Initializing RS485 on port: {port} with baudrate: {baudrate}")
        debug_logger.debug(f"Attempting to initialize RS485: port={port}, baudrate={baudrate}")
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1  # 设置超时时间为 1 秒
        )
        if ser.is_open:
            run_logger.info(f"RS485 Port {port} initialized successfully.")
            debug_logger.debug(f"RS485 connection established on port {port}.")
            return ser
        else:
            raise serial.SerialException(f"Failed to open RS485 port: {port}")
    except Exception as e:
        run_logger.error(f"Error initializing RS485 port: {e}")
        debug_logger.exception("Detailed error during RS485 initialization:")
        raise


def send_command(ser: serial.Serial, command: str) -> str:
    """
    发送指令到流量计并接收响应。
    Args:
        ser (serial.Serial): 已初始化的串口对象。
        command (str): ASCII 指令，例如 'A' 或 'AS2.75'。
    Returns:
        str: 流量计的响应字符串。
    """
    try:
        command_with_appendix = f"{command}\r".encode("ascii")  # 在命令末尾添加固定附加位 0D（\r）
        ser.write(command_with_appendix)
        debug_logger.debug(f"Command sent: {command} (encoded: {command_with_appendix})")
        response = ser.readline().decode("ascii", errors="ignore").strip()
        run_logger.info(f"Command sent: {command}, Response received: {response}")
        debug_logger.debug(f"Raw response received: {response}")
        return response
    except Exception as e:
        run_logger.error(f"Error in RS485 communication: {e}")
        debug_logger.exception("Detailed error during RS485 communication:")
        raise


def parse_response(response: str) -> dict:
    """
    解析流量计返回的响应数据。
    Args:
        response (str): 流量计返回的响应字符串。
    Returns:
        dict: 包含解析后的数据。
    """
    try:
        parts = response.split()
        debug_logger.debug(f"Response parts after split: {parts}")
        if len(parts) >= 6:
            result = {
                "device_id": parts[0],
                "pressure": float(parts[1]),
                "temperature": float(parts[2]),
                "volumetric_flow": float(parts[3]),
                "mass_flow": float(parts[4]),
                "gas_type": parts[5]
            }
            run_logger.info(f"Parsed response successfully: {result}")
            debug_logger.debug(f"Detailed parsed response: {result}")
            return result
        else:
            raise ValueError(f"Invalid response format. Expected at least 6 fields but got {len(parts)}. Raw response: {response}")
    except Exception as e:
        run_logger.error(f"Error parsing response: {e}")
        debug_logger.exception("Detailed error during response parsing:")
        raise


if __name__ == "__main__":
    import sys

    print("RS485 Module Manual Testing")
    print("===========================")
    try:
        port = input("Enter RS485 port (e.g., COM3): ").strip()
        baudrate = int(input("Enter baudrate (e.g., 9600): ").strip())
        rs485 = initialize_rs485(port, baudrate)

        while True:
            command = input("Enter command to send (or 'exit' to quit): ").strip()
            if command.lower() == "exit":
                print("Exiting manual testing.")
                break
            try:
                response = send_command(rs485, command)
                print(f"Raw Response: {response}")
                parsed_response = parse_response(response)
                print("Parsed Response:")
                for key, value in parsed_response.items():
                    print(f"  {key}: {value}")
            except Exception as e:
                print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nManual testing interrupted.")
    except Exception as e:
        print(f"Error during manual testing: {e}")
