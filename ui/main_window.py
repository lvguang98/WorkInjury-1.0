from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QAction)

from utils.config import Config
from core.services import CaseService
from ui.new_case_window import NewCaseWindow


class MainWindow(QMainWindow):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.case_service = CaseService(config.get_database_path())
        self._init_ui()
        self._init_menu()  # 新增菜单初始化方法
        self._connect_signals()

    def _init_ui(self):
        """简化后的界面初始化"""
        self.setWindowTitle("工伤助手")
        self.resize(*self.config.data["ui"]["window_size"])

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.title_label = QLabel("工伤案件管理系统")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title_label)

    def _connect_signals(self):
        """连接信号槽"""
        pass

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存窗口大小
        self.config.data["ui"]["window_size"] = [self.width(), self.height()]
        self.config.save()
        super().closeEvent(event)

    def _init_menu(self):
        """初始化菜单栏"""
        menubar = self.menuBar()

        # 创建"案件"主菜单
        case_menu = menubar.addMenu("案件")

        # 添加"新建案件"动作
        new_case_action = QAction("新建案件", self)
        new_case_action.triggered.connect(self._on_new_case)
        case_menu.addAction(new_case_action)

    def _on_new_case(self):
        """新建案件菜单点击事件"""
        self.new_case_window = NewCaseWindow(self)  # 创建新窗口
        self.new_case_window.show()  # 显示新窗口