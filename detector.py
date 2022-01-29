import dlib
import numpy as np


class Detector:
    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor('./dat/shape_predictor_68_face_landmarks.dat')
        self.feature_model = dlib.face_recognition_model_v1('./dat/dlib_face_recognition_resnet_model_v1.dat')

    def ext_feature(self, image):
        rects = self.face_detector(image, 1)
        if len(rects) == 1:
            shape = self.shape_predictor(image, rects[0])
            face_feature = self.feature_model.compute_face_descriptor(image, shape)
            return np.array(face_feature)
        else:
            return None



dt = Detector()
