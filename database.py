import sqlite3
import numpy as np
from PyQt5.QtGui import QImage, QPixmap


class FaceData:
    def __init__(self, m_name, m_image, m_feature):
        self.p_name = m_name
        self.p_image = m_image
        self.p_feature = m_feature

    def modify_name(self, m_name):
        self.p_name = m_name

    def modify_image(self, m_image, m_feature):
        self.p_image = m_image
        self.p_feature = m_feature

    def export_to_qpixmap(self):
        show_image = QImage(
            self.p_image.data,
            640,
            480,
            QImage.Format_RGB888
        )
        return QPixmap.fromImage(show_image)


class FaceDataBase:
    def __init__(self):
        self.connection = sqlite3.connect("FaceData.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Face(
                NAME TEXT PRIMARY KEY NOT NULL,
                IMAGE BLOB NOT NULL,
                FEATURE BLOB NOT NULL
            )
            """
        )
        self.connection.commit()
        self.cursor.execute("SELECT * FROM Face ORDER BY NAME ASC")
        self.faces = []
        self.new_faces = []
        self.del_faces = []
        for data in self.cursor.fetchall():
            data_image = np.frombuffer(data[1], dtype=np.uint8)
            data_feature = np.frombuffer(data[2], dtype=np.float64)
            data_image = data_image.reshape((480, 640, 3))
            face_data = FaceData(data[0], data_image, data_feature)
            self.faces.append(face_data)

    def insert_data(self, name, image, feature):
        data = FaceData(name, image, feature)
        self.faces.append(data)
        self.new_faces.append(data)

    def delete_data(self, name):
        for f in self.faces:
            if f.p_name == name:
                self.del_faces.append(f)
                self.faces.remove(f)

    def save(self):
        for f in self.del_faces:
            self.cursor.execute(
                """
                DELETE FROM Face
                WHERE NAME = '%s'
                """
                %
                f.p_name
            )
            self.del_faces.clear()
            self.connection.commit()
        for f in self.new_faces:
            self.cursor.execute(
                """
                INSERT INTO Face (NAME, IMAGE, FEATURE) 
                VALUES (?, ?, ?)
                """,
                (f.p_name, f.p_image, f.p_feature)
            )
            self.new_faces.clear()
            self.connection.commit()


db = FaceDataBase()
