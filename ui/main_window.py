from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from config import Config
from core.services import CaseService


class MainWindow(QMainWindow):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.case_service = CaseService(config.get_database_path())
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """初始化界面"""
        self.setWindowTitle("工伤助手")
        self.resize(*self.config.data["ui"]["window_size"])

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.title_label = QLabel("工伤案件管理系统")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addStretch(1)
        layout.addWidget(self.status_label)

    def _connect_signals(self):
        """连接信号槽"""
        pass

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存窗口大小
        self.config.data["ui"]["window_size"] = [self.width(), self.height()]
        self.config.save()
        super().closeEvent(event)