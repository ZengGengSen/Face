from PyQt5.QtWidgets import QWidget, qApp, QFileDialog, QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from ui_widget import Ui_Widget
from show_widget import ShowWidget
from database import db
from detector import dt
import cv2
import numpy as np
import sys
from PIL import Image, ImageDraw, ImageFont
import qss


def recognition(face_feature):
    def func(im1, im2):
        im = im1 - im2
        return np.dot(im, im)
    for f in db.faces:
        if func(face_feature, f.p_feature) < 0.2:
            return f.p_name


def rec_faces(image):
    rects = dt.face_detector(image, 1)
    names = []
    for i, r in enumerate(rects):
        shape = dt.shape_predictor(image, rects[i])
        face_feature = dt.feature_model.compute_face_descriptor(image, shape)
        face_name = recognition(face_feature)
        if face_name:
            names.append(face_name)
        else:
            names.append('None')
    return rects, names


def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=80):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


class Widget(QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setupUi(self)

        self.timer_camera = QTimer()
        self.cap = cv2.VideoCapture()
        self.show_data_widget = ShowWidget()
        self.show_data_widget.setStyleSheet(qss.qssStyle)

        self.timer_camera.timeout.connect(self.show_camera)
        self.show_face_button.clicked.connect(self.show_data_widget.show)
        self.pic_rec_button.clicked.connect(self.open_image_action)
        self.cap_rec_button.clicked.connect(self.open_camera_action)
        self.quit.clicked.connect(qApp.quit)

    def show_camera(self):
        flag, image = self.cap.read()
        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        rects, names = rec_faces(show)
        for i, r in enumerate(rects):
            show = cv2.rectangle(show, (r.left(), r.top()), (r.right(), r.bottom()), (0, 255, 0), 2)
            show = cv2ImgAddText(show, names[i], r.left(), r.top(), (255, 0, 0))
        show_image = QImage(
            show.data,
            show.shape[1],
            show.shape[0],
            QImage.Format_RGB888
        )
        self.picture.setPixmap(QPixmap.fromImage(show_image))

    def open_image_action(self):
        if self.timer_camera.isActive():
            self.timer_camera.stop()
            self.cap.release()
            self.label.clear()
            self.cap_rec_button.setText(u'打开相机识别')
        path = 'C:/Users/stone/Pictures/'
        file_path = QFileDialog.getOpenFileNames(None, "请选择要添加的文件", path, "Text Files (*.png, *.jpg);;All Files (*)")
        if len(file_path[0]) > 0:
            image = cv2.imread(file_path[0][0])
            image = cv2.resize(image, (640, 480))
            show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            rects, names = rec_faces(show)

            for i, r in enumerate(rects):
                show = cv2.rectangle(show, (r.left(), r.top()), (r.right(), r.bottom()), (0, 255, 0), 2)
                show = cv2ImgAddText(show, names[i], r.left(), r.top(), (255, 0, 0))

            show_image = QImage(
                show.data,
                show.shape[1],
                show.shape[0],
                QImage.Format_RGB888
            )
            self.picture.setPixmap(QPixmap.fromImage(show_image))

    def open_camera_action(self):
        if not self.timer_camera.isActive():
            flag = self.cap.open(0)
            if not flag:
                msg = QMessageBox.Warning(
                    self,
                    u'Warning',
                    u'请检测相机与电脑是否连接正确',
                    QMessageBox.Ok,
                    QMessageBox.Ok
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
    win = Widget()
    win.setStyleSheet(qss.qssStyle)
    win.show()
    sys.exit(App.exec_())
