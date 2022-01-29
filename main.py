import sys
import cv2
import DataSet

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

db = DataSet.DataSet()
db.load()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.timer_camera = QTimer()         # 初始化定时器
        self.cap = cv2.VideoCapture()               # 初始化摄像头

        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayoutWidget = QWidget(self.central_widget)
        self.horizontalLayoutWidget.setGeometry(QRect(-1, -1, 801, 601))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QWidget(self.horizontalLayoutWidget)
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setGeometry(QRect(-1, -1, 701, 601))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item)
        self.verticalLayout2 = QVBoxLayout()
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.pic_rec_button = QPushButton(self.horizontalLayoutWidget)
        self.pic_rec_button.setObjectName("pic_rec_button")
        self.verticalLayout2.addWidget(self.pic_rec_button)
        self.cap_rec_button = QPushButton(self.horizontalLayoutWidget)
        self.cap_rec_button.setObjectName("cap_rec_button")
        self.verticalLayout2.addWidget(self.cap_rec_button)
        self.quit_button = QPushButton(self.horizontalLayoutWidget)
        self.quit_button.setObjectName("quit_button")
        self.verticalLayout2.addWidget(self.quit_button)
        self.verticalLayout.addLayout(self.verticalLayout2)
        spacer_item1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_item1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 9)
        self.horizontalLayout.setStretch(1, 1)
        self.setCentralWidget(self.central_widget)

        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pic_rec_button.setText(_translate("MainWindow", "图像识别"))
        self.cap_rec_button.setText(_translate("MainWindow", "打开相机识别"))
        self.quit_button.setText(_translate("MainWindow", "退出"))

        QMetaObject.connectSlotsByName(self)

        self.timer_camera.timeout.connect(self.show_camera)
        self.pic_rec_button.clicked.connect(self.open_image_action)
        self.cap_rec_button.clicked.connect(self.open_camera_action)
        self.quit_button.clicked.connect(qApp.quit)

        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def show_camera(self):
        flag, image = self.cap.read()
        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        rects, names = db.rec_faces(show)
        for i, r in enumerate(rects):
            show = cv2.rectangle(show, (r.left(), r.top()), (r.right(), r.bottom()), (0, 255, 0), 2)
            show = cv2.putText(show, names[i], (r.left(), r.top()), self.font, 1.2, (255, 0, 0), 2)
        show_image = QImage(
            show.data,
            show.shape[1],
            show.shape[0],
            QImage.Format_RGB888
        )
        self.label.setPixmap(QPixmap.fromImage(show_image))

    def open_image_action(self):
        if self.timer_camera.isActive():
            self.timer_camera.stop()
            self.cap.release()
            self.label.clear()
            self.cap_rec_button.setText(u'打开相机识别')
        path = 'C:/Users/stone/Pictures/'
        file_path = QFileDialog.getOpenFileNames(None, "请选择要添加的文件", path, "Text Files (*.png, *.jpg);;All Files (*)")
        image = cv2.imread(file_path[0][0])
        show = image.reshape((480, 640, 3))

        rects, names = db.rec_faces(show)
        for i, r in enumerate(rects):
            show = cv2.rectangle(show, (r.left(), r.top()), (r.right(), r.bottom()), (0, 255, 0), 2)
            show = cv2.putText(show, names[i], (r.left(), r.top()), self.font, 1.2, (255, 0, 0), 2)
        show_image = QImage(
            show.data,
            show.shape[1],
            show.shape[0],
            QImage.Format_RGB888
        )
        self.label.setPixmap(QPixmap.fromImage(show_image))

    def open_camera_action(self):
        if not self.timer_camera.isActive():
            flag = self.cap.open(0)
            if not flag:
                msg = QMessageBox.Warning(
                    self,
                    u'Warning',
                    u'请检测相机与电脑是否连接正确',
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok
                )
            else:
                self.timer_camera.start(30)
                self.cap_rec_button.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label.clear()
            self.cap_rec_button.setText(u'打开相机识别')


if __name__ == '__main__':
    App = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(App.exec_())
