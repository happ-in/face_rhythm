import sys, cv2
import pyautogui, dlib
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 850
ORANGE = (250, 150, 0)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Face Rhythm')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        title = QLabel('Face Rhythm', self)
        font = QFont()
        font.setPointSize(50)
        title.setFont(font)
        title.move(280, 230)
        title.resize(530, 130)

        game_start = QPushButton('Game Start', self)
        game_start.move(400, 530)
        game_start.resize(230, 50)
        game_start.clicked.connect(GameStart)

        setting_btn = QPushButton('Setting', self)
        setting_btn.move(400, 600)
        setting_btn.resize(230, 50)

        rank_btn = QPushButton('Rank', self)
        rank_btn.move(400, 670)
        rank_btn.resize(230, 50)

        self.show()

class GameStart(QWidget):
    def __init__(self):
        super().__init__()
        self.camUI()

    def camUI(self):
        self.capture = cv2.VideoCapture(0)

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 850)

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        while True:
            ret, frame = self.capture.read()
            #frame.shape[0] = 세로길이, frame.shape[1] = 가로길이
            cv2.line(frame, (0, 100), (frame.shape[1], 100), (0, 0, 255), 3)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(frame)

            for face in faces:
                dlib_shape = predictor(frame, face)
                shape_2d = np.array([[p.x, p.y] for p in dlib_shape.parts()])

            frame = cv2.rectangle(frame, pt1=(face.left(), face.top()), pt2=(face.right(), face.bottom()), color=(255,255,255))

            for s in shape_2d:
                cv2.circle(frame, center=tuple(s), radius=1, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

            # faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            #
            # for (x, y, w, h) in faces:
            #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

            cv2.imshow("face_rhythm", frame)

            if cv2.waitKey(1) == 27 :
                self.mini_setting()
                self.show()
                cv2.waitKey(0)

        self.capture.release()
        cv2.destroyAllWindows()

    def mini_setting(self):
        self.setWindowTitle('Setting')
        self.resize(550, 735)

        title = QLabel('Setting', self)
        font = QFont()
        font.setPointSize(25)
        title.setFont(font)
        title.move(210, 125)
        title.resize(530, 130)

        restart_game = QPushButton('Restart', self)
        restart_game.move(180, 250)
        restart_game.resize(220, 55)
        restart_game.clicked.connect(self.restartGame)

        replay_game = QPushButton('Replay', self)
        replay_game.move(180,360)
        replay_game.resize(220, 55)
        replay_game.clicked.connect(self.replayGame)

        exit_btn = QPushButton('Exit', self)
        exit_btn.move(180, 470)
        exit_btn.resize(220, 55)
        exit_btn.clicked.connect(sys.exit)

    def replayGame(self):
        self.close()
        pyautogui.press('a')

    def restartGame(self):
        self.close()
        self.capture.release()
        cv2.destroyAllWindows()

        self.camUI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())



