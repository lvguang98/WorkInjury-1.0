import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow  # 更新导入路径
from config import Config
from utils.logger import setup_logging


def main():
    # 初始化配置和日志
    config = Config()
    setup_logging()

    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("工伤助手")
    app.setApplicationVersion("1.0.0")

    # 创建主窗口
    window = MainWindow(config)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = Config()
    window = MainWindow(config)
    window.show()
    sys.exit(app.exec_())