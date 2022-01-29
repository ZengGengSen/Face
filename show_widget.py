from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, qApp
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from ui_show_widget import Ui_Show_Widget
from database import db
from add_data_widget import AddDataWidget
import sys


class ShowWidget(QWidget, Ui_Show_Widget):
    def __init__(self, parent=None):
        super(ShowWidget, self).__init__(parent)
        self.setupUi(self)
        for data in db.faces:
            self.listWidget.addItem(data.p_name)
        self.add_data_widget = AddDataWidget()
        self.add_data_widget.setWindowModality(Qt.ApplicationModal)
        self.box = QMessageBox(QMessageBox.Question, '提示', '是否删除该条数据')
        self.yes = self.box.addButton('确定', QMessageBox.YesRole)
        self.no = self.box.addButton('取消', QMessageBox.NoRole)

        if len(db.faces) > 0:
            self.listWidget.setCurrentRow(0)
            self.label.setPixmap(db.faces[0].export_to_qpixmap())

        self.listWidget.itemClicked.connect(self.list_item_clicked_slot)
        self.add_data.clicked.connect(self.add_data_widget.show)
        self.delete_data.clicked.connect(self.delete_data_clicked)
        self.add_data_widget.cancel.clicked.connect(self.modify_items)

    def list_item_clicked_slot(self, list_item):
        self.listWidget.setCurrentItem(list_item)
        i = self.listWidget.currentRow()
        self.label.setPixmap(db.faces[i].export_to_qpixmap())

    def modify_items(self):
        item = self.listWidget.currentItem()
        self.listWidget.clear()
        for f in db.faces:
            self.listWidget.addItem(f.p_name)
        if len(db.faces) > 0:
            self.listWidget.setCurrentItem(item)
            self.label.setPixmap(
                db.faces[self.listWidget.currentRow()].export_to_qpixmap()
            )

    def delete_data_clicked(self):
        self.box.exec_()
        if self.box.clickedButton() == self.yes:
            i = self.listWidget.currentRow()
            name = self.listWidget.item(i).text()
            self.listWidget.takeItem(i)
            db.delete_data(name)
            self.label.clear()
            if len(db.faces) > 0:
                self.listWidget.setCurrentRow(0)
                self.label.setPixmap(db.faces[0].export_to_qpixmap())

    def closeEvent(self, event: QCloseEvent) -> None:
        db.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ShowWidget()
    win.show()
    sys.exit(app.exec())
