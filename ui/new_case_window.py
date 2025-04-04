from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton,
                             QHBoxLayout, QWidget, QRadioButton, QButtonGroup,
                             QComboBox, QMessageBox)
from PyQt5.QtCore import Qt


class NewCaseWindow(QDialog):
    IDENTITY_MAP = {
        1: "本人",
        2: "证人",
        3: "法人"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建工伤案件")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.resize(450, 350)
        self._init_ui()
        self._connect_identity_signals()

    def _connect_identity_signals(self):
        """连接身份切换的信号"""
        self.identity_self.toggled.connect(self._validate_identity_switch)
        self.identity_witness.toggled.connect(self._validate_identity_switch)
        self.identity_legal.toggled.connect(self._validate_identity_switch)

    def _validate_identity_switch(self, checked):
        """
        验证身份切换
        :param checked: 按钮是否被选中
        """
        # 只有从"本人"切出时才需要验证
        if (self.identity_witness.isChecked() or self.identity_legal.isChecked()) and checked:
            if not self.name_edit.text().strip():
                QMessageBox.warning(self, "提示", "请先填写受伤职工本人姓名")

                # 阻止切换：强制切回"本人"
                self.identity_self.setChecked(True)
                return False
        return True

    def _init_ui(self):
        layout = QFormLayout()
        self.setLayout(layout)

        # 1. 案件状态选择
        self.case_status = QComboBox(self)
        self.case_status.addItems(["正常案件", "个人案件", "死亡案件"])
        layout.addRow("案件状态:", self.case_status)

        # 2. 身份类型单选组
        self.identity_group = QButtonGroup(self)
        hbox = QHBoxLayout()

        self.identity_self = QRadioButton("本人", self)
        self.identity_witness = QRadioButton("证人", self)
        self.identity_legal = QRadioButton("法人", self)

        self.identity_group.addButton(self.identity_self, 1)
        self.identity_group.addButton(self.identity_witness, 2)
        self.identity_group.addButton(self.identity_legal, 3)
        self.identity_self.setChecked(True)

        hbox.addWidget(self.identity_self)
        hbox.addWidget(self.identity_witness)
        hbox.addWidget(self.identity_legal)
        hbox.addStretch()

        identity_widget = QWidget(self)
        identity_widget.setLayout(hbox)
        layout.addRow("身份类型:", identity_widget)

        # 3. 其他字段（全部指定父对象）
        self.name_edit = QLineEdit(self)
        self.id_edit = QLineEdit(self)
        self.phone_edit = QLineEdit(self)
        self.position_edit = QLineEdit(self)

        layout.addRow("受伤职工姓名:", self.name_edit)
        layout.addRow("身份证号:", self.id_edit)
        layout.addRow("联系电话:", self.phone_edit)
        layout.addRow("工作岗位:", self.position_edit)

        # 4. 提交按钮
        submit_btn = QPushButton("提交", self)
        submit_btn.clicked.connect(self._on_submit)
        layout.addRow(submit_btn)

    def _on_submit(self):
        """获取并验证所有字段数据"""
        identity = self.IDENTITY_MAP.get(self.identity_group.checkedId(), "本人")

        data = {
            "status": self.case_status.currentText(),
            "identity": identity,
            "name": self.name_edit.text().strip(),
            "id": self.id_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "position": self.position_edit.text().strip()
        }

        # 简单验证示例
        if not data["name"]:
            QMessageBox.warning(self, "错误", "姓名不能为空")
            return

        print("案件数据:", data)
        self.accept()