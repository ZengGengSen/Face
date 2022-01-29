from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMessageBox
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QKeyEvent
from dialog import Ui_Form
import detector
import database
import os
import sys
import cv2
import qss


class AddDataWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(AddDataWidget, self).__init__(parent)
        self.setupUi(self)
        self.browse.clicked.connect(self.browse_click_slot)
        self.confirm.clicked.connect(self.confirm_click_slot)
        self.cancel.clicked.connect(self.close)
        self.setStyleSheet(qss.qssStyle)

    def browse_click_slot(self):
        file_path = QFileDialog.getOpenFileName(self, "请选择图片文件", "./", "All Files (*)")
        if file_path[0]:
            self.img_path.setText(file_path[0])
            self.img_name.setText(os.path.basename(file_path[0]))

    def confirm_click_slot(self):
        image_path = self.img_path.text()
        fi = QFileInfo(image_path)
        if fi.isFile():
            image = cv2.imread(image_path)
            if image is not None:
                image = cv2.resize(image, (640, 480))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                feature = detector.dt.ext_feature(image)
                if feature is not None:
                    if self.img_name.text() != "":
                        database.db.insert_data(self.img_name.text(), image, feature)
                        QMessageBox.information(
                            self,
                            '提示',
                            '添加数据库数据成功',
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.Yes
                        )
                    else:
                        QMessageBox.warning(
                            self,
                            '警告',
                            '请输入正确的名称',
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.Yes
                        )
                else:
                    QMessageBox.warning(
                        self,
                        '警告',
                        '无法提取图片特征',
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes
                    )
            else:
                QMessageBox.warning(
                    self,
                    '警告',
                    '无法打开图片，请确认图片路径是否正确，无法支持中文',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
        else:
            QMessageBox.warning(
                self,
                '警告',
                '请输入正确的路径',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

    def keyPressEvent(self, event: QKeyEvent) -> None:
        k = event.key()
        if Qt.Key_Enter == k:
            self.confirm_click_slot()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AddDataWidget()
    win.show()
    sys.exit(app.exec())
